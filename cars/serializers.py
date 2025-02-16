from rest_framework import serializers
from .models import *

class CarSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True)

    class Meta:
        model = Car
        fields = '__all__'

class ContactSerializer(serializers.ModelSerializer):

     class Meta:
        model = contact
        fields = '__all__'


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'



class CancellationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cancellation
        fields = '__all__'

class AvailabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Availability
        fields = '__all__'