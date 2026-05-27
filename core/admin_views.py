from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.utils.text import slugify
from django import forms as django_forms
from django.forms import inlineformset_factory
from django.db.models import Count, Q
import datetime

from .models import (
    Trainer, GymClass, ClassSchedule, Exercise,
    GalleryImage, Testimonial, MembershipPlan, ContactMessage, DAYS_OF_WEEK
)

# ─────────────────────────────────────────
# FORMS
# ─────────────────────────────────────────

class TrainerForm(django_forms.ModelForm):
    class Meta:
        model = Trainer
        fields = ['name', 'specialty', 'bio', 'photo', 'experience_years',
                  'certifications', 'instagram', 'order', 'is_active']
        widgets = {
            'bio': django_forms.Textarea(attrs={'rows': 4}),
            'certifications': django_forms.TextInput(attrs={'placeholder': 'NSCA-CSCS, CPR, ...'}),
        }


class GymClassForm(django_forms.ModelForm):
    class Meta:
        model = GymClass
        fields = ['name', 'category', 'description', 'trainer', 'difficulty',
                  'duration_minutes', 'max_capacity', 'image', 'icon', 'is_active']
        widgets = {
            'description': django_forms.Textarea(attrs={'rows': 4}),
        }


class ClassScheduleForm(django_forms.ModelForm):
    class Meta:
        model = ClassSchedule
        fields = ['gym_class', 'day_of_week', 'start_time', 'end_time', 'room', 'is_active']
        widgets = {
            'start_time': django_forms.TimeInput(attrs={'type': 'time'}),
            'end_time':   django_forms.TimeInput(attrs={'type': 'time'}),
        }


class ExerciseForm(django_forms.ModelForm):
    class Meta:
        model = Exercise
        fields = ['name', 'muscle_group', 'equipment', 'description', 'instructions',
                  'sets_reps', 'difficulty', 'image', 'video_url', 'calories_per_hour', 'is_featured']
        widgets = {
            'description':  django_forms.Textarea(attrs={'rows': 3}),
            'instructions': django_forms.Textarea(attrs={'rows': 5}),
        }


class GalleryImageForm(django_forms.ModelForm):
    class Meta:
        model = GalleryImage
        fields = ['title', 'image', 'category', 'order', 'is_featured']


class TestimonialForm(django_forms.ModelForm):
    class Meta:
        model = Testimonial
        fields = ['name', 'role', 'content', 'rating', 'photo', 'is_featured']
        widgets = {
            'content': django_forms.Textarea(attrs={'rows': 4}),
            'rating':  django_forms.NumberInput(attrs={'min': 1, 'max': 5}),
        }


class MembershipPlanForm(django_forms.ModelForm):
    class Meta:
        model = MembershipPlan
        fields = ['name', 'price', 'billing_period', 'features', 'is_featured', 'is_active', 'order']
        widgets = {
            'features': django_forms.Textarea(attrs={'rows': 6, 'placeholder': 'One feature per line'}),
        }


# ─────────────────────────────────────────
# DASHBOARD
# ─────────────────────────────────────────

@staff_member_required(login_url='/accounts/login/')
def dashboard(request):
    unread_messages = ContactMessage.objects.filter(is_read=False).count()
    context = {
        'total_trainers':  Trainer.objects.filter(is_active=True).count(),
        'total_classes':   GymClass.objects.filter(is_active=True).count(),
        'total_schedules': ClassSchedule.objects.filter(is_active=True).count(),
        'total_exercises': Exercise.objects.count(),
        'total_gallery':   GalleryImage.objects.count(),
        'total_plans':     MembershipPlan.objects.filter(is_active=True).count(),
        'total_testimonials': Testimonial.objects.filter(is_featured=True).count(),
        'unread_messages': unread_messages,
        'recent_messages': ContactMessage.objects.all()[:5],
        'meta_title': 'Admin Dashboard | IronForge Gym',
    }
    return render(request, 'admin_panel/dashboard.html', context)


# ─────────────────────────────────────────
# TRAINERS
# ─────────────────────────────────────────

@staff_member_required(login_url='/accounts/login/')
def trainer_list(request):
    trainers = Trainer.objects.all()
    return render(request, 'admin_panel/trainer_list.html', {
        'trainers': trainers, 'meta_title': 'Manage Trainers'
    })

@staff_member_required(login_url='/accounts/login/')
def trainer_create(request):
    form = TrainerForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.slug = slugify(obj.name)
        obj.save()
        messages.success(request, f'Trainer "{obj.name}" created successfully.')
        return redirect('admin_panel:trainer_list')
    return render(request, 'admin_panel/form.html', {
        'form': form, 'title': 'Add Trainer', 'back_url': 'admin_panel:trainer_list'
    })

