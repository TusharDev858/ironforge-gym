from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    GOAL_CHOICES = [
        ('weight_loss', 'Weight Loss'),
        ('muscle_gain', 'Muscle Gain'),
        ('endurance', 'Build Endurance'),
        ('flexibility', 'Improve Flexibility'),
        ('general_fitness', 'General Fitness'),
        ('athletic_performance', 'Athletic Performance'),
        ('rehabilitation', 'Rehabilitation'),
        ('stress_relief', 'Stress Relief'),
    ]
    ACTIVITY_CHOICES = [
        ('sedentary', 'Sedentary (little/no exercise)'),
        ('lightly_active', 'Lightly Active (1-3 days/week)'),
        ('moderately_active', 'Moderately Active (3-5 days/week)'),
        ('very_active', 'Very Active (6-7 days/week)'),
        ('extra_active', 'Extra Active (twice a day)'),
    ]
    EXPERIENCE_CHOICES = [
        ('beginner', 'Beginner (< 1 year)'),
        ('intermediate', 'Intermediate (1-3 years)'),
        ('advanced', 'Advanced (3+ years)'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    date_of_birth = models.DateField(null=True, blank=True)
    phone = models.CharField(max_length=20, blank=True)

    # Body stats
    height_cm = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True)
    weight_kg = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True)
    body_fat_percentage = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True)

    # Fitness info
    fitness_goal = models.CharField(max_length=30, choices=GOAL_CHOICES, default='general_fitness')
    activity_level = models.CharField(max_length=20, choices=ACTIVITY_CHOICES, default='sedentary')
    experience_level = models.CharField(max_length=20, choices=EXPERIENCE_CHOICES, default='beginner')
    health_conditions = models.TextField(blank=True, help_text="Any health conditions or injuries")
    emergency_contact = models.CharField(max_length=100, blank=True)
    emergency_phone = models.CharField(max_length=20, blank=True)

    # Membership
    membership_start = models.DateField(null=True, blank=True)
    membership_end = models.DateField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

    @property
    def bmi(self):
        if self.height_cm and self.weight_kg:
            h = float(self.height_cm) / 100
            return round(float(self.weight_kg) / (h ** 2), 1)
        return None

    @property
    def bmi_category(self):
        bmi = self.bmi
        if bmi is None:
            return None
        if bmi < 18.5:
            return 'Underweight'
        elif bmi < 25:
            return 'Normal weight'
        elif bmi < 30:
            return 'Overweight'
        else:
            return 'Obese'
