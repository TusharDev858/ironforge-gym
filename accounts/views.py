from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse
from .forms import RegisterForm, ProfileForm, UserUpdateForm
from .models import UserProfile
from bookings.models import Booking


def register(request):
    if request.user.is_authenticated:
        return redirect('accounts:profile')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.create(user=user)
            login(request, user)
            messages.success(request, f'Welcome to IronForge, {user.first_name}! Complete your profile below.')
            return redirect('accounts:profile')
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form, 'meta_title': 'Join IronForge Gym'})


def user_login(request):
    if request.user.is_authenticated:
        return redirect('accounts:profile')
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            next_url = request.GET.get('next') or reverse('accounts:profile')
            messages.success(request, f'Welcome back, {user.first_name or user.username}!')
            return redirect(next_url)
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form, 'meta_title': 'Login | IronForge Gym'})


def user_logout(request):
    logout(request)
    messages.info(request, 'You have been logged out. See you next time!')
    return redirect('core:home')


@login_required
def profile(request):
    profile_obj, created = UserProfile.objects.get_or_create(user=request.user)
    recent_bookings = Booking.objects.filter(user=request.user).select_related(
        'schedule__gym_class', 'schedule__gym_class__trainer'
    ).order_by('-created_at')[:5]
    context = {
        'profile': profile_obj,
        'recent_bookings': recent_bookings,
        'meta_title': f'{request.user.first_name}\'s Profile | IronForge Gym',
    }
    return render(request, 'accounts/profile.html', context)


@login_required
def edit_profile(request):
    profile_obj, created = UserProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=profile_obj)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('accounts:profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileForm(instance=profile_obj)
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'meta_title': 'Edit Profile | IronForge Gym',
    }
    return render(request, 'accounts/edit_profile.html', context)
