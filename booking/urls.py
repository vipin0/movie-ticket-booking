from django.urls import path
from .views import detailBookingView, reserve_seat, BookingListView, BookingDeleteView
app_name = 'booking'
urlpatterns = [
    path('select-seat/<int:show_id>/', reserve_seat, name='reserve_seat'),
    path('booking/', BookingListView.as_view(), name='list'),
    path('booking/<str:btid>/delete/',
         BookingDeleteView.as_view(), name='delete'),
    path('booking/<str:btid>/', detailBookingView, name='detail'),
]