@staff_member_required(login_url='/accounts/login/')
def trainer_edit(request, pk):
    obj = get_object_or_404(Trainer, pk=pk)
    form = TrainerForm(request.POST or None, request.FILES or None, instance=obj)
    if form.is_valid():
        form.save()
        messages.success(request, f'Trainer "{obj.name}" updated.')
        return redirect('admin_panel:trainer_list')
    return render(request, 'admin_panel/form.html', {
        'form': form, 'title': f'Edit Trainer — {obj.name}',
        'back_url': 'admin_panel:trainer_list', 'obj': obj
    })

@staff_member_required(login_url='/accounts/login/')
def trainer_delete(request, pk):
    obj = get_object_or_404(Trainer, pk=pk)
    if request.method == 'POST':
        name = obj.name
        obj.delete()
        messages.success(request, f'Trainer "{name}" deleted.')
        return redirect('admin_panel:trainer_list')
    return render(request, 'admin_panel/confirm_delete.html', {
        'obj': obj, 'obj_type': 'Trainer', 'back_url': 'admin_panel:trainer_list'
    })


# ─────────────────────────────────────────
# CLASSES
# ─────────────────────────────────────────

@staff_member_required(login_url='/accounts/login/')
def class_list(request):
    classes = GymClass.objects.select_related('trainer').all()
    return render(request, 'admin_panel/class_list.html', {
        'classes': classes, 'meta_title': 'Manage Classes'
    })

@staff_member_required(login_url='/accounts/login/')
def class_create(request):
    form = GymClassForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.slug = slugify(obj.name)
        obj.save()
        messages.success(request, f'Class "{obj.name}" created.')
        return redirect('admin_panel:class_list')
    return render(request, 'admin_panel/form.html', {
        'form': form, 'title': 'Add Class', 'back_url': 'admin_panel:class_list'
    })

@staff_member_required(login_url='/accounts/login/')
def class_edit(request, pk):
    obj = get_object_or_404(GymClass, pk=pk)
    form = GymClassForm(request.POST or None, request.FILES or None, instance=obj)
    if form.is_valid():
        form.save()
        messages.success(request, f'Class "{obj.name}" updated.')
        return redirect('admin_panel:class_list')
    return render(request, 'admin_panel/form.html', {
        'form': form, 'title': f'Edit Class — {obj.name}',
        'back_url': 'admin_panel:class_list', 'obj': obj
    })

@staff_member_required(login_url='/accounts/login/')
def class_delete(request, pk):
    obj = get_object_or_404(GymClass, pk=pk)
    if request.method == 'POST':
        name = obj.name
        obj.delete()
        messages.success(request, f'Class "{name}" deleted.')
        return redirect('admin_panel:class_list')
    return render(request, 'admin_panel/confirm_delete.html', {
        'obj': obj, 'obj_type': 'Class', 'back_url': 'admin_panel:class_list'
    })


# ─────────────────────────────────────────
# SCHEDULES
# ─────────────────────────────────────────

@staff_member_required(login_url='/accounts/login/')
def schedule_list(request):
    schedules = ClassSchedule.objects.select_related('gym_class', 'gym_class__trainer').all()
    return render(request, 'admin_panel/schedule_list.html', {
        'schedules': schedules, 'meta_title': 'Manage Schedules'
    })

@staff_member_required(login_url='/accounts/login/')
def schedule_create(request):
    form = ClassScheduleForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Schedule entry created.')
        return redirect('admin_panel:schedule_list')
    return render(request, 'admin_panel/form.html', {
        'form': form, 'title': 'Add Schedule Entry', 'back_url': 'admin_panel:schedule_list'
    })

@staff_member_required(login_url='/accounts/login/')
def schedule_edit(request, pk):
    obj = get_object_or_404(ClassSchedule, pk=pk)
    form = ClassScheduleForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
        messages.success(request, 'Schedule updated.')
        return redirect('admin_panel:schedule_list')
    return render(request, 'admin_panel/form.html', {
        'form': form, 'title': f'Edit Schedule — {obj}',
        'back_url': 'admin_panel:schedule_list', 'obj': obj
    })

