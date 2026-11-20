"""One-time setup helper for cPanel accounts without Terminal access.

Run it once from a cPanel Cron Job after uploading the project and installing
requirements. Remove the temporary Cron Job after it completes.
"""

import os
import sys
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent
if str(PROJECT_DIR) not in sys.path:
    sys.path.insert(0, str(PROJECT_DIR))
os.chdir(PROJECT_DIR)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ibmts_platform.settings')

import django

django.setup()

from django.contrib.auth import get_user_model
from django.core.management import call_command

call_command('migrate', interactive=False)
call_command('collectstatic', interactive=False, clear=False)

username = os.environ.get('DJANGO_SUPERUSER_USERNAME', '').strip()
email = os.environ.get('DJANGO_SUPERUSER_EMAIL', '').strip()
password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', '')
User = get_user_model()

if username and email and password and not User.objects.filter(username=username).exists():
    call_command('createsuperuser', username=username, email=email, interactive=False)

print('IBMTS cPanel setup completed.')
