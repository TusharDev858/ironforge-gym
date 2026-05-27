from django.db import models
from django.contrib.auth.models import User
from core.models import ClassSchedule
import datetime


class Booking(models.Model):
    STATUS_CHOICES = [
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('waitlisted', 'Waitlisted'),
        ('attended', 'Attended'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    schedule = models.ForeignKey(ClassSchedule, on_delete=models.CASCADE, related_name='bookings')
    booking_date = models.DateField(help_text="The specific date for this booking")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='confirmed')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ['user', 'schedule', 'booking_date']

    def __str__(self):
        return f"{self.user.username} - {self.schedule.gym_class.name} ({self.booking_date})"

    @property
    def is_upcoming(self):
        return self.booking_date >= datetime.date.today()
