from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('classes/', views.classes, name='classes'),
    path('schedule/', views.schedule, name='schedule'),
    path('trainers/', views.trainers, name='trainers'),
    path('trainers/<slug:slug>/', views.trainer_detail, name='trainer_detail'),
    path('exercises/', views.exercises, name='exercises'),
    path('gallery/', views.gallery, name='gallery'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
]
