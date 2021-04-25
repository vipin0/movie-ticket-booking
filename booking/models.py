# import uuid
# from django.contrib.auth import get_user_model
# from django.db import models
# from django.urls import reverse
# User = get_user_model()
# # Create your models here.


# class Screen(models.Model):
#     name = models.CharField(max_length=20)
#     seats = models.IntegerField(default=10)

#     def __str__(self) -> str:
#         return str("Screen : "+self.name)

# class Seat(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     # show = models.ForeignKey(Show, on_delete=models.CASCADE)
#     screen = models.ForeignKey(Screen, on_delete=models.CASCADE)
#     seat_no = models.IntegerField()

#     def __str__(self):
#         return str(self.id)

# class Booking(models.Model):
#     id = models.CharField(max_length=255, primary_key=True)
#     transaction_id = models.UUIDField(unique=True, editable=False,
#                                       default=uuid.uuid4)
#     timestamp = models.DateTimeField(auto_now=True, auto_now_add=False)
#     seat = models.ForeignKey(Seat, on_delete=models.CASCADE)
#     paid_amount = models.DecimalField(max_digits=8, decimal_places=2)
#     paid_by = models.ForeignKey(User, on_delete=models.DO_NOTHING)

#     def __str__(self):
#         return str("Booking ID # "+str(self.transaction_id))

#     def get_absolute_url(self):
#         return reverse('booking:detail', kwargs={'btid': self.id})


