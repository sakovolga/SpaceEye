# urls.py
from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.index, name='index'),
    path('mars-rover/', views.mars_rover_photos, name='mars_rover'),
    # path('earth-imagery/', views.earth_imagery, name='earth_imagery'),
    path('api/data/', views.api_data_ajax, name='api_data_ajax'),
]