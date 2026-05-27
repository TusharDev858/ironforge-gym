from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
                ('bio', models.TextField(blank=True)),
                ('avatar', models.ImageField(blank=True, null=True, upload_to='avatars/')),
                ('date_of_birth', models.DateField(blank=True, null=True)),
                ('phone', models.CharField(blank=True, max_length=20)),
                ('height_cm', models.DecimalField(blank=True, decimal_places=1, max_digits=5, null=True)),
                ('weight_kg', models.DecimalField(blank=True, decimal_places=1, max_digits=5, null=True)),
                ('body_fat_percentage', models.DecimalField(blank=True, decimal_places=1, max_digits=4, null=True)),
                ('fitness_goal', models.CharField(choices=[('weight_loss','Weight Loss'),('muscle_gain','Muscle Gain'),('endurance','Build Endurance'),('flexibility','Improve Flexibility'),('general_fitness','General Fitness'),('athletic_performance','Athletic Performance'),('rehabilitation','Rehabilitation'),('stress_relief','Stress Relief')], default='general_fitness', max_length=30)),
                ('activity_level', models.CharField(choices=[('sedentary','Sedentary (little/no exercise)'),('lightly_active','Lightly Active (1-3 days/week)'),('moderately_active','Moderately Active (3-5 days/week)'),('very_active','Very Active (6-7 days/week)'),('extra_active','Extra Active (twice a day)')], default='sedentary', max_length=20)),
                ('experience_level', models.CharField(choices=[('beginner','Beginner (< 1 year)'),('intermediate','Intermediate (1-3 years)'),('advanced','Advanced (3+ years)')], default='beginner', max_length=20)),
                ('health_conditions', models.TextField(blank=True, help_text='Any health conditions or injuries')),
                ('emergency_contact', models.CharField(blank=True, max_length=100)),
                ('emergency_phone', models.CharField(blank=True, max_length=20)),
                ('membership_start', models.DateField(blank=True, null=True)),
                ('membership_end', models.DateField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
