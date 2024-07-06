from django.urls import path
from . import views

app_name = 'rentals'

urlpatterns = [
    path('', views.home, name='home'),
    path('movies/', views.movie_list, name='movie_list'),
    path('movies/<int:pk>/', views.movie_detail, name='movie_detail'),
    path('movies/<int:movie_id>/rent/', views.rent_movie, name='rent_movie'),
    path('return/<int:rental_id>/', views.return_movie, name='return_movie'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
]
