# IBMTS 2027

Django site for the Ibadan Muslim Tech Summit. Attendee payments use Paystack's hosted checkout; the application confirms a registration only after checking the transaction with Paystack.

## Local development

```sh
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

For local checkout testing, create a `.env` containing `PAYSTACK_SECRET_KEY` with a Paystack **test** secret key. `.env.example` contains production defaults, so do not copy it unchanged for local development. `.env` is ignored by Git. The local default email backend prints confirmation messages to the console.

## Deploy to PythonAnywhere

Create a PythonAnywhere web app with manual Django configuration and a Python version supported by the account. In a Bash console, clone the repository into your home directory and create the virtual environment with that same Python version:

```sh
cd ~
git clone https://github.com/Abdulmateenmuthoir/IBMTS.git
cd IBMTS
python3.12 -m venv .venv
.venv/bin/pip install -r requirements.txt
cp .env.example .env
chmod 600 .env
```

Replace `python3.12` with the Python version selected for the web app. Edit `~/IBMTS/.env` on the host. Set a newly generated `DJANGO_SECRET_KEY`, `DJANGO_DEBUG=false`, the PythonAnywhere hostname in `DJANGO_ALLOWED_HOSTS` and `DJANGO_CSRF_TRUSTED_ORIGINS`, and production Paystack and email credentials. Set `PAYSTACK_CALLBACK_URL` to `https://YOUR-HOSTNAME/payment/callback/`. Keep live keys out of Git and logs.

In the PythonAnywhere Web tab:

1. Set the source code directory to `/home/YOUR-USERNAME/IBMTS` and the virtualenv to `/home/YOUR-USERNAME/IBMTS/.venv`.
2. Edit the generated WSGI file and replace its Django section with:

   ```python
   import os
   import sys

   project_home = '/home/YOUR-USERNAME/IBMTS'
   if project_home not in sys.path:
       sys.path.insert(0, project_home)
   os.chdir(project_home)
   os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ibmts_platform.settings')

   from django.core.wsgi import get_wsgi_application
   application = get_wsgi_application()
   ```

   Settings load the private `.env` from the project directory.
3. Add a static file mapping from `/static/` to `/home/YOUR-USERNAME/IBMTS/staticfiles` and a media mapping from `/media/` to `/home/YOUR-USERNAME/IBMTS/media`.
4. In a Bash console, run:

   ```sh
   cd ~/IBMTS
   .venv/bin/python manage.py migrate
   .venv/bin/python manage.py collectstatic --noinput
   .venv/bin/python manage.py createsuperuser
   ```

5. Enable HTTPS for the site, then reload the web app from the Web tab.

In Paystack's dashboard, set the webhook URL to `https://YOUR-HOSTNAME/payment/webhook/`. Configure `PAYSTACK_WEBHOOK_SECRET` from the dashboard's webhook signing secret. The webhook confirms payments independently of the customer's browser return; the callback also verifies the transaction server to server.

Start with Paystack test credentials and complete a test checkout before changing `PAYSTACK_SECRET_KEY` to a live key. Confirm that the webhook is received and that a paid attendee appears in the admin dashboard. Never use a live key for a test checkout or publish either key.

PythonAnywhere's current Django deployment guide: <https://help.pythonanywhere.com/pages/DeployExistingDjangoProject/>.
