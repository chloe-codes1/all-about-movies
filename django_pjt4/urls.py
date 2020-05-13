
from django.contrib import admin
from django.urls import path, include
from movies import views as movie_views
from accounts import views as accounts_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', movie_views.home, name='home'),

    path('movies/', include('movies.urls')),
    path('accounts/', include('accounts.urls')),
    path('<str:username>/follow/', accounts_views.follow, name='follow'),
    path('<str:username>/', accounts_views.profile, name='profile'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

