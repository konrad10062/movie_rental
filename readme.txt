Movie Rental Application
This is a Django-based web application for renting movies.
The application allows users to browse, rent, and return movies.
It also includes functionalities for user registration, profile management, and movie filtering/searching.

Features

User Authentication:
Registration
Login/Logout
Profile management
Password change

Movie Management:
Browse movies
Filter by category
Search by title

Rental System:
Rent movies
Return movies
View active rentals
View rental history

Carousel:
Displays selected movies on the home page
Users can navigate through movies using left and right arrows

Setup
Prerequisites
Python 3.x
Django
Bootstrap (for front-end styling)
Docker

Installation
Clone the repository:
https://github.com/konrad10062/movie_rental.git

Create a docker container and install the required packages:
docker-compose up --build

Database migration:
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py makemigrations

Create a superuser to access the Django admin interface:
docker-compose run web python manage.py createsuperuser

Add sample movies to database:
docker-compose exec web python populate_movies.py

Access the application:
Open your browser and navigate to http://localhost:8000 to access the Movie Rental application.

Usage
Home Page
The home page displays a carousel with selected movies.
Users can navigate through the movies using the left and right arrows.
Clicking on a movie in the carousel redirects to the movie detail page.

Movies
Movie List:
Users can browse all available movies. They can filter movies by category and search by title.
Movie Detail:
The detail page of each movie provides more information about the movie and allows authenticated users to rent the movie.
Rentals
Profile:
The profile page shows active rentals and rental history. Users can return rented movies from this page.
Edit Profile:
Users can edit their profile information and change their password.
Project Structure
templates:
Contains all HTML templates for the application.
static:
Contains static files such as CSS and JavaScript.
rentals:
Contains Django app files including models, views, forms, and URLs.
Contributing
Feel free to fork the repository and submit pull requests.
For major changes, please open an issue first to discuss what you would like to change.


Additional Notes
Ensure that the required static files and Bootstrap are correctly linked in the base template.
Also, verify that all URLs and views are correctly set up in the urls.py and views.py files, respectively.