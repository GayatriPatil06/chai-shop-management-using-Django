from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q, Avg, Count
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from decimal import Decimal
from .models import ChaiVariety, Store, ChaiReview, Favorite, ReviewComment, StoreRating
from .forms import ChaiVarietyForm, ChaiReviewForm, ReviewCommentForm, StoreRatingForm, ChaiFilterForm

def all_chai(request):
    """Display all chai varieties with pagination, search, and filtering"""
    chais = ChaiVariety.objects.all()
    form = ChaiFilterForm(request.GET)
    
    # Search functionality
    query = request.GET.get('q')
    if query:
        chais = chais.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )
    
    # Filter by chai type
    chai_types = request.GET.getlist('chai_type')
    if chai_types:
        chais = chais.filter(chai_type__in=chai_types)
    
    # Filter by price range
    price_range = request.GET.get('price_range')
    if price_range and price_range != 'all':
        if price_range == '0-50':
            chais = chais.filter(price__lt=50)
        elif price_range == '50-100':
            chais = chais.filter(price__gte=50, price__lt=100)
        elif price_range == '100-200':
            chais = chais.filter(price__gte=100, price__lt=200)
        elif price_range == '200+':
            chais = chais.filter(price__gte=200)
    
    # Filter by minimum rating
    min_rating = request.GET.get('min_rating')
    if min_rating:
        try:
            min_rating = int(min_rating)
            # Annotate with average rating and filter
            chais = chais.annotate(avg_rating=Avg('reviews__rating')).filter(avg_rating__gte=min_rating)
        except (ValueError, TypeError):
            pass
    
    # Pagination
    paginator = Paginator(chais, 12)
    page_number = request.GET.get('page')
    
    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    
    # Add ratings to chais
    for chai in page_obj.object_list:
        chai.avg_rating = chai.get_average_rating()
        chai.review_count = chai.get_review_count()
    
    context = {
        'page_obj': page_obj,
        'chais': page_obj.object_list,
        'query': query,
        'form': form,
    }
    return render(request, 'chai/all_chai.html', context)

def chai_detail(request, chai_id):
    """Display chai details with reviews and allow adding reviews"""
    chai = get_object_or_404(ChaiVariety, pk=chai_id)
    reviews = chai.reviews.all()
    avg_rating = chai.get_average_rating()
    review_count = chai.get_review_count()
    favorite_count = chai.get_favorite_count()
    
    # Check if user has favorited this chai
    is_favorite = False
    if request.user.is_authenticated:
        is_favorite = Favorite.objects.filter(user=request.user, chai_variety=chai).exists()
    
    # Handle review submission (AJAX or POST)
    if request.user.is_authenticated and request.method == 'POST':
        try:
            import json
            if request.content_type == 'application/json':
                data = json.loads(request.body)
                review = ChaiReview(
                    user=request.user,
                    chai_variety=chai,
                    rating=data.get('rating'),
                    review_text=data.get('review_text')
                )
                review.full_clean()
                review.save()
                return JsonResponse({'success': True, 'message': 'Review posted successfully!'})
            else:
                review_form = ChaiReviewForm(request.POST)
                if review_form.is_valid():
                    review = review_form.save(commit=False)
                    review.user = request.user
                    review.chai_variety = chai
                    review.save()
                    return redirect('chai_detail', chai_id=chai_id)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)
    
    context = {
        'chai': chai,
        'reviews': reviews,
        'avg_rating': avg_rating,
        'review_count': review_count,
        'favorite_count': favorite_count,
        'is_favorite': is_favorite,
    }
    return render(request, 'chai/chai_detail.html', context)

@require_POST
def add_favorite(request, chai_id):
    """Add/remove chai from user's favorites (AJAX)"""
    if not request.user.is_authenticated:
        return JsonResponse({'success': False, 'error': 'Not authenticated'}, status=401)
    
    chai = get_object_or_404(ChaiVariety, pk=chai_id)
    favorite, created = Favorite.objects.get_or_create(user=request.user, chai_variety=chai)
    
    if not created:
        favorite.delete()
        favorited = False
    else:
        favorited = True
    
    return JsonResponse({
        'success': True,
        'favorited': favorited,
        'message': f"Added to favorites" if favorited else "Removed from favorites",
        'favorite_count': chai.get_favorite_count()
    })

def top_rated_chais(request):
    """Display top-rated chai varieties"""
    chais = ChaiVariety.objects.annotate(
        avg_rating=Avg('reviews__rating'),
        review_count=Count('reviews')
    ).filter(
        review_count__gt=0
    ).order_by('-avg_rating')[:10]
    
    context = {'chais': chais, 'title': 'Top Rated Chais'}
    return render(request, 'chai/top_rated.html', context)

def recently_added_chais(request):
    """Display recently added chai varieties"""
    chais = ChaiVariety.objects.order_by('-date_added')[:10]
    context = {'chais': chais, 'title': 'Recently Added Chais'}
    return render(request, 'chai/recently_added.html', context)

def chai_store_view(request):
    """Find stores that sell selected chai variety with ratings"""
    stores = None
    if request.method == 'POST':
        form = ChaiVarietyForm(request.POST)
        if form.is_valid():
            chai_variety = form.cleaned_data['chai_variety']
            stores = Store.objects.filter(chai_varieties=chai_variety).prefetch_related('chai_varieties')
            
            # Add ratings to stores
            for store in stores:
                store.avg_rating = store.get_average_rating()
                store.rating_count = store.get_rating_count()
    else:
        form = ChaiVarietyForm()

    context = {
        'stores': stores,
        'form': form,
    }
    return render(request, 'chai/chai_stores.html', context)

def store_detail(request, store_id):
    """Display store details with ratings"""
    store = get_object_or_404(Store, pk=store_id)
    ratings = store.ratings.all()
    avg_rating = store.get_average_rating()
    rating_count = store.get_rating_count()
    
    # Handle rating submission
    rating_form = None
    if request.user.is_authenticated:
        if request.method == 'POST':
            rating_form = StoreRatingForm(request.POST)
            if rating_form.is_valid():
                rating = rating_form.save(commit=False)
                rating.user = request.user
                rating.store = store
                rating.save()
                return redirect('store_detail', store_id=store_id)
        else:
            rating_form = StoreRatingForm()
    
    context = {
        'store': store,
        'ratings': ratings,
        'avg_rating': avg_rating,
        'rating_count': rating_count,
        'rating_form': rating_form,
    }
    return render(request, 'chai/store_detail.html', context)

@login_required(login_url='login')
def user_favorites(request):
    """Display user's favorite chais"""
    favorites = Favorite.objects.filter(user=request.user).select_related('chai_variety')
    context = {'favorites': favorites}
    return render(request, 'chai/favorites.html', context)

@login_required(login_url='login')
def user_reviews(request):
    """Display user's chai reviews"""
    reviews = ChaiReview.objects.filter(user=request.user).select_related('chai_variety')
    context = {'reviews': reviews}
    return render(request, 'chai/user_reviews.html', context)
