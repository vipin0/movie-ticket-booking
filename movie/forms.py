from django import forms
from django.db.models import fields
from django.forms.widgets import TimeInput
from .models import Movie
from .models import Show


class DateTimeInput(forms.DateTimeInput):
    input_type = 'date'


class TimInput(forms.TimeInput):
    input_type = 'time'


class MovieForm(forms.ModelForm):
    moviename = forms.CharField(max_length=255, required=True)
    poster = forms.FileField(required=True)
    ticket_price = forms.FloatField(required=True)

    class Meta:
        model = Movie
        fields = '__all__'


class ShowForm(forms.ModelForm):
    date = forms.DateField(
        widget=DateTimeInput()
    )
    time = forms.TimeField(
        widget=TimeInput()
    )

    class Meta:
        model = Show
        fields = '__all__'
