from django.urls import path
from core import admin_views as v

app_name = 'admin_panel'

urlpatterns = [
    # Dashboard
    path('', v.dashboard, name='dashboard'),

    # Trainers
    path('trainers/',                  v.trainer_list,   name='trainer_list'),
    path('trainers/add/',              v.trainer_create,  name='trainer_create'),
    path('trainers/<int:pk>/edit/',    v.trainer_edit,    name='trainer_edit'),
    path('trainers/<int:pk>/delete/',  v.trainer_delete,  name='trainer_delete'),

    # Classes
    path('classes/',                   v.class_list,     name='class_list'),
    path('classes/add/',               v.class_create,    name='class_create'),
    path('classes/<int:pk>/edit/',     v.class_edit,      name='class_edit'),
    path('classes/<int:pk>/delete/',   v.class_delete,    name='class_delete'),

    # Schedules
    path('schedules/',                  v.schedule_list,   name='schedule_list'),
    path('schedules/add/',              v.schedule_create, name='schedule_create'),
    path('schedules/<int:pk>/edit/',    v.schedule_edit,   name='schedule_edit'),
    path('schedules/<int:pk>/delete/',  v.schedule_delete, name='schedule_delete'),

    # Exercises
    path('exercises/',                  v.exercise_list,   name='exercise_list'),
    path('exercises/add/',              v.exercise_create, name='exercise_create'),
    path('exercises/<int:pk>/edit/',    v.exercise_edit,   name='exercise_edit'),
    path('exercises/<int:pk>/delete/',  v.exercise_delete, name='exercise_delete'),

    # Gallery
    path('gallery/',                    v.gallery_list,    name='gallery_list'),
    path('gallery/add/',                v.gallery_create,  name='gallery_create'),
    path('gallery/<int:pk>/edit/',      v.gallery_edit,    name='gallery_edit'),
    path('gallery/<int:pk>/delete/',    v.gallery_delete,  name='gallery_delete'),

    # Testimonials
    path('testimonials/',               v.testimonial_list,   name='testimonial_list'),
    path('testimonials/add/',           v.testimonial_create, name='testimonial_create'),
    path('testimonials/<int:pk>/edit/', v.testimonial_edit,   name='testimonial_edit'),
    path('testimonials/<int:pk>/delete/', v.testimonial_delete, name='testimonial_delete'),

    # Membership Plans
    path('plans/',                      v.plan_list,    name='plan_list'),
    path('plans/add/',                  v.plan_create,  name='plan_create'),
    path('plans/<int:pk>/edit/',        v.plan_edit,    name='plan_edit'),
    path('plans/<int:pk>/delete/',      v.plan_delete,  name='plan_delete'),

    # Contact Messages Inbox
    path('messages/',                   v.message_inbox,  name='message_inbox'),
    path('messages/<int:pk>/',          v.message_detail, name='message_detail'),
]
