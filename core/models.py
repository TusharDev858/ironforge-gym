from django.db import models
from django.utils.text import slugify


class Trainer(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    specialty = models.CharField(max_length=200)
    bio = models.TextField()
    photo = models.ImageField(upload_to='trainers/', blank=True, null=True)
    experience_years = models.PositiveIntegerField(default=1)
    certifications = models.TextField(blank=True, help_text="Comma-separated certifications")
    instagram = models.URLField(blank=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order', 'name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_certifications_list(self):
        return [c.strip() for c in self.certifications.split(',') if c.strip()]


class GymClass(models.Model):
    DIFFICULTY_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
        ('all', 'All Levels'),
    ]
    CATEGORY_CHOICES = [
        ('strength', 'Strength Training'),
        ('cardio', 'Cardio'),
        ('yoga', 'Yoga & Flexibility'),
        ('hiit', 'HIIT'),
        ('pilates', 'Pilates'),
        ('boxing', 'Boxing'),
        ('spin', 'Spin / Cycling'),
        ('crossfit', 'CrossFit'),
    ]

    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='strength')
    description = models.TextField()
    trainer = models.ForeignKey(Trainer, on_delete=models.SET_NULL, null=True, related_name='classes')
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES, default='all')
    duration_minutes = models.PositiveIntegerField(default=60)
    max_capacity = models.PositiveIntegerField(default=20)
    image = models.ImageField(upload_to='classes/', blank=True, null=True)
    icon = models.CharField(max_length=50, default='🏋️', help_text="Emoji icon for the class")
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Gym Class'
        verbose_name_plural = 'Gym Classes'
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


DAYS_OF_WEEK = [
    (0, 'Monday'), (1, 'Tuesday'), (2, 'Wednesday'),
    (3, 'Thursday'), (4, 'Friday'), (5, 'Saturday'), (6, 'Sunday'),
]


class ClassSchedule(models.Model):
    gym_class = models.ForeignKey(GymClass, on_delete=models.CASCADE, related_name='schedules')
    day_of_week = models.IntegerField(choices=DAYS_OF_WEEK)
    start_time = models.TimeField()
    end_time = models.TimeField()
    room = models.CharField(max_length=50, default='Main Floor')
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['day_of_week', 'start_time']

    def __str__(self):
        return f"{self.gym_class.name} - {self.get_day_of_week_display()} {self.start_time}"

    @property
    def available_spots(self):
        from bookings.models import Booking
        booked = self.bookings.filter(status='confirmed').count()
        return self.gym_class.max_capacity - booked


class Exercise(models.Model):
    MUSCLE_GROUP_CHOICES = [
        ('chest', 'Chest'), ('back', 'Back'), ('shoulders', 'Shoulders'),
        ('arms', 'Arms'), ('core', 'Core'), ('legs', 'Legs'),
        ('glutes', 'Glutes'), ('full_body', 'Full Body'), ('cardio', 'Cardio'),
    ]
    EQUIPMENT_CHOICES = [
        ('barbell', 'Barbell'), ('dumbbell', 'Dumbbell'), ('cable', 'Cable Machine'),
        ('machine', 'Machine'), ('bodyweight', 'Bodyweight'), ('kettlebell', 'Kettlebell'),
        ('resistance_band', 'Resistance Band'), ('pull_up_bar', 'Pull-Up Bar'),
    ]

    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    muscle_group = models.CharField(max_length=20, choices=MUSCLE_GROUP_CHOICES)
    equipment = models.CharField(max_length=20, choices=EQUIPMENT_CHOICES, default='bodyweight')
    description = models.TextField()
    instructions = models.TextField(help_text="Step-by-step instructions")
    sets_reps = models.CharField(max_length=100, default='3 sets x 10 reps')
    difficulty = models.CharField(max_length=20, choices=GymClass.DIFFICULTY_CHOICES, default='beginner')
    image = models.ImageField(upload_to='exercises/', blank=True, null=True)
    video_url = models.URLField(blank=True, help_text="YouTube embed URL")
    calories_per_hour = models.PositiveIntegerField(default=300)
    is_featured = models.BooleanField(default=False)

    class Meta:
        ordering = ['muscle_group', 'name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class GalleryImage(models.Model):
    CATEGORY_CHOICES = [
        ('facility', 'Facility'), ('equipment', 'Equipment'),
        ('classes', 'Classes'), ('events', 'Events'),
    ]
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='gallery/')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='facility')
    order = models.PositiveIntegerField(default=0)
    is_featured = models.BooleanField(default=False)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title


class Testimonial(models.Model):
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100, default='Member')
    content = models.TextField()
    rating = models.PositiveIntegerField(default=5)
    photo = models.ImageField(upload_to='testimonials/', blank=True, null=True)
    is_featured = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.rating}★"


class MembershipPlan(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    billing_period = models.CharField(max_length=20, default='month')
    features = models.TextField(help_text="One feature per line")
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'price']

    def __str__(self):
        return self.name

    def get_features_list(self):
        return [f.strip() for f in self.features.split('\n') if f.strip()]


class ContactMessage(models.Model):
    SUBJECT_CHOICES = [
        ('membership', 'Membership Enquiry'),
        ('classes', 'Classes & Schedule'),
        ('personal_training', 'Personal Training'),
        ('facilities', 'Facilities & Equipment'),
        ('other', 'Other'),
    ]

    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    subject = models.CharField(max_length=30, choices=SUBJECT_CHOICES, default='other')
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    replied = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Contact Message'
        verbose_name_plural = 'Contact Messages'

    def __str__(self):
        return f"{self.name} — {self.get_subject_display()} ({self.created_at.strftime('%d %b %Y')})"
