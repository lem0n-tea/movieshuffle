import datetime, ast
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.http import urlencode
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.paginator import Paginator
from .models import Watchlist, Genre, Movie, CachedSearch
from .utils import imdb_search_results, download_and_compress_img, get_neighbor_pages


def home(request):
    return render(request, 'movies/home.html')

@login_required
def watchlist(request):
    user_watchlist = Watchlist.objects.filter(user=request.user)[0]
    search_query = request.GET.get('search')
    
    if search_query:
        movies = user_watchlist.movies.filter(title__icontains=search_query)
    else:
        movies = user_watchlist.movies.all()

    # Get genres present in user's watchlist for filtering
    genre_ids = movies.values_list('genres', flat=True).distinct()
    available_genres = Genre.objects.filter(id__in=genre_ids).order_by('name')

    # Filter by genres
    selected_genres = [int(genre_id) for genre_id in request.GET.getlist('genre')]
    if selected_genres:
        movies = movies.filter(genres__in=selected_genres).distinct()

    movies = movies.order_by('title')

    # Pagination
    paginator = Paginator(movies, 5)
    page_number = request.GET.get('page')
    movies_for_display = paginator.get_page(page_number)

    # Get list of 3 pages with current and its closest
    if page_number:
        closest_pages = get_neighbor_pages(paginator.num_pages, int(page_number))
    else:
        closest_pages = get_neighbor_pages(paginator.num_pages, 1)

    test = request.GET.get('selected_genres')
    return render(request, 'movies/watchlist.html', context={
        'movies': movies_for_display,
        'prev_query': search_query,
        'genres': available_genres,
        'selected_genres': selected_genres,
        'closest_pages': closest_pages,
        'test': test,
    })

@login_required
def add_new(request):
    if request.method == 'POST':
        # Identify if the user is adding new item to the watchlist
        if request.POST.get('id'):
            # Check if chosen movie is in database
            if Movie.objects.filter(imdb_id=request.POST.get('id')).exists():
                # Pull movie from database and add it to user watchlist
                chosen_movie = Movie.objects.get(imdb_id=request.POST.get('id'))
                user_watchlist = Watchlist.objects.get(user=request.user)
                user_watchlist.movies.add(chosen_movie)
            else:
                # Add new movie to Movie
                new_movie = Movie.objects.create(
                    imdb_id = request.POST.get('id'),
                    title = request.POST.get('primaryTitle'),
                    description = request.POST.get('description'),
                    release_year = int(request.POST.get('startYear'))
                )

                for genre in request.POST.get('genres').split(', '):
                    obj, _ = Genre.objects.get_or_create(name=genre)
                    new_movie.genres.add(obj)
                
                # Poster upload and compression
                if request.POST.get('primaryImage'):
                    download_and_compress_img(request.POST.get('primaryImage'), new_movie)

                new_movie.save()

                # Add new movie to user watchlist
                user_watchlist = Watchlist.objects.get(user=request.user)
                user_watchlist.movies.add(new_movie)
        else:
            #found_movies = []
            search_query = request.POST.get('search')
            #request.session['last_search'] = search_query 
            # Searching for movies by user's query
            try:
                # Searches for cached search results
                cached_search = CachedSearch.objects.get(search_query=search_query.lower())
                
                # Checks if the cached result been updated within a month
                if (datetime.datetime.now().date() - cached_search.last_updated).days > 30:
                    # Call API and update cache
                    setattr(cached_search, 'results', imdb_search_results(search_query))
                    cached_search.save()

                #found_movies = cached_search.results
            except CachedSearch.DoesNotExist:
                # Make an API call and cache the response
                cached_search = CachedSearch.objects.create(search_query=search_query.lower(), results=imdb_search_results(search_query))
                #found_movies = cached_search.results

            return redirect('{}?{}'.format(reverse('add-new'), urlencode({'search': search_query})))

    else:
        search_query = request.GET.get('search')
        #search_query = request.session.get('last_search', None)
        if not search_query:
            return render(request, 'movies/add_new.html')
        
        found_movies = CachedSearch.objects.get(search_query=search_query.lower()).results

        # Finding intersection between search results and user's watchlist to place already added items on top
        user_movies_id = set(Watchlist.objects.get(user=request.user).movies.values_list('imdb_id', flat=True))
        found_movies_id = set([item['id'] for item in found_movies])

        # Movies in search results that are already added to user's watchlist
        already_added = user_movies_id & found_movies_id
        user_movies = list(Movie.objects.filter(pk__in=already_added))

        # The rest movies from search result
        found_movies = [item for item in found_movies if not item['id'] in already_added]

        # Pagination
        paginator = Paginator(user_movies + found_movies, 5)
        page_number = request.GET.get('page')
        movies_for_display = paginator.get_page(page_number)

        # Get list of 3 pages with current and its closest
        if page_number:
            closest_pages = get_neighbor_pages(paginator.num_pages, int(page_number))
        else:
            closest_pages = get_neighbor_pages(paginator.num_pages, 1)

        return render(request, 'movies/add_new.html', context={
            'prev_query': search_query,
            'movies': movies_for_display,
            'closest_pages': closest_pages,
            'user_movies': user_movies,
            #'found_movies': found_movies,
        })

@login_required
def remove_movie(request, movie_id):
    # TO KEEP SEARCH QUERY IN BAR AFTER REMOVAL, REWRITE DELETION TO PERFORM ON POST
    #search_query = request.GET.get('search')
    user_watchlist = Watchlist.objects.get(user=request.user)
    movie = Movie.objects.get(imdb_id=movie_id)
    user_watchlist.movies.remove(movie)

    return redirect(reverse('watchlist'))