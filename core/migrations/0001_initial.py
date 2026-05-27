from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Trainer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('slug', models.SlugField(blank=True, unique=True)),
                ('specialty', models.CharField(max_length=200)),
                ('bio', models.TextField()),
                ('photo', models.ImageField(blank=True, null=True, upload_to='trainers/')),
                ('experience_years', models.PositiveIntegerField(default=1)),
                ('certifications', models.TextField(blank=True, help_text='Comma-separated certifications')),
                ('instagram', models.URLField(blank=True)),
                ('order', models.PositiveIntegerField(default=0)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={'ordering': ['order', 'name']},
        ),
        migrations.CreateModel(
            name='GymClass',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('slug', models.SlugField(blank=True, unique=True)),
                ('category', models.CharField(choices=[('strength','Strength Training'),('cardio','Cardio'),('yoga','Yoga & Flexibility'),('hiit','HIIT'),('pilates','Pilates'),('boxing','Boxing'),('spin','Spin / Cycling'),('crossfit','CrossFit')], default='strength', max_length=20)),
                ('description', models.TextField()),
                ('trainer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='classes', to='core.trainer')),
                ('difficulty', models.CharField(choices=[('beginner','Beginner'),('intermediate','Intermediate'),('advanced','Advanced'),('all','All Levels')], default='all', max_length=20)),
                ('duration_minutes', models.PositiveIntegerField(default=60)),
                ('max_capacity', models.PositiveIntegerField(default=20)),
                ('image', models.ImageField(blank=True, null=True, upload_to='classes/')),
                ('icon', models.CharField(default='🏋️', help_text='Emoji icon for the class', max_length=50)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={'ordering': ['name'], 'verbose_name': 'Gym Class', 'verbose_name_plural': 'Gym Classes'},
        ),
        migrations.CreateModel(
            name='ClassSchedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gym_class', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='schedules', to='core.gymclass')),
                ('day_of_week', models.IntegerField(choices=[(0,'Monday'),(1,'Tuesday'),(2,'Wednesday'),(3,'Thursday'),(4,'Friday'),(5,'Saturday'),(6,'Sunday')])),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('room', models.CharField(default='Main Floor', max_length=50)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={'ordering': ['day_of_week', 'start_time']},
        ),
        migrations.CreateModel(
            name='Exercise',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('slug', models.SlugField(blank=True, unique=True)),
                ('muscle_group', models.CharField(choices=[('chest','Chest'),('back','Back'),('shoulders','Shoulders'),('arms','Arms'),('core','Core'),('legs','Legs'),('glutes','Glutes'),('full_body','Full Body'),('cardio','Cardio')], max_length=20)),
                ('equipment', models.CharField(choices=[('barbell','Barbell'),('dumbbell','Dumbbell'),('cable','Cable Machine'),('machine','Machine'),('bodyweight','Bodyweight'),('kettlebell','Kettlebell'),('resistance_band','Resistance Band'),('pull_up_bar','Pull-Up Bar')], default='bodyweight', max_length=20)),
                ('description', models.TextField()),
                ('instructions', models.TextField(help_text='Step-by-step instructions')),
                ('sets_reps', models.CharField(default='3 sets x 10 reps', max_length=100)),
                ('difficulty', models.CharField(choices=[('beginner','Beginner'),('intermediate','Intermediate'),('advanced','Advanced'),('all','All Levels')], default='beginner', max_length=20)),
                ('image', models.ImageField(blank=True, null=True, upload_to='exercises/')),
                ('video_url', models.URLField(blank=True, help_text='YouTube embed URL')),
                ('calories_per_hour', models.PositiveIntegerField(default=300)),
                ('is_featured', models.BooleanField(default=False)),
            ],
            options={'ordering': ['muscle_group', 'name']},
        ),
        migrations.CreateModel(
            name='GalleryImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('image', models.ImageField(upload_to='gallery/')),
                ('category', models.CharField(choices=[('facility','Facility'),('equipment','Equipment'),('classes','Classes'),('events','Events')], default='facility', max_length=20)),
                ('order', models.PositiveIntegerField(default=0)),
                ('is_featured', models.BooleanField(default=False)),
            ],
            options={'ordering': ['order']},
        ),
        migrations.CreateModel(
            name='Testimonial',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('role', models.CharField(default='Member', max_length=100)),
                ('content', models.TextField()),
                ('rating', models.PositiveIntegerField(default=5)),
                ('photo', models.ImageField(blank=True, null=True, upload_to='testimonials/')),
                ('is_featured', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='MembershipPlan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('price', models.DecimalField(decimal_places=2, max_digits=8)),
                ('billing_period', models.CharField(default='month', max_length=20)),
                ('features', models.TextField(help_text='One feature per line')),
                ('is_featured', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('order', models.PositiveIntegerField(default=0)),
            ],
            options={'ordering': ['order', 'price']},
        ),
        migrations.CreateModel(
            name='ContactMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField()),
                ('phone', models.CharField(blank=True, max_length=20)),
                ('subject', models.CharField(choices=[('membership','Membership Enquiry'),('classes','Classes & Schedule'),('personal_training','Personal Training'),('facilities','Facilities & Equipment'),('other','Other')], default='other', max_length=30)),
                ('message', models.TextField()),
                ('is_read', models.BooleanField(default=False)),
                ('replied', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={'ordering': ['-created_at'], 'verbose_name': 'Contact Message', 'verbose_name_plural': 'Contact Messages'},
        ),
    ]
