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

## Deploy to cPanel

This project needs a cPanel host that supports Python WSGI applications through **Setup Python App** (CloudLinux Python Selector) or **Application Manager** (Passenger). A normal PHP-only cPanel account cannot run Django. The host must provide a way to install `requirements.txt` and run a one-time Python script.

### Upload without Terminal

1. In cPanel, open **Setup Python App** and create a Python app for your domain. Select Python 3.10 or newer if available, set the application root to `IBMTS`, and set the app URL to the domain root.
2. Upload `IBMTS-cpanel-deploy.zip` in **File Manager** to `/home/CPANEL-USER/IBMTS` and use **Extract**. Extract the archive contents directly into this folder. It excludes `.env`, the local SQLite database, `.git`, virtualenvs, and cPanel's generated `passenger_wsgi.py` wrapper.
3. Return to the Python app page. Under **Configuration files**, enter `requirements.txt`, click **Add**, then click **Run Pip Install**. Wait for installation to finish.
4. Set **Application startup file** to `ibmts_platform/wsgi.py` and **Application Entry Point** to `application`. Keep cPanel's generated `passenger_wsgi.py` file; do not set it as its own startup file, or Passenger can recursively load itself.
5. Add the required settings in the app page's **Environment variables** section. Use your exact domain in `DJANGO_ALLOWED_HOSTS`, `DJANGO_CSRF_TRUSTED_ORIGINS`, and `PAYSTACK_CALLBACK_URL`. Keep live keys out of Git and chat.
6. Enable HTTPS for the domain through the host's SSL/AutoSSL section before serving requests, because production redirects HTTP to HTTPS.
7. To create the database and collect static files, enter `/home/CPANEL-USER/IBMTS/cpanel_setup.py` in **Execute python script** and click **Run Script**. The helper runs migrations and collects static files. If `DJANGO_SUPERUSER_USERNAME`, `DJANGO_SUPERUSER_EMAIL`, and `DJANGO_SUPERUSER_PASSWORD` are configured for the app, it also creates that admin user. Remove the temporary password variable after setup.
8. Restart the Python app from its cPanel page and open `https://YOUR-DOMAIN/`. The new database is empty; add speaker and sponsor entries in `/admin/`.

In Paystack's dashboard, set the webhook URL to `https://YOUR-DOMAIN/payment/webhook/` and set the matching webhook signing secret in the app's environment variables as `PAYSTACK_WEBHOOK_SECRET`. Start with test-mode credentials, complete a checkout, and confirm the attendee is marked paid. Then replace both Paystack secrets with the live-mode values when ready to accept real payments. Keep all secrets out of Git and chat.

If the cPanel app page has no package installer or script runner, ask the host whether those features are enabled for your Python app. cPanel's WSGI setup requires hosting-provider support for Python and Passenger: <https://docs.cpanel.net/knowledge-base/web-services/how-to-install-a-python-wsgi-application/>.
