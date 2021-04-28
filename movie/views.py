from datetime import datetime

from django.contrib.auth import authenticate, get_user_model, login
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.shortcuts import Http404, redirect, render
from django.utils.http import is_safe_url
from django.views.generic import CreateView, FormView, ListView, View
from .forms import MovieForm, ShowForm
from .models import *
from itertools import chain


class HomePage(View):
    def get(self, request, *args, **kwargs):
        movie_list = Movie.objects.all().order_by('-added')
        # top_list = movie_list[:3]
        # movie_list = movie_list[3:]
        context = {'movie_list': movie_list}
        return render(request, 'home.html', context)


class SearchView(ListView):
    template_name = 'search.html'

    def get_context_data(self, *args, **kwargs):
        context = super(SearchView, self).get_context_data(*args, **kwargs)
        query = self.request.GET.get('q')
        context['query'] = query
        return context

    def get_queryset(self, *args, **kwargs):
        request = self.request
        print(request.GET)
        query = request.GET.get('q')
        if query is not None:
            query = query.strip()
            return Movie.objects.search(query).order_by('-added')
        else:
            return Movie.objects.all()


class MovieListView(ListView):
    def get_queryset(self):
        return Movie.objects.all().order_by('-added')

    def get_context_data(self, *args, **kwargs):
        context = super(MovieListView, self).get_context_data(*args, **kwargs)
        movies = Movie.objects.all().order_by('-added')
        context = {'movie_list': movies}
        print(movies)
        print(context)
        return context


def movie_details(request, movie_id):
    try:
        movie_info = Movie.objects.get(pk=movie_id)
        
        day1 = Show.objects.filter(movie=movie_id,
                                   date=datetime.today())
        day2 = Show.objects.filter(movie=movie_id,
                                   date=datetime.today()+timedelta(days=1))
        day3 = Show.objects.filter(movie=movie_id,
                                   date=datetime.today()+timedelta(days=2))
        shows = list(chain(day1, day2, day3))
    except Movie.DoesNotExist:
        raise Http404("Page does not exist")
    return render(request, 'movie/movie_detail.html',
                  {'movie': movie_info, 'show_list': shows})


@login_required
def add_movie(request):
    template_name = 'movie/add_movie.html'
    print("qa")
    if request.method == 'POST':
        new_movie = MovieForm(request.POST, request.FILES)
        if new_movie.is_valid():
            new_movie.save()
            return redirect('admin')
    else:
        new_movie = MovieForm()
    return render(request, template_name, {'form': new_movie})


@login_required
def add_show(request):
    template_name = 'movie/add_show.html'

    if request.method == 'POST':
        show = ShowForm(request.POST)
        if show.is_valid():
            print(show)
            show.save()
            return redirect('admin')
    else:
        show = ShowForm()
    return render(request, template_name, {'form': show})
