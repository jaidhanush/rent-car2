# from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import *
from rest_framework import viewsets
from rest_framework.decorators import action
from datetime import date, datetime, timedelta
from rest_framework.parsers import MultiPartParser, FormParser

class CarViewSet(viewsets.ModelViewSet):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    parser_classes = (MultiPartParser, FormParser)



class AvailabilityViewset(viewsets.ModelViewSet):
     queryset = Availability.objects.all()
     serializer_class = AvailabilitySerializer


class ContactsViewset(viewsets.ModelViewSet):
     queryset = contact.objects.all()
     serializer_class = ContactSerializer



from datetime import datetime, timedelta
from django.conf import settings
from django.core.mail import send_mail
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Booking, Car, Availability
from .serializers import BookingSerializer

class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
  
    def create(self, request, *args, **kwargs):
        car_id = request.data.get('car')
        pickup_date = request.data.get('pickup_date')
        return_date = request.data.get('return_date')
        pickup_time = request.data.get('pickup_time')
        drop_time = request.data.get('drop_time')
        destination = request.data.get('destination')
        
        try:
            car = Car.objects.get(pk=car_id)
        except Car.DoesNotExist:
            return Response({"error": "Car not found"}, status=status.HTTP_404_NOT_FOUND)

        # Convert date and time strings to objects
        try:
            pickup_date = datetime.strptime(pickup_date, '%Y-%m-%d').date()
            return_date = datetime.strptime(return_date, '%Y-%m-%d').date()
            pickup_time = datetime.strptime(pickup_time, '%H:%M').time()
            drop_time = datetime.strptime(drop_time, '%H:%M').time()
        except ValueError:
            return Response({"error": "Invalid date or time format"}, status=status.HTTP_400_BAD_REQUEST)

        # Check for overlapping bookings
        overlapping_bookings = Booking.objects.filter(
            car=car,
            status='active',
            pickup_date__lt=return_date + timedelta(days=1),
            return_date__gt=pickup_date - timedelta(days=1)
        )

        if overlapping_bookings.exists():
            return Response({"error": "Car is already booked for the selected dates"}, status=status.HTTP_400_BAD_REQUEST)

        # Proceed with booking creation
        response = super().create(request, *args, **kwargs)

        # Ensure only one availability record per car
        availability, created = Availability.objects.get_or_create(
            car=car,
            defaults={'pickup_date': pickup_date, 'return_date': return_date, 'available_quantity': 0}
        )

        # If the availability record already exists, update the dates
        if not created:
            availability.pickup_date = pickup_date
            availability.return_date = return_date
            availability.available_quantity = 0  # Adjust logic if needed
            availability.save()

        # Send confirmation email
        user = request.user  
        user_email = user.email  

        subject = "Booking Confirmation"
        message = f"""
        Dear {user.username},

        Your booking for {car.name} has been confirmed!

        Booking Details:
        - Car: {car.name}
        - Pickup Date: {pickup_date}
        - Return Date: {return_date}
        - Pickup Time: {pickup_time}
        - Drop Time: {drop_time}
        - Destination: {destination}

        Thank you for choosing our service!

        Regards,
        Car Rental Team
        """

        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,  
            [user_email],  
            fail_silently=False,
        )

        return response

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if 'status' in request.data and request.data['status'] == 'canceled':
            car = instance.car

            active_bookings = Booking.objects.filter(
                car=car,
                status='active',
                pickup_date__lt=instance.return_date + timedelta(days=1),
                return_date__gt=instance.pickup_date - timedelta(days=1)
            )

            if not active_bookings.exists():
                car.is_available = True
                car.save()

            availability_record, created = Availability.objects.get_or_create(
                car=car,
                defaults={'pickup_date': instance.pickup_date, 'return_date': instance.return_date, 'available_quantity': 1}
            )

            # If the record exists, update it
            if not created:
                availability_record.pickup_date = instance.pickup_date
                availability_record.return_date = instance.return_date
                availability_record.available_quantity = 1  # Adjust logic if needed
                availability_record.save()

        return Response(serializer.data)



class CancellationViewSet(viewsets.ModelViewSet):
    queryset = Cancellation.objects.all()
    serializer_class = CancellationSerializer


    def create(self, request, *args, **kwargs):
        booking_id = request.data.get('booking')

        # Validate booking existence and status
        try:
            booking = Booking.objects.get(pk=booking_id, status='active')
        except Booking.DoesNotExist:
            return Response({"error": "Booking not found or already canceled"}, status=status.HTTP_404_NOT_FOUND)

        # Proceed with the cancellation record creation
        response = super().create(request, *args, **kwargs)

        # Update the booking status to 'canceled'
        booking.status = 'canceled'
        booking.save()

        # Set the car's availability to 'True' (available)
        car = booking.car
        car.is_available = True
        car.save()

        # Update the availability record (or create if not exists)
        availability_record, created = Availability.objects.get_or_create(
            car=car,
            pickup_date=booking.pickup_date,
            return_date=booking.return_date,
        )

        if not created:
            # If record exists, update available quantity
            availability_record.available_quantity = 1
            availability_record.save()

        return response


