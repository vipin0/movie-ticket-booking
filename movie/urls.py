from django.urls import path
from .views import *
app_name = 'movie'
urlpatterns = [
    path('', HomePage.as_view(), name='home'),
    path('<int:movie_id>/', movie_details, name='detail'),
    path('search/', SearchView.as_view(), name='search'),
    path('movies/', MovieListView.as_view(), name='movie-list'),
    path('admin/add-movie', add_movie, name='add-movie'),
    path('admin/add-show', add_show, name='add-show'),

]
