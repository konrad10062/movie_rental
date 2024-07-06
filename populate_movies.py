import os
import django
from rentals.models import Movie, Category


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nazwa_twojego_projektu.settings')

django.setup()


def populate_movies():
    category1, _ = Category.objects.get_or_create(name='Kategoria 1')
    category2, _ = Category.objects.get_or_create(name='Kategoria 2')

    movies_to_add = [
        {'title': 'Pierwszy film', 'description': 'Opis pierwszego filmu', 'category': category1, 'release_date': '2024-01-01'},
        {'title': 'Drugi film', 'description': 'Opis drugiego filmu', 'category': category2, 'release_date': '2024-02-01'},
        {'title': 'Trzeci film', 'description': 'Opis trzeciego filmu', 'category': category1, 'release_date': '2024-03-01'},
        {'title': 'Czwarty film', 'description': 'Opis czwartego filmu', 'category': category2, 'release_date': '2024-04-01'},
        {'title': 'Piąty film', 'description': 'Opis piątego filmu', 'category': category1, 'release_date': '2024-05-01'},
        {'title': 'Szósty film', 'description': 'Opis szóstego filmu', 'category': category2, 'release_date': '2024-06-01'},
        {'title': 'Siódmy film', 'description': 'Opis siódmego filmu', 'category': category1, 'release_date': '2024-07-01'},
        {'title': 'Ósmy film', 'description': 'Opis ósmego filmu', 'category': category2, 'release_date': '2024-08-01'},
        {'title': 'Dziewiąty film', 'description': 'Opis dziewiątego filmu', 'category': category1, 'release_date': '2024-09-01'},
        {'title': 'Dziesiąty film', 'description': 'Opis dziesiątego filmu', 'category': category2, 'release_date': '2024-10-01'}
    ]

    for movie_data in movies_to_add:
        Movie.objects.create(
            title=movie_data['title'],
            description=movie_data['description'],
            category=movie_data['category'],
            release_date=movie_data['release_date']
        )

    print("Dodano 10 filmów do bazy danych.")

if __name__ == '__main__':
    populate_movies()
