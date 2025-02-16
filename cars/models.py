from django.db import models

from user.models import User
from datetime import time

class Car(models.Model):
    name = models.CharField(max_length=255)
    description=models.CharField(max_length=255)
    fuel = models.CharField(max_length=50)
    seats = models.IntegerField()
    rating = models.DecimalField(max_digits=2, decimal_places=1)
    amount = models.IntegerField()
    image = models.ImageField(upload_to='cars/', blank=True, null=True)  

    def __str__(self):
        return self.name

class Booking(models.Model):
     STATUS_CHOICES = [
        ('active', 'Active'),
        ('canceled', 'Canceled'),
     ]
     booking_id = models.AutoField(primary_key=True)
     user = models.ForeignKey(User, on_delete=models.CASCADE)
     car = models.ForeignKey(Car, on_delete=models.CASCADE)
     booking_date = models.DateField()
     pickup_date = models.DateField()
     return_date = models.DateField()
     pickup_time = models.TimeField(default=time(9, 0))  
     drop_time = models.TimeField(default=time(17, 0))   
     destination = models.CharField(max_length=255)
     total_price = models.FloatField()

     status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')

     def __str__(self):
        return f"Booking {self.booking_id} - {self.status}"



class Cancellation(models.Model):
    cancellation_id = models.AutoField(primary_key=True)
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    cancellation_date = models.DateField()
    reason = models.TextField()

    def __str__(self):
        return f"Cancellation {self.cancellation_id} for Booking {self.booking.booking_id}"

class Availability(models.Model):
    car = models.OneToOneField(Car, on_delete=models.CASCADE, primary_key=True)
    pickup_date = models.DateField()
    return_date = models.DateField()
    available_quantity = models.IntegerField()


class contact(models.Model):
    name=models.CharField(max_length=25)
    email=models.EmailField()
    phone=models.IntegerField()
    text=models.TextField()