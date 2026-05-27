from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.utils import timezone
from core.models import ClassSchedule
from .models import Booking
import datetime
import json


@login_required
def book_class(request, schedule_id):
    schedule = get_object_or_404(ClassSchedule, id=schedule_id, is_active=True)

    if request.method == 'POST':
        booking_date_str = request.POST.get('booking_date')
        try:
            booking_date = datetime.date.fromisoformat(booking_date_str)
        except (ValueError, TypeError):
            messages.error(request, 'Invalid date selected.')
            return redirect('core:schedule')

        if booking_date < datetime.date.today():
            messages.error(request, 'Cannot book a class in the past.')
            return redirect('core:schedule')

        # Check if already booked
        existing = Booking.objects.filter(user=request.user, schedule=schedule, booking_date=booking_date).first()
        if existing:
            messages.warning(request, f'You already have a booking for {schedule.gym_class.name} on {booking_date}.')
            return redirect('accounts:profile')

        # Check capacity
        confirmed_count = schedule.bookings.filter(status='confirmed', booking_date=booking_date).count()
        if confirmed_count >= schedule.gym_class.max_capacity:
            booking = Booking.objects.create(
                user=request.user, schedule=schedule,
                booking_date=booking_date, status='waitlisted'
            )
            messages.info(request, f'Class is full! You\'ve been added to the waitlist for {schedule.gym_class.name}.')
        else:
            booking = Booking.objects.create(
                user=request.user, schedule=schedule,
                booking_date=booking_date, status='confirmed'
            )
            messages.success(request, f'Successfully booked {schedule.gym_class.name} for {booking_date.strftime("%B %d, %Y")}!')

        return redirect('accounts:profile')

    # GET - show booking form
    # Get next occurrence dates for this day of week
    today = datetime.date.today()
    upcoming_dates = []
    for i in range(28):  # next 4 weeks
        check_date = today + datetime.timedelta(days=i)
        if check_date.weekday() == schedule.day_of_week:
            upcoming_dates.append(check_date)

    context = {
        'schedule': schedule,
        'upcoming_dates': upcoming_dates,
        'meta_title': f'Book {schedule.gym_class.name} | IronForge Gym',
    }
    return render(request, 'bookings/book_class.html', context)


@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    if booking.status == 'confirmed' and booking.is_upcoming:
        booking.status = 'cancelled'
        booking.save()
        messages.success(request, f'Booking for {booking.schedule.gym_class.name} has been cancelled.')
    else:
        messages.error(request, 'This booking cannot be cancelled.')
    return redirect('accounts:profile')


@login_required
def my_bookings(request):
    upcoming = Booking.objects.filter(
        user=request.user,
        booking_date__gte=datetime.date.today(),
        status__in=['confirmed', 'waitlisted']
    ).select_related('schedule__gym_class', 'schedule__gym_class__trainer').order_by('booking_date')

    past = Booking.objects.filter(
        user=request.user,
        booking_date__lt=datetime.date.today()
    ).select_related('schedule__gym_class').order_by('-booking_date')[:20]

    context = {
        'upcoming_bookings': upcoming,
        'past_bookings': past,
        'meta_title': 'My Bookings | IronForge Gym',
    }
    return render(request, 'bookings/my_bookings.html', context)
