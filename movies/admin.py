from django.contrib import admin
from .models import Genre, Movie, Watchlist, CachedSearch

# Register your models here.
admin.site.register(Genre)
admin.site.register(Movie)
admin.site.register(Watchlist)
admin.site.register(CachedSearch)