@staff_member_required(login_url='/accounts/login/')
def schedule_delete(request, pk):
    obj = get_object_or_404(ClassSchedule, pk=pk)
    if request.method == 'POST':
        obj.delete()
        messages.success(request, 'Schedule entry deleted.')
        return redirect('admin_panel:schedule_list')
    return render(request, 'admin_panel/confirm_delete.html', {
        'obj': obj, 'obj_type': 'Schedule', 'back_url': 'admin_panel:schedule_list'
    })


# ─────────────────────────────────────────
# EXERCISES
# ─────────────────────────────────────────

@staff_member_required(login_url='/accounts/login/')
def exercise_list(request):
    exercises = Exercise.objects.all()
    return render(request, 'admin_panel/exercise_list.html', {
        'exercises': exercises, 'meta_title': 'Manage Exercises'
    })

@staff_member_required(login_url='/accounts/login/')
def exercise_create(request):
    form = ExerciseForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.slug = slugify(obj.name)
        obj.save()
        messages.success(request, f'Exercise "{obj.name}" created.')
        return redirect('admin_panel:exercise_list')
    return render(request, 'admin_panel/form.html', {
        'form': form, 'title': 'Add Exercise', 'back_url': 'admin_panel:exercise_list'
    })

@staff_member_required(login_url='/accounts/login/')
def exercise_edit(request, pk):
    obj = get_object_or_404(Exercise, pk=pk)
    form = ExerciseForm(request.POST or None, request.FILES or None, instance=obj)
    if form.is_valid():
        form.save()
        messages.success(request, f'Exercise "{obj.name}" updated.')
        return redirect('admin_panel:exercise_list')
    return render(request, 'admin_panel/form.html', {
        'form': form, 'title': f'Edit Exercise — {obj.name}',
        'back_url': 'admin_panel:exercise_list', 'obj': obj
    })

@staff_member_required(login_url='/accounts/login/')
def exercise_delete(request, pk):
    obj = get_object_or_404(Exercise, pk=pk)
    if request.method == 'POST':
        name = obj.name
        obj.delete()
        messages.success(request, f'Exercise "{name}" deleted.')
        return redirect('admin_panel:exercise_list')
    return render(request, 'admin_panel/confirm_delete.html', {
        'obj': obj, 'obj_type': 'Exercise', 'back_url': 'admin_panel:exercise_list'
    })


# ─────────────────────────────────────────
# GALLERY
# ─────────────────────────────────────────

@staff_member_required(login_url='/accounts/login/')
def gallery_list(request):
    images = GalleryImage.objects.all()
    return render(request, 'admin_panel/gallery_list.html', {
        'images': images, 'meta_title': 'Manage Gallery'
    })

@staff_member_required(login_url='/accounts/login/')
def gallery_create(request):
    form = GalleryImageForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Image added to gallery.')
        return redirect('admin_panel:gallery_list')
    return render(request, 'admin_panel/form.html', {
        'form': form, 'title': 'Add Gallery Image', 'back_url': 'admin_panel:gallery_list'
    })

@staff_member_required(login_url='/accounts/login/')
def gallery_edit(request, pk):
    obj = get_object_or_404(GalleryImage, pk=pk)
    form = GalleryImageForm(request.POST or None, request.FILES or None, instance=obj)
    if form.is_valid():
        form.save()
        messages.success(request, 'Gallery image updated.')
        return redirect('admin_panel:gallery_list')
    return render(request, 'admin_panel/form.html', {
        'form': form, 'title': f'Edit Image — {obj.title}',
        'back_url': 'admin_panel:gallery_list', 'obj': obj
    })

@staff_member_required(login_url='/accounts/login/')
def gallery_delete(request, pk):
    obj = get_object_or_404(GalleryImage, pk=pk)
    if request.method == 'POST':
        obj.delete()
        messages.success(request, 'Image deleted.')
        return redirect('admin_panel:gallery_list')
    return render(request, 'admin_panel/confirm_delete.html', {
        'obj': obj, 'obj_type': 'Gallery Image', 'back_url': 'admin_panel:gallery_list'
    })


# ─────────────────────────────────────────
# TESTIMONIALS
# ─────────────────────────────────────────

@staff_member_required(login_url='/accounts/login/')
def testimonial_list(request):
    testimonials = Testimonial.objects.all()
    return render(request, 'admin_panel/testimonial_list.html', {
        'testimonials': testimonials, 'meta_title': 'Manage Testimonials'
    })

@staff_member_required(login_url='/accounts/login/')
def testimonial_create(request):
    form = TestimonialForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Testimonial added.')
        return redirect('admin_panel:testimonial_list')
    return render(request, 'admin_panel/form.html', {
        'form': form, 'title': 'Add Testimonial', 'back_url': 'admin_panel:testimonial_list'
    })

