import datetime
from django.urls import reverse
from django.contrib.auth import get_user_model
import uuid
from django.db import models
from django.db.models import Q
from django.urls.base import reverse
from datetime import datetime, timedelta
# Create your models here.


class MovieQuerySet(models.query.QuerySet):
    def search(self, query):
        lookup = (
            Q(moviename__icontains=query)
        )
        return self.filter(lookup).distinct()


class MovieManager(models.Manager):
    def get_queryset(self):
        return MovieQuerySet(self.model, self._db)

    def search(self, query):
        return self.get_queryset().search(query)


User = get_user_model()
# Create your models here.


class Screen(models.Model):
    name = models.CharField(max_length=20)
    seats = models.IntegerField(default=10)

    def __str__(self) -> str:
        return str("Screen : "+self.name)


class Movie(models.Model):
    moviename = models.CharField("Movie Name", max_length=20, blank=False)
    poster = models.ImageField(
        null=True, blank=False, upload_to='%Y/%m/%d/')
    ticket_price = models.FloatField(null=False, blank=False)
    added = models.DateTimeField(auto_now_add=True)
    screen = models.ManyToManyField(Screen)
    objects = MovieManager()

    def get_absolute_url(self):
        return reverse('movie:detail', kwargs={'movie_id': self.pk})

    def __str__(self):
        return self.moviename

class Show(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    screen = models.ForeignKey(Screen, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()

    def __str__(self):
        return str(self.movie)+" : "+str(self.screen)+"-"+str(self.date)+"-"+str(self.time)


class Seat(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    show = models.ForeignKey(Show, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    screen = models.ForeignKey(Screen, on_delete=models.CASCADE)
    seat_no = models.IntegerField()

    def __str__(self):
        return str(self.id)


class Booking(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    transaction_id = models.UUIDField(unique=True, editable=False,
                                      default=uuid.uuid4)
    timestamp = models.DateTimeField(auto_now=True, auto_now_add=False)
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    show = models.ForeignKey(Show, on_delete=models.CASCADE)
    paid_amount = models.DecimalField(max_digits=8, decimal_places=2)
    paid_by = models.ForeignKey(User, on_delete=models.DO_NOTHING)

    def __str__(self):
        return str("Booking ID # "+str(self.transaction_id))

    def get_absolute_url(self):
        return reverse('booking:detail', kwargs={'btid': self.id})

    @property
    def cancel_time(self):
        d = datetime.now()+timedelta(days=1)
        dd = datetime.strptime(str(self.show.date)+" "+str(
            self.show.time), '%Y-%m-%d %H:%M:%S')
        return d > dd
