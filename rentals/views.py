from django.shortcuts import render, get_object_or_404, redirect
from .models import Movie, Rental, Category
from django.contrib import messages
from .forms import MovieForm, UserRegisterForm, RentalForm, UserProfileForm
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash


@login_required
def edit_profile(request):
    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST, instance=request.user)
        password_form = PasswordChangeForm(request.user, request.POST)

        if profile_form.is_valid() and password_form.is_valid():
            profile_form.save()
            user = password_form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your profile and password were successfully updated!')
            return redirect('rentals:profile')
        else:
            if not profile_form.is_valid():
                messages.error(request, 'Please correct the errors in your profile form.')
            if not password_form.is_valid():
                messages.error(request, 'Please correct the errors in your password form.')
    else:
        profile_form = UserProfileForm(instance=request.user)
        password_form = PasswordChangeForm(request.user)

    context = {
        'profile_form': profile_form,
        'password_form': password_form,
    }
    return render(request, 'rentals/edit_profile.html', context)


@login_required
def profile(request):
    current_user = request.user
    current_time = timezone.now()

    active_rentals = Rental.objects.filter(user=current_user, returned=False)
    rental_history = Rental.objects.filter(user=current_user, returned=True)

    for rental in active_rentals:
        time_left = rental.return_date - current_time
        rental.time_left = int(time_left.total_seconds() // 3600)

    context = {
        'active_rentals': active_rentals,
        'rental_history': rental_history,
    }

    return render(request, 'rentals/profile.html', context)


def home(request):
    movies = Movie.objects.all()
    selected_movies = movies[:5]
    context = {
        'movies': movies,
        'selected_movies': selected_movies,
    }
    return render(request, 'home.html', context)


def movie_list(request):
    movies = Movie.objects.all()
    categories = Category.objects.all()

    category_id = request.GET.get('category')
    if category_id:
        movies = movies.filter(category__id=category_id)

    query = request.GET.get('search')
    if query:
        movies = movies.filter(title__icontains=query)

    context = {
        'movies': movies,
        'categories': categories,
    }
    return render(request, 'rentals/movie_list.html', context)


@login_required
def movie_detail(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    current_user = request.user

    is_rented = Rental.objects.filter(user=current_user, movie=movie, returned=False).exists()

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

    #active_rental = Rental.objects.filter(user=current_user, movie=movie, returned=True).exists()

    #if active_rental:
    #    messages.warning(request, 'You have already rented this movie.')
    #    return redirect('rentals:movie_detail', pk=movie_id)

    current_time = timezone.now()
    return_date = current_time + timezone.timedelta(hours=24)

    rental = Rental(user=current_user, movie=movie, return_date=return_date, returned=False)
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
