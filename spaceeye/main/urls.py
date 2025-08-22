# urls.py
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'main'

urlpatterns = [
    path('', views.index, name='index'),
    path('mars-rover/', views.mars_rover_photos, name='mars_rover'),
    path('api/data/', views.api_data_ajax, name='api_data_ajax'),

    # Авторизация
    path('login/', auth_views.LoginView.as_view(template_name='main/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='index'), name='logout'),
    path('register/', views.register_view, name='register'),
]
