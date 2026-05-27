from django.urls import path
from . import views

app_name = 'bookings'

urlpatterns = [
    path('book/<int:schedule_id>/', views.book_class, name='book_class'),
    path('cancel/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
]
