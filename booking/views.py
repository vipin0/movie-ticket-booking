from django.shortcuts import render, get_object_or_404
from movie.models import Movie, Show, Screen, Show, Seat, Booking
from .forms import SeatForm, BookingForm
from django.urls import reverse_lazy
import datetime
from django.views.generic import ListView, DetailView, DeleteView
from django.shortcuts import redirect
from django.http.response import Http404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from datetime import datetime, timedelta

# Create your views here.


@login_required
def reserve_seat(request, show_id):
    template_name = 'booking/reserve_seat.html'
    try:
        show_info = Show.objects.get(pk=show_id)
        # print("show", show_info.screen)
    except Show.DoesNotExist:
        raise Http404("Page does not exist")
    form = SeatForm()
    movie = show_info.movie
    # print(movie)
    screen = show_info.screen
    price = movie.ticket_price
    # print(price)
    booked = Booking.objects.filter(movie=movie, show=show_info)
    booked_seats = []
    for i in booked:
        booked_seats.append(i.seat.seat_no)
    not_booked = [int(i) for i in range(1, 11) if i not in booked_seats]
    print(not_booked)
    if request.method == 'POST':
        form = SeatForm(request.POST)
        sno = request.POST.get('seat_no')
        print(sno)
        if form.is_valid() and sno != None:
            new_seat = form.save(commit=False)
            new_seat.user = request.user
            new_seat.movie = movie
            new_seat.show = show_info
            new_seat.seat_no = sno
            # print(request.user.id)
            new_seat.save()
            form = Booking()
            form.seat = new_seat
            form.movie = movie
            form.show = show_info
            form.id = form.transaction_id
            form.paid_by = request.user
            form.paid_amount = price
            form.seat = new_seat
            form.save()
            return redirect('/booking/')
    else:
        return render(request, template_name,
                      {'show_info': show_info, 'form': form, 'not_booked': not_booked})


@method_decorator(login_required, name='dispatch')
class BookingListView(ListView):
    template_name = 'booking/booking_list.html'

    def get_queryset(self):
        return Booking.objects.filter(paid_by=self.request.user)

@login_required
def detailBookingView(request, btid):
    template_name = 'booking/booking_detail.html'
    obj = get_object_or_404(Booking, id=btid, paid_by=request.user)
    # print(obj)
    print(obj.show)
    d = datetime.strptime((datetime.now()+timedelta(days=1)
                           ).strftime("%Y-%m-%d %H:%M:%S"), '%Y-%m-%d %H:%M:%S')
    dd = datetime.strptime(str(obj.show.date)+" "+str(
        obj.show.time), '%Y-%m-%d %H:%M:%S')
    # print(type(d))
    # print(type(dd))
    can_be_canceled = True if d < dd else False
    # print(can_be_canceled)

    return render(request, template_name, {"object": obj, "cancel": can_be_canceled})


@method_decorator(login_required, name='dispatch')
class BookingDeleteView(DeleteView):
    template_name = 'booking/booking_confirm_delete.html'
    model = Booking
    success_url = reverse_lazy('booking:list')

    def get_object(self, *args, **kwargs):
        btid = self.kwargs.get('btid')
        obj = get_object_or_404(Booking, id=btid)
        return obj
