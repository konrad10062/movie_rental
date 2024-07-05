from django.shortcuts import render, get_object_or_404, redirect
from .models import Movie, Rental
from django.contrib import messages
from .forms import MovieForm, UserRegisterForm, RentalForm
from django.contrib.auth.decorators import login_required
from django.utils import timezone


@login_required
def profile(request):
    current_user = request.user
    current_time = timezone.now()

    active_rentals = Rental.objects.filter(user=current_user, returned=False)
    rental_history = Rental.objects.filter(user=current_user, returned=True)

    # Oblicz czas pozostały do zwrotu dla każdego wypożyczenia
    for rental in active_rentals:
        time_left = rental.return_date - current_time
        rental.time_left = int(time_left.total_seconds() // 3600)  # Pozostały czas w godzinach

    context = {
        'active_rentals': active_rentals,
        'rental_history': rental_history,
    }

    return render(request, 'rentals/profile.html', context)


def home(request):
    return render(request, 'home.html')


def movie_list(request):
    movies = Movie.objects.all()

    # Filtrowanie po kategorii
    category = request.GET.get('category')
    if category:
        movies = movies.filter(category__name=category)

    # Wyszukiwanie po nazwie filmu
    query = request.GET.get('q')
    if query:
        movies = movies.filter(title__icontains=query)

    return render(request, 'rentals/movie_list.html', {'movies': movies})


@login_required
def movie_detail(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    current_user = request.user

    # Sprawdzenie, czy użytkownik już wypożyczył ten film
    is_rented = Rental.objects.filter(user=current_user, movie=movie).exists()

    context = {
        'movie': movie,
        'is_rented': is_rented
    }

    return render(request, 'rentals/movie_detail.html', context)


@login_required
def add_movie(request):
    if request.method == "POST":
        form = MovieForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('movie_list')
    else:
        form = MovieForm()
    return render(request, 'rentals/add_movie.html', {'form': form})


@login_required
def rent_movie(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    current_user = request.user

    # Sprawdzenie, czy użytkownik już wypożyczył ten film
    if Rental.objects.filter(user=current_user, movie=movie).exists():
        messages.warning(request, 'You have already rented this movie.')
        return redirect('rentals:movie_detail', pk=movie_id)  # Przekierowanie z powrotem do szczegółów filmu

    # Jeśli użytkownik jeszcze nie wypożyczył filmu, dodaj nowe wypożyczenie
    current_time = timezone.now()
    return_date = current_time + timezone.timedelta(hours=24)  # Ustawienie czasu zwrotu za 24 godziny

    rental = Rental(user=current_user, movie=movie, return_date=return_date)
    rental.save()

    messages.success(request, 'Movie rented successfully.')
    return redirect('rentals:profile')


@login_required
def return_movie(request, rental_id):
    rental = get_object_or_404(Rental, pk=rental_id, user=request.user)

    if request.method == 'POST':
        rental.returned = True
        rental.save()
        messages.success(request, 'Movie returned successfully.')

    return redirect('rentals:profile')


def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created! You are now able to log in')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})
