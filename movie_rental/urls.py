from django.contrib import admin
from django.urls import include, path
from rentals import views
from django.contrib.auth import views as auth_views
from rentals import views as rentals_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('rentals/', include('rentals.urls')),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('register/', rentals_views.register, name='register'),  # Dodana ścieżka rejestracji
]
