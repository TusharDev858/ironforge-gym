from django.contrib import admin
from .models import Trainer, GymClass, ClassSchedule, Exercise, GalleryImage, Testimonial, MembershipPlan, ContactMessage


@admin.register(Trainer)
class TrainerAdmin(admin.ModelAdmin):
    list_display = ['name', 'specialty', 'experience_years', 'is_active', 'order']
    list_editable = ['is_active', 'order']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name', 'specialty']
    list_filter = ['is_active']


class ClassScheduleInline(admin.TabularInline):
    model = ClassSchedule
    extra = 1


@admin.register(GymClass)
class GymClassAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'trainer', 'difficulty', 'duration_minutes', 'max_capacity', 'is_active']
    list_editable = ['is_active']
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ['category', 'difficulty', 'is_active']
    search_fields = ['name', 'description']
    inlines = [ClassScheduleInline]


@admin.register(ClassSchedule)
class ClassScheduleAdmin(admin.ModelAdmin):
    list_display = ['gym_class', 'day_of_week', 'start_time', 'end_time', 'room', 'is_active']
    list_editable = ['is_active']
    list_filter = ['day_of_week', 'is_active', 'gym_class']


@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    list_display = ['name', 'muscle_group', 'equipment', 'difficulty', 'is_featured']
    list_editable = ['is_featured']
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ['muscle_group', 'equipment', 'difficulty']
    search_fields = ['name', 'description']


@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'order', 'is_featured']
    list_editable = ['order', 'is_featured']
    list_filter = ['category']


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ['name', 'role', 'rating', 'is_featured']
    list_editable = ['is_featured']


@admin.register(MembershipPlan)
class MembershipPlanAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'billing_period', 'is_featured', 'is_active', 'order']
    list_editable = ['is_featured', 'is_active', 'order']


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'is_read', 'replied', 'created_at']
    list_editable = ['is_read', 'replied']
    list_filter = ['subject', 'is_read', 'replied']
    search_fields = ['name', 'email', 'message']
    readonly_fields = ['name', 'email', 'phone', 'subject', 'message', 'created_at']
    date_hierarchy = 'created_at'

    def has_add_permission(self, request):
        # Contact messages are only created by visitors, not manually via admin
        return False
