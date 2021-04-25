from django import forms
from movie.models import Booking, Seat


class SeatForm(forms.ModelForm):
    class Meta:
        model = Seat
        fields = ('screen',)


class BookingForm(forms.ModelForm):

    class Meta:
        model = Booking
        fields = '__all__'
