from django.shortcuts import render
from django.core.cache import cache
from django.conf import settings
import requests
import logging

logger = logging.getLogger(__name__)

def index(request):
    cache_key = 'nasa_apod_data'
    cached_data = cache.get(cache_key)

    if cached_data:
        return render(request, 'main/index.html', {'nasa_data': cached_data})

    api_key = settings.NASA_API_KEY

    try:
        response = requests.get(
            f'https://api.nasa.gov/planetary/apod?api_key={api_key}',
            timeout=10
        )
        response.raise_for_status()

        data = response.json()

        if data.get('media_type') != 'image':
            data = {'error': 'Video available today instead of image'}
            cache.set(cache_key, data, 60 * 60)
        else:
            cache.set(cache_key, data, 60 * 60 * 24)

    except requests.exceptions.RequestException as e:
        logger.error(f"NASA API request failed: {str(e)}")
        data = {'error': 'Failed to load data'}
        cache.set(cache_key, data, 60 * 5)

    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        data = {'error': 'Internal server error'}
        cache.set(cache_key, data, 60 * 5)

    return render(request, 'main/index.html', {'nasa_data': data})