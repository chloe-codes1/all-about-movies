from django.urls import path
from . import views

app_name = 'movies'

urlpatterns = [
    path('reviews/', views.review_list, name='review_list'),
    path('<int:movie_pk>/', views.movie_detail, name='movie_detail'),
    path('<int:movie_pk>/reviews/', views.review_create, name='review_create'),
    path('<int:movie_pk>/reviews/<int:review_pk>/', views.review_detail, name='review_detail'),
    path('<int:movie_pk>/reviews/<int:review_pk>/update/', views.review_update, name='review_update'),
    path('<int:movie_pk>/reviews/<int:review_pk>/delete/', views.review_delete, name='review_delete'),
    path('<int:movie_pk>/reviews/<int:review_pk>/comments/', views.comment_create, name='comment_create'),
    path('<int:movie_pk>/reviews/<int:review_pk>/comments/<int:comment_pk>/delete/', views.comment_delete, name='comment_delete'),
    path('<int:review_pk>/like/', views.like, name='like'),
]