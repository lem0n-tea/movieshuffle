from django.db import models
from django.contrib.auth.models import User
from django.db.models.functions import Lower
from django.core.validators import MinValueValidator
from .storage import CacheStorage

'''
def cached_search_path(instance, filename):
    extension = filename.split('.')[-1]
    return f'search/{instance.search_query}.{extension}'
'''
    
# Caches the APi responses for search to reduce the number of requests per month
class CachedSearch(models.Model):
    search_query = models.CharField(max_length=200, primary_key=True)
    results = models.JSONField()
    last_updated = models.DateField(auto_now=True, blank=False)


class Genre(models.Model):
    name = models.CharField(max_length=200, help_text='Enter a genre', unique=True)

    def __str__(self):
        return self.name

    class Meta:
        constraints = [
            models.UniqueConstraint(
                Lower('name'),
                name = 'genre_name_case_insensitive_unique',
                violation_error_message = "Genre already exists (case insensitive match)"
            ),
        ]

def poster_upload_path(instance, filename):
    extension = filename.split('.')[-1]
    return f'posters/{instance.imdb_id}-{instance.title}.{extension}'

class Movie(models.Model):
    imdb_id = models.CharField(max_length=16, primary_key=True)
    title = models.CharField(max_length=200, help_text='Enter a title')
    description = models.TextField(max_length=2000, help_text='Enter a description', blank=True, null=True)
    poster = models.ImageField(upload_to=poster_upload_path, blank=True, null=True)
    genres = models.ManyToManyField(Genre)
    release_year = models.PositiveIntegerField(validators=[
        MinValueValidator(1900),
    ])

    def __str__(self):
        return f'{self.title} ({self.release_year})'
    
    def genre_list(self):
        return ', '.join([genre.name for genre in self.genres.all()])
    
class Watchlist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    movies = models.ManyToManyField(Movie, blank=True)

    def __str__(self):
        return f"{self.user}'s watchlist"
