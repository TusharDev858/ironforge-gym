from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib import messages
from django import forms as django_forms
from .models import (
    Trainer, GymClass, ClassSchedule, Exercise,
    GalleryImage, Testimonial, MembershipPlan, ContactMessage
)


# --------------- Contact Form (defined here, no separate forms.py needed) ---------------

class ContactForm(django_forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'phone', 'subject', 'message']
        widgets = {
            'name':    django_forms.TextInput(attrs={'placeholder': 'Your full name'}),
            'email':   django_forms.EmailInput(attrs={'placeholder': 'your@email.com'}),
            'phone':   django_forms.TextInput(attrs={'placeholder': '+1 (555) 000-0000 (optional)'}),
            'message': django_forms.Textarea(attrs={'rows': 5, 'placeholder': 'How can we help you?'}),
        }


# --------------- Views ---------------

def home(request):
    context = {
        'trainers': Trainer.objects.filter(is_active=True)[:4],
        'featured_classes': GymClass.objects.filter(is_active=True)[:6],
        'testimonials': Testimonial.objects.filter(is_featured=True)[:6],
        'membership_plans': MembershipPlan.objects.filter(is_active=True),
        'gallery_featured': GalleryImage.objects.filter(is_featured=True)[:8],
        'total_members': 2847,
        'total_classes': GymClass.objects.filter(is_active=True).count(),
        'total_trainers': Trainer.objects.filter(is_active=True).count(),
        'meta_title': 'IronForge Gym | Transform Your Body, Forge Your Strength',
        'meta_description': 'Premium gym with world-class trainers, cutting-edge equipment, and diverse class schedules. Join IronForge today and start your transformation.',
    }
    return render(request, 'core/home.html', context)


def classes(request):
    category_filter = request.GET.get('category', '')
    difficulty_filter = request.GET.get('difficulty', '')
    all_classes = GymClass.objects.filter(is_active=True).select_related('trainer')
    if category_filter:
        all_classes = all_classes.filter(category=category_filter)
    if difficulty_filter:
        all_classes = all_classes.filter(difficulty=difficulty_filter)
    context = {
        'classes': all_classes,
        'category_choices': GymClass.CATEGORY_CHOICES,
        'difficulty_choices': GymClass.DIFFICULTY_CHOICES,
        'selected_category': category_filter,
        'selected_difficulty': difficulty_filter,
        'meta_title': 'Gym Classes | IronForge Gym',
        'meta_description': 'Explore our diverse range of fitness classes including HIIT, Yoga, Strength Training, Boxing, and more.',
    }
    return render(request, 'core/classes.html', context)


def schedule(request):
    schedules_by_day = {}
    day_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    for i, day in enumerate(day_names):
        schedules_by_day[day] = ClassSchedule.objects.filter(
            day_of_week=i, is_active=True
        ).select_related('gym_class', 'gym_class__trainer')
    context = {
        'schedules_by_day': schedules_by_day,
        'day_names': day_names,
        'meta_title': 'Class Schedule | IronForge Gym',
        'meta_description': 'View our weekly class schedule and book your spot in any class.',
    }
    return render(request, 'core/schedule.html', context)


def trainers(request):
    context = {
        'trainers': Trainer.objects.filter(is_active=True),
        'meta_title': 'Our Trainers | IronForge Gym',
        'meta_description': 'Meet our world-class team of certified personal trainers and fitness coaches.',
    }
    return render(request, 'core/trainers.html', context)


def trainer_detail(request, slug):
    trainer = get_object_or_404(Trainer, slug=slug, is_active=True)
    context = {
        'trainer': trainer,
        'trainer_classes': trainer.classes.filter(is_active=True),
        'meta_title': f'{trainer.name} | IronForge Gym Trainer',
        'meta_description': trainer.bio[:160],
    }
    return render(request, 'core/trainer_detail.html', context)


def exercises(request):
    muscle_filter = request.GET.get('muscle', '')
    equipment_filter = request.GET.get('equipment', '')
    difficulty_filter = request.GET.get('difficulty', '')
    all_exercises = Exercise.objects.all()
    if muscle_filter:
        all_exercises = all_exercises.filter(muscle_group=muscle_filter)
    if equipment_filter:
        all_exercises = all_exercises.filter(equipment=equipment_filter)
    if difficulty_filter:
        all_exercises = all_exercises.filter(difficulty=difficulty_filter)
    context = {
        'exercises': all_exercises,
        'muscle_choices': Exercise.MUSCLE_GROUP_CHOICES,
        'equipment_choices': Exercise.EQUIPMENT_CHOICES,
        'difficulty_choices': GymClass.DIFFICULTY_CHOICES,
        'selected_muscle': muscle_filter,
        'selected_equipment': equipment_filter,
        'selected_difficulty': difficulty_filter,
        'meta_title': 'Exercise Library | IronForge Gym',
        'meta_description': 'Browse our comprehensive exercise library with instructions, tips, and videos.',
    }
    return render(request, 'core/exercises.html', context)


def gallery(request):
    category_filter = request.GET.get('category', '')
    images = GalleryImage.objects.all()
    if category_filter:
        images = images.filter(category=category_filter)
    context = {
        'images': images,
        'category_choices': GalleryImage.CATEGORY_CHOICES,
        'selected_category': category_filter,
        'meta_title': 'Gallery | IronForge Gym',
        'meta_description': 'Take a virtual tour of IronForge Gym - world-class facilities and equipment.',
    }
    return render(request, 'core/gallery.html', context)


def about(request):
    context = {
        'trainers': Trainer.objects.filter(is_active=True)[:4],
        'meta_title': 'About Us | IronForge Gym',
        'meta_description': "Learn about IronForge Gym's mission, values, and the team behind your transformation.",
    }
    return render(request, 'core/about.html', context)


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Thanks for reaching out! We'll get back to you within 24 hours."
            )
            return redirect('core:contact')
        else:
            messages.error(request, "Please correct the errors below and try again.")
    else:
        form = ContactForm()

    context = {
        'form': form,
        'meta_title': 'Contact Us | IronForge Gym',
        'meta_description': 'Get in touch with IronForge Gym — we\'d love to hear from you.',
    }
    return render(request, 'core/contact.html', context)
