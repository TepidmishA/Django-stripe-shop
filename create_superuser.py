"""
This module initializes Django and creates a superuser if the required
environment variables are set and the user does not already exist.

Environment variables used:
- DJANGO_SUPERUSER_USERNAME: username for the superuser
- DJANGO_SUPERUSER_PASSWORD: password for the superuser
- DJANGO_SUPERUSER_EMAIL: email for the superuser

If all variables are provided and the superuser does not exist, it creates
the superuser and prints a confirmation message. Otherwise, it prints
an appropriate message.
"""

import os
import django
from django.contrib.auth import get_user_model

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'simple_shop.settings')
django.setup()

User = get_user_model()

username = os.getenv('DJANGO_SUPERUSER_USERNAME')
password = os.getenv('DJANGO_SUPERUSER_PASSWORD')
email = os.getenv('DJANGO_SUPERUSER_EMAIL')

if username and password and email:
    if not User.objects.filter(username=username).exists():
        User.objects.create_superuser(username=username, email=email, password=password)
        print(f"Superuser {username} created.")
    else:
        print(f"Superuser {username} already exists.")
else:
    print("Superuser environment variables not set properly.")
