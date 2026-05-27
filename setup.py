#!/usr/bin/env python3
"""IronForge Gym — one-command setup script."""
import os, sys, subprocess

def run(cmd):
    print(f"  → {cmd}")
    subprocess.run(cmd, shell=True, check=True)

os.chdir(os.path.dirname(os.path.abspath(__file__)))
print("\n" + "="*52)
print("  🏋️  IRONFORGE GYM — SETUP")
print("="*52 + "\n")

print("[1/5] Installing dependencies...")
run("pip install django pillow django-crispy-forms crispy-bootstrap5 whitenoise gunicorn")

print("\n[2/5] Running migrations...")
run("python manage.py migrate --run-syncdb")

print("\n[3/5] Loading demo data...")
try:
    run("python manage.py loaddata core/fixtures/initial_data.json")
except:
    print("  ⚠ Fixtures skipped — add content via /manage/")

print("\n[4/5] Collecting static files...")
try:
    run("python manage.py collectstatic --noinput")
except:
    pass

print("\n[5/5] Done!\n")
print("="*52)
print("  Next steps:")
print("  1. python manage.py createsuperuser")
print("  2. python manage.py runserver")
print("  3. Open http://127.0.0.1:8000")
print("  4. Admin panel: http://127.0.0.1:8000/manage/")
print("="*52 + "\n")