@staff_member_required(login_url='/accounts/login/')
def testimonial_edit(request, pk):
    obj = get_object_or_404(Testimonial, pk=pk)
    form = TestimonialForm(request.POST or None, request.FILES or None, instance=obj)
    if form.is_valid():
        form.save()
        messages.success(request, 'Testimonial updated.')
        return redirect('admin_panel:testimonial_list')
    return render(request, 'admin_panel/form.html', {
        'form': form, 'title': f'Edit Testimonial — {obj.name}',
        'back_url': 'admin_panel:testimonial_list', 'obj': obj
    })

@staff_member_required(login_url='/accounts/login/')
def testimonial_delete(request, pk):
    obj = get_object_or_404(Testimonial, pk=pk)
    if request.method == 'POST':
        obj.delete()
        messages.success(request, 'Testimonial deleted.')
        return redirect('admin_panel:testimonial_list')
    return render(request, 'admin_panel/confirm_delete.html', {
        'obj': obj, 'obj_type': 'Testimonial', 'back_url': 'admin_panel:testimonial_list'
    })


# ─────────────────────────────────────────
# MEMBERSHIP PLANS
# ─────────────────────────────────────────

@staff_member_required(login_url='/accounts/login/')
def plan_list(request):
    plans = MembershipPlan.objects.all()
    return render(request, 'admin_panel/plan_list.html', {
        'plans': plans, 'meta_title': 'Manage Membership Plans'
    })

@staff_member_required(login_url='/accounts/login/')
def plan_create(request):
    form = MembershipPlanForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Membership plan created.')
        return redirect('admin_panel:plan_list')
    return render(request, 'admin_panel/form.html', {
        'form': form, 'title': 'Add Membership Plan', 'back_url': 'admin_panel:plan_list'
    })

@staff_member_required(login_url='/accounts/login/')
def plan_edit(request, pk):
    obj = get_object_or_404(MembershipPlan, pk=pk)
    form = MembershipPlanForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
        messages.success(request, f'Plan "{obj.name}" updated.')
        return redirect('admin_panel:plan_list')
    return render(request, 'admin_panel/form.html', {
        'form': form, 'title': f'Edit Plan — {obj.name}',
        'back_url': 'admin_panel:plan_list', 'obj': obj
    })

@staff_member_required(login_url='/accounts/login/')
def plan_delete(request, pk):
    obj = get_object_or_404(MembershipPlan, pk=pk)
    if request.method == 'POST':
        name = obj.name
        obj.delete()
        messages.success(request, f'Plan "{name}" deleted.')
        return redirect('admin_panel:plan_list')
    return render(request, 'admin_panel/confirm_delete.html', {
        'obj': obj, 'obj_type': 'Membership Plan', 'back_url': 'admin_panel:plan_list'
    })


# ─────────────────────────────────────────
# CONTACT MESSAGES INBOX
# ─────────────────────────────────────────

@staff_member_required(login_url='/accounts/login/')
def message_inbox(request):
    filter_status = request.GET.get('status', 'all')
    msgs = ContactMessage.objects.all()
    if filter_status == 'unread':
        msgs = msgs.filter(is_read=False)
    elif filter_status == 'read':
        msgs = msgs.filter(is_read=True)
    elif filter_status == 'replied':
        msgs = msgs.filter(replied=True)

    unread_count = ContactMessage.objects.filter(is_read=False).count()
    return render(request, 'admin_panel/message_inbox.html', {
        'messages_list': msgs,
        'filter_status': filter_status,
        'unread_count': unread_count,
        'meta_title': 'Message Inbox',
    })

@staff_member_required(login_url='/accounts/login/')
def message_detail(request, pk):
    msg = get_object_or_404(ContactMessage, pk=pk)
    # Auto-mark as read on open
    if not msg.is_read:
        msg.is_read = True
        msg.save(update_fields=['is_read'])
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'mark_replied':
            msg.replied = True
            msg.save(update_fields=['replied'])
            messages.success(request, 'Marked as replied.')
        elif action == 'mark_unread':
            msg.is_read = False
            msg.save(update_fields=['is_read'])
            messages.info(request, 'Marked as unread.')
        elif action == 'delete':
            msg.delete()
            messages.success(request, 'Message deleted.')
            return redirect('admin_panel:message_inbox')
        return redirect('admin_panel:message_detail', pk=pk)
    return render(request, 'admin_panel/message_detail.html', {
        'msg': msg, 'meta_title': f'Message from {msg.name}'
    })
