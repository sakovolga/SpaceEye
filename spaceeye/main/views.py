from datetime import timedelta, datetime

from django.http import JsonResponse
from django.shortcuts import render
from django.core.cache import cache
from django.conf import settings
import requests
import logging

logger = logging.getLogger(__name__)

def index(request):
    selected_date = request.GET.get('date')

    if selected_date:
        try:
            datetime.strptime(selected_date, '%Y-%m-%d')
        except ValueError:
            selected_date = None

    nasa_data = get_apod_data(selected_date)

    date_options = []
    today = datetime.now().date()
    for i in range(30):
        date = today - timedelta(days=i)
        date_options.append({
            'value': date.strftime('%Y-%m-%d'),
            'display': date.strftime('%B %d, %Y')
        })

    context = {
        'nasa_data': nasa_data,
        'selected_date': selected_date,
        'date_options': date_options
    }

    return render(request, 'main/index.html', context)


def get_apod_data(date=None):
    cache_key = f'nasa_apod_data_{date or "today"}'
    cached_data = cache.get(cache_key)

    if cached_data:
        return cached_data

    api_key = settings.NASA_API_KEY
    url = 'https://api.nasa.gov/planetary/apod'
    params = {'api_key': api_key}

    if date:
        params['date'] = date

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        data['source'] = 'apod'

        if data.get('media_type') != 'image':
            data['error'] = 'Video available for this date instead of image'
            cache.set(cache_key, data, 60 * 60)
        else:
            cache_time = 60 * 60 * 24 if date else 60 * 60 * 2
            cache.set(cache_key, data, cache_time)

    except requests.exceptions.RequestException as e:
        logger.error(f"NASA APOD API request failed: {str(e)}")
        data = {'error': 'Failed to load APOD data', 'source': 'apod'}
        cache.set(cache_key, data, 60 * 5)
    except Exception as e:
        logger.error(f"Unexpected error in APOD: {str(e)}")
        data = {'error': 'Internal server error', 'source': 'apod'}
        cache.set(cache_key, data, 60 * 5)

    return data


def mars_rover_photos(request):
    sol = request.GET.get('sol', '1000')
    rover = request.GET.get('rover', 'curiosity')

    try:
        sol = int(sol)
    except ValueError:
        sol = 1000

    photos_data = get_mars_rover_data(rover, sol)

    context = {
        'photos_data': photos_data,
        'selected_rover': rover,
        'selected_sol': sol,
        'rover_options': [
            {'value': 'curiosity', 'name': 'Curiosity'},
            {'value': 'opportunity', 'name': 'Opportunity'},
            {'value': 'spirit', 'name': 'Spirit'},
            {'value': 'perseverance', 'name': 'Perseverance'}
        ]
    }

    return render(request, 'main/mars_rover.html', context)


def get_mars_rover_data(rover, sol):
    cache_key = f'mars_rover_{rover}_{sol}'
    cached_data = cache.get(cache_key)

    if cached_data:
        return cached_data

    api_key = settings.NASA_API_KEY
    url = f'https://api.nasa.gov/mars-photos/api/v1/rovers/{rover}/photos'
    params = {
        'api_key': api_key,
        'sol': sol,
        'page': 1
    }

    try:
        response = requests.get(url, params=params, timeout=15)
        response.raise_for_status()
        data = response.json()

        if data.get('photos'):
            data['photos'] = data['photos'][:12]
            data['total_photos'] = len(data['photos'])

        data['source'] = 'mars_rover'
        data['rover_name'] = rover.title()
        data['sol'] = sol

        cache.set(cache_key, data, 60 * 60 * 24 * 7)

    except requests.exceptions.RequestException as e:
        logger.error(f"Mars Rover API request failed: {str(e)}")
        data = {
            'error': f'Failed to load {rover} photos for sol {sol}',
            'source': 'mars_rover',
            'photos': []
        }
        cache.set(cache_key, data, 60 * 5)
    except Exception as e:
        logger.error(f"Unexpected error in Mars Rover: {str(e)}")
        data = {
            'error': 'Internal server error',
            'source': 'mars_rover',
            'photos': []
        }
        cache.set(cache_key, data, 60 * 5)

    return data

def api_data_ajax(request):
    api_type = request.GET.get('type')

    if api_type == 'apod':
        date = request.GET.get('date')
        data = get_apod_data(date)
    elif api_type == 'mars_rover':
        rover = request.GET.get('rover', 'curiosity')
        sol = int(request.GET.get('sol', 1000))
        data = get_mars_rover_data(rover, sol)
    else:
        data = {'error': 'Invalid API type'}

    return JsonResponse(data)
