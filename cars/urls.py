from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'cars', CarViewSet)
router.register(r'availability', AvailabilityViewset)
router.register(r'booking', BookingViewSet)
router.register(r'cancel', CancellationViewSet)
router.register(r'contact', ContactsViewset)


urlpatterns = [
    path('', include(router.urls)),
]