from django.contrib import admin
from .models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'fitness_goal', 'experience_level', 'membership_start', 'membership_end']
    list_filter = ['fitness_goal', 'experience_level', 'activity_level']
    search_fields = ['user__username', 'user__email', 'user__first_name', 'user__last_name']
    raw_id_fields = ['user']
