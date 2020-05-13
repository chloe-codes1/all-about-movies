from django.db import models
from django.conf import settings
from itertools import islice
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFit

#TMDB
from django.conf import settings
import requests


key = settings.TMDB_API_KEY
base_url = 'https://api.themoviedb.org/3/'


class Movie(models.Model):
    title = models.CharField(max_length=100)
    poster = models.URLField(max_length=200)
    genre = models.CharField(max_length=100)
    vote_average = models.FloatField()
    content = models.TextField()

    @classmethod
    def TMDB(cls, number):
        url = f'{base_url}movie/top_rated?api_key={key}&language=en-US&page=1'
        response = requests.get(url).json()
        data = response['results']
        for i in range(number):
            Movie.objects.create(
                    title=data[i].get('title'),
                    poster=data[i].get('poster_path'),
                    content=data[i].get('overview'),
                    genre=data[i].get('genre_ids'),
                    vote_average=data[i].get('vote_average')
                )

class Review(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='reviews')
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    rating = models.IntegerField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    #좋아요 기능
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                    related_name='like_posts')
    image = models.ImageField(blank=True)
    # DB 저장 x, 호출하게 되면 잘라서 표현
    image_thumbnail = ImageSpecField(source='image',
                                      processors=[ResizeToFit(300, 300)],
                                      format='JPEG',
                                      options={'quality': 60})


class Comment(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='comments')
    content = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
