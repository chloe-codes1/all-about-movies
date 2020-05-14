from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.db.models import Count, Prefetch

from .models import Movie, Comment, Review
from .forms import MovieForm, CommentForm, ReviewForm

from django.conf import settings
import requests


# Create your views here.



# main page - 영화 전체 목록
def home(request):
    movies = Movie.objects.order_by('-vote_average')[:8]
    boxoffice = movies[:3]
    context = {
        'movies': movies,
        'boxoffice': boxoffice,

    }
    return render(request, 'movies/home.html', context)

# review list page
def review_list(request):
    reviews = Review.objects.prefetch_related(
        Prefetch('comments',
                 queryset = Comment.objects.select_related('user'))
        ).order_by('-pk')
    context = {
        'reviews': reviews,
    }
    return render(request, 'movies/review_list.html', context)

# 전체 영화들 보기
def movie_list(request):
    movies = Movie.objects.order_by('-vote_average')
    context = {
        'movies': movies,

    }
    return render(request, 'movies/movie_list.html', context)


# 영화별 상세보기 - 해당 영화 리뷰출력
def movie_detail(request, movie_pk):
    movie = get_object_or_404(Movie, id=movie_pk)
    tmdb_id = movie.tmdb_id
    url = f'https://api.themoviedb.org/3/movie/{tmdb_id}?api_key=763c6d15a6a1f3af5c6b8f7cb7b3fdcd&language=en-US&language=en-US'
    response = requests.get(url).json()
    data = response['genres']
    release_date = response['release_date']
    country = response['production_countries'][0].get('name')
    genres = (data[i].get('name') for i in range(len(data)))
    context = {
        'movie': movie,
        'genres': genres,
        'release_date': release_date,
        'country': country
    }
    return render(request, 'movies/movie_detail.html', context)

# 리뷰 작성 - review에 사진 첨부 할 수 있음!
@login_required
def review_create(request, movie_pk):
    if request.method == 'POST':
        movie = get_object_or_404(Movie, id= movie_pk)
        form = ReviewForm(request.POST, request.FILES)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.movie = movie
            review.save()
            return redirect('movies:movie_detail', movie_pk)
        messages.warning(request, 'Please check the form submitted')
    else:
        form = ReviewForm()
    context = {
        'form': form,
    }
    return render(request, 'movies/forms.html',context)

# 리뷰 상세보기 - 각 리뷰 별 댓글 목록/댓글 입력창 출력
def review_detail(request, review_pk):
    review = get_object_or_404(Review, id= review_pk)
    form = CommentForm()
    context = {
        'review': review,
        'form': form,
    }
    return render(request, 'movies/review_detail.html', context)


@login_required
def review_update(request, review_pk):
    review = get_object_or_404(Review, id=review_pk)
    if request.user == review.user:
        if request.method == 'POST':
            form = ReviewForm(request.POST, request.FILES, instance=review)
            if form.is_valid():
                review = form.save(commit=False)
                review.user = request.user
                review.save()
                return redirect('movies:review_detail', review.pk)
        else:
            form = ReviewForm(instance=review)
        context = {
            'form':form
        }
        return render(request, 'movies:forms.html', context)
    else:
        messages.warning(request, "Editting other people's review is not allowed")
        return redirect('movies:review_detail')


@login_required
@require_POST
def review_delete(request, review_pk):
    review = get_object_or_404(Review, id=review_pk)
    if request.user == post.user:
        review.delete()
        messages.add_message(request, messages.SUCCESS, 'Your review has been successfully deleted!')
    return redirect('movies:home')



# 댓글 작성 - 각 리뷰에 대한 댓글 입력
@login_required
@require_POST
def comment_create(request, review_pk):
    review = get_object_or_404(Review, pk=review_pk)
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.review = review
        comment.user = request.user
        comment.save()
    return redirect('movies:review_detail', review.pk)


# 댓글 삭제 - 댓글 작성자일떄만 삭제
@login_required
@require_POST
def comment_delete(request, review_pk, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)
    if request.user == comment.user:
        comment.delete()
    return redirect('movies:review_detail', review_pk)


@login_required
def like(request, review_pk):
    review = get_object_or_404(Review, id=review_pk)
    user = request.user
    # ver1)
    # if request.user in article.liked_users.all():

    # ver2)
    if review.like_users.filter(id=user.id).exists():
        review.like_users.remove(user)
    else:
        review.like_users.add(user)
    return redirect('movies:review_detail', review_pk)