from django.contrib import admin
from .models import Movie, Rental, Category

admin.site.register(Movie)
admin.site.register(Rental)
admin.site.register(Category)
