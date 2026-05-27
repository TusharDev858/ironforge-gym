# IronForge Gym — Deployment Guide

## Quick Start (Local Development)

```bash
# 1. Clone / unzip the project
cd ironforge_gym

# 2. Create a virtual environment
python -m venv venv
source venv/bin/activate       # Windows: venv\Scripts\activate

# 3. Run setup (installs deps, migrates, loads demo data)
python setup.py

# 4. Create superuser
python manage.py createsuperuser

# 5. Start dev server
python manage.py runserver

# Visit: http://127.0.0.1:8000
# Admin:  http://127.0.0.1:8000/admin
```

---

## Production Deployment (Ubuntu + Nginx + Gunicorn)

### 1. Install system packages
```bash
sudo apt update
sudo apt install python3-pip python3-venv nginx postgresql postgresql-contrib
```

### 2. Clone and set up the app
```bash
git clone <your-repo> /var/www/ironforge
cd /var/www/ironforge
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Set environment variables
Create `/var/www/ironforge/.env`:
```
SECRET_KEY=your-very-secret-key-here-change-me
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
```

Update `ironforge_gym/settings.py` to load from `.env` using `python-decouple` or `os.environ`.

### 4. Initialize
```bash
python manage.py migrate
python manage.py loaddata core/fixtures/initial_data.json
python manage.py collectstatic
python manage.py createsuperuser
```

### 5. Gunicorn service
Create `/etc/systemd/system/ironforge.service`:
```ini
[Unit]
Description=IronForge Gym Gunicorn
After=network.target

[Service]
User=www-data
WorkingDirectory=/var/www/ironforge
ExecStart=/var/www/ironforge/venv/bin/gunicorn \
    --workers 3 \
    --bind unix:/run/ironforge.sock \
    ironforge_gym.wsgi:application

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl start ironforge
sudo systemctl enable ironforge
```

### 6. Nginx config
Create `/etc/nginx/sites-available/ironforge`:
```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;

    location = /favicon.ico { access_log off; log_not_found off; }

    location /static/ {
        root /var/www/ironforge;
    }

    location /media/ {
        root /var/www/ironforge;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/run/ironforge.sock;
    }
}
```

```bash
sudo ln -s /etc/nginx/sites-available/ironforge /etc/nginx/sites-enabled
sudo nginx -t
sudo systemctl restart nginx
```

### 7. SSL (Let's Encrypt)
```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

---

## Deploy to Railway / Render / Fly.io (One-click)

### Railway
1. Push code to GitHub
2. New project → Deploy from GitHub
3. Set env vars: `SECRET_KEY`, `DEBUG=False`, `ALLOWED_HOSTS`
4. Add start command: `gunicorn ironforge_gym.wsgi:application`

### Render
1. New Web Service → connect GitHub repo
2. Build: `pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate`
3. Start: `gunicorn ironforge_gym.wsgi:application`

---

## Admin Panel Features

Visit `/admin` with your superuser to:

- **Trainers** — Add, edit, reorder trainer profiles with photos and certifications
- **Classes** — Create class types with icons, categories, difficulty, capacity
- **Schedules** — Assign classes to days/times/rooms inline on the class page
- **Exercises** — Build your exercise library with instructions and videos
- **Bookings** — View and manage all member bookings and status
- **Members** — View user profiles, fitness goals, and body stats
- **Plans** — Set up membership pricing tiers
- **Gallery** — Upload facility and equipment photos
- **Testimonials** — Feature member success stories

---

## Project Structure

```
ironforge_gym/
├── ironforge_gym/       # Django config (settings, urls, wsgi)
├── core/                # Main app (trainers, classes, exercises, gallery)
│   ├── models.py
│   ├── views.py
│   ├── admin.py
│   ├── urls.py
│   ├── sitemaps.py
│   └── fixtures/initial_data.json
├── accounts/            # Auth, registration, user profiles
├── bookings/            # Class booking system
├── templates/           # All HTML templates
├── static/              # CSS, JS, images
├── media/               # User-uploaded files
├── requirements.txt
├── setup.py             # Quick setup script
└── DEPLOY.md            # This file
```
