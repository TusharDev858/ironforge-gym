from django.contrib import admin
from .models import Booking


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['user', 'schedule', 'booking_date', 'status', 'created_at']
    list_editable = ['status']
    list_filter = ['status', 'booking_date', 'schedule__gym_class']
    search_fields = ['user__username', 'user__email', 'schedule__gym_class__name']
    date_hierarchy = 'booking_date'
    raw_id_fields = ['user']
