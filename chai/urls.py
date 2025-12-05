from django.urls import path
from . import views

#localhost:8000/chai
urlpatterns = [
    path('', views.all_chai, name='all_chai'),
    path('<int:chai_id>/', views.chai_detail, name='chai_detail'),
    path('<int:chai_id>/favorite/', views.add_favorite, name='add_favorite'),
    path('chai_stores/', views.chai_store_view, name='chai_stores'),
    path('stores/<int:store_id>/', views.store_detail, name='store_detail'),
    path('top-rated/', views.top_rated_chais, name='top_rated'),
    path('recently-added/', views.recently_added_chais, name='recently_added'),
    path('my-favorites/', views.user_favorites, name='user_favorites'),
    path('my-reviews/', views.user_reviews, name='user_reviews'),
]