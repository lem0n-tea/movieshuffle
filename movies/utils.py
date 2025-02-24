import requests
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile

API_URL = "https://imdb236.p.rapidapi.com/imdb/search"
HEADERS = {
    "x-rapidapi-key": "bd0d9c7e5cmsh218c3fb15824d3cp14f5b2jsn5d502ced974e",
    "x-rapidapi-host": "imdb236.p.rapidapi.com"
}


def imdb_search_results(search_query):
    search_query = search_query.lower()
    query = {"primaryTitleAutocomplete":search_query,"rows":"25","sortOrder":"DESC","sortField":"numVotes"}

    response = requests.get(API_URL, headers=HEADERS, params=query)
    response.raise_for_status()

    return response.json()['results']


def download_and_compress_img(image_url, instance):
    response = requests.get(image_url)
    if response.status_code != 200:
        return
    
    with BytesIO(response.content) as content_io:
        poster = Image.open(content_io)

        # Image compression
        poster_height = poster.height
        poster_width = poster.width
        poster = poster.resize((poster_width, poster_height), Image.NEAREST)

        with BytesIO() as poster_io:
            poster.save(poster_io, format='JPEG', quality=85)

            # Saving image
            poster_content = ContentFile(poster_io.getvalue())
            filename = f'{instance.imdb_id}-{instance.title}.jpg'
            instance.poster.save(filename, poster_content, save=False)


def get_neighbor_pages(total, target):
    # Range correction
    if target > total:
        target = total
    elif target < 1:
        target = 1

    # Window positioning
    start = max(1, target - 1)
    if start == total - 1 and total > 2:
        start -= 1

    end = min(target + 1, total)
    if end == 2 and total > 2:
        end += 1

    return [i for i in range(start, end + 1)]