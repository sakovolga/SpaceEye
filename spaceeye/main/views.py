from datetime import timedelta, datetime

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core.cache import cache
from django.conf import settings
import requests
import logging
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib import messages
from .forms import CustomUserCreationForm
from .models import Favorite
import json

logger = logging.getLogger(__name__)


def index(request):
    selected_date = request.GET.get('date')

    if selected_date:
        try:
            datetime.strptime(selected_date, '%Y-%m-%d')
        except ValueError:
            selected_date = None

    nasa_data = get_apod_data(selected_date)

    is_favorited = False
    if request.user.is_authenticated and nasa_data.get('url'):
        is_favorited = Favorite.objects.filter(
            user=request.user,
            favorite_type='apod',
            image_url=nasa_data['url']
        ).exists()

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
        'date_options': date_options,
        'is_favorited': is_favorited
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


@login_required
def mars_rover_photos(request):
    sol = request.GET.get('sol', '1000')
    rover = request.GET.get('rover', 'curiosity')

    try:
        sol = int(sol)
    except ValueError:
        sol = 1000

    photos_data = get_mars_rover_data(rover, sol)

    if request.user.is_authenticated and photos_data.get('photos'):
        favorited_urls = set(
            Favorite.objects.filter(
                user=request.user,
                favorite_type='mars_rover'
            ).values_list('image_url', flat=True)
        )

        for photo in photos_data['photos']:
            photo['is_favorited'] = photo['img_src'] in favorited_urls

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


@login_required
def add_to_favorites(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            favorite_type = data.get('type')
            api_data = data.get('data')

            if favorite_type == 'apod':
                title = api_data.get('title', 'NASA APOD')
                description = api_data.get('explanation', '')[:500]  # Limit length
                image_url = api_data.get('url')
            elif favorite_type == 'mars_rover':
                camera_name = api_data.get('camera', {}).get('full_name', 'Unknown Camera')
                rover_name = api_data.get('rover', {}).get('name', 'Unknown Rover')
                title = f"{rover_name} - {camera_name}"
                description = f"Sol: {api_data.get('sol', 'Unknown')}, Earth Date: {api_data.get('earth_date', 'Unknown')}"
                image_url = api_data.get('img_src')
            else:
                return JsonResponse({'success': False, 'error': 'Invalid type'})

            if not image_url:
                return JsonResponse({'success': False, 'error': 'No image URL provided'})

            favorite, created = Favorite.objects.get_or_create(
                user=request.user,
                favorite_type=favorite_type,
                image_url=image_url,
                defaults={
                    'title': title,
                    'description': description,
                    'api_data': api_data
                }
            )

            if created:
                return JsonResponse({'success': True, 'action': 'added'})
            else:
                return JsonResponse({'success': False, 'error': 'Already in favorites'})

        except Exception as e:
            logger.error(f"Error adding to favorites: {str(e)}")
            return JsonResponse({'success': False, 'error': 'Server error'})

    return JsonResponse({'success': False, 'error': 'Invalid request method'})


@login_required
def remove_from_favorites(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            favorite_type = data.get('type')
            image_url = data.get('image_url')

            if not image_url:
                return JsonResponse({'success': False, 'error': 'No image URL provided'})

            deleted, _ = Favorite.objects.filter(
                user=request.user,
                favorite_type=favorite_type,
                image_url=image_url
            ).delete()

            if deleted:
                return JsonResponse({'success': True, 'action': 'removed'})
            else:
                return JsonResponse({'success': False, 'error': 'Not found in favorites'})

        except Exception as e:
            logger.error(f"Error removing from favorites: {str(e)}")
            return JsonResponse({'success': False, 'error': 'Server error'})

    return JsonResponse({'success': False, 'error': 'Invalid request method'})


@login_required
def favorites_list(request):
    favorites = Favorite.objects.filter(user=request.user)

    filter_type = request.GET.get('type')
    if filter_type in ['apod', 'mars_rover']:
        favorites = favorites.filter(favorite_type=filter_type)

    context = {
        'favorites': favorites,
        'filter_type': filter_type
    }

    return render(request, 'main/favorites.html', context)


@login_required
def delete_favorite(request, favorite_id):
    favorite = get_object_or_404(Favorite, id=favorite_id, user=request.user)
    favorite.delete()
    messages.success(request, 'Removed from favorites.')
    return redirect('main:favorites')


def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Welcome, {user.username}! You have successfully registered.')
            return redirect('main:index')
        else:
            messages.error(request, 'Please correct the errors in the form.')
    else:
        form = CustomUserCreationForm()

    return render(request, 'registration/register.html', {'form': form})