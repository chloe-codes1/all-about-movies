from django.shortcuts import render
from .models import Movie, Comment, Review

# Create your views here.
def home(request):
    movies = Movie.objects.all()
    context = {
        'movies': movies
    }
    return render(request, 'movies/home.html', context)

