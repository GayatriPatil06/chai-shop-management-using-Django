from django import forms
from .models import ChaiVariety, ChaiReview, ReviewComment, StoreRating

class ChaiVarietyForm(forms.Form):
    chai_variety = forms.ModelChoiceField(
        queryset=ChaiVariety.objects.all(),
        label="Select Chai Variety",
        empty_label="-- Choose a Chai --",
        widget=forms.Select(attrs={'class': 'form-control'}))

class ChaiReviewForm(forms.ModelForm):
    """Form for users to submit chai reviews"""
    class Meta:
        model = ChaiReview
        fields = ['review_text', 'rating']
        widgets = {
            'review_text': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Share your thoughts about this chai...'
            }),
            'rating': forms.RadioSelect(choices=[(i, f'{i} Star' + ('s' if i > 1 else '')) for i in range(1, 6)], attrs={
                'class': 'form-check-input'
            })
        }

class ReviewCommentForm(forms.ModelForm):
    """Form for commenting on reviews"""
    class Meta:
        model = ReviewComment
        fields = ['comment_text']
        widgets = {
            'comment_text': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Add your comment...'
            })
        }

class StoreRatingForm(forms.ModelForm):
    """Form for rating stores"""
    class Meta:
        model = StoreRating
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.RadioSelect(choices=[(i, f'{i} Star' + ('s' if i > 1 else '')) for i in range(1, 6)], attrs={
                'class': 'form-check-input'
            }),
            'comment': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Tell us about your experience...'
            })
        }

class ChaiFilterForm(forms.Form):
    """Form for filtering chais"""
    PRICE_CHOICES = [
        ('all', 'All Prices'),
        ('0-50', 'Under ₹50'),
        ('50-100', '₹50 - ₹100'),
        ('100-200', '₹100 - ₹200'),
        ('200+', '₹200+'),
    ]
    
    price_range = forms.ChoiceField(
        choices=PRICE_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    min_rating = forms.IntegerField(
        required=False,
        initial=0,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'max': 5})
    )
    chai_type = forms.MultipleChoiceField(
        choices=ChaiVariety.CHAI_TYPE_CHOICE,
        required=False,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'})
    )
