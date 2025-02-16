# from django.contrib import admin
# from .models import Car, Availability, Booking, Cancellation, Reservation

# @admin.register(Car)
# class CarAdmin(admin.ModelAdmin):
#     list_display = ('name', 'model', 'price', 'status')

# @admin.register(Availability)
# class AvailableAdmin(admin.ModelAdmin):
#     list_display = ('car', 'date', 'is_available')

# @admin.register(Booking)
# class BookingAdmin(admin.ModelAdmin):
#     list_display = ('user', 'car', 'start_date', 'end_date', 'status')
#     list_filter = ('status',)

# @admin.register(Cancellation)
# class CancelAdmin(admin.ModelAdmin):
#     list_display = ('booking', 'cancel_date', 'reason')

# @admin.register(Reservation)
# class RegisterAdmin(admin.ModelAdmin):
#     list_display = ('user')