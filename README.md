# FSDI_Ch68_Capstone_Strubell

## Cinematic Strubell Goods & Gear Marketplace

A responsive Django capstone application for Strubell Goods & Gear (SGnG). The project combines a cinematic branded interface with authentication, a searchable product catalog, staff product management, a contact workflow, REST API support, automated Django tests, and Selenium end-to-end testing.

## Project Status

- Core Django architecture implemented
- Accounts and authentication implemented
- Marketplace catalog and product-detail workflow implemented
- Staff product create, update, and delete workflow implemented
- Django REST Framework included
- Responsive SGnG visual system implemented
- Contact form validation implemented
- Gmail SMTP delivery configuration documented below
- Automated Django and Selenium tests included
- Stripe SDK installed for future payment integration; checkout is not yet claimed as complete

## Technology Stack

- Python
- Django 6.1.2
- Django REST Framework
- HTML5, CSS3, and JavaScript
- SQLite for local development
- PostgreSQL-ready configuration through `dj-database-url`
- Pillow for image handling
- Selenium for browser-based tests
- Gunicorn and WhiteNoise for production preparation
- Stripe Python SDK for planned payment functionality

## Repository Structure

```text
FSDI_Ch68_Capstone_Strubell/
├── accounts/                 # Authentication and account workflows
├── catalog/                  # Products, marketplace, staff CRUD, and API
├── config/                   # Project settings and root URLs
├── contact/                  # Contact form, view, template, and tests
├── pages/                    # Homepage and general pages
├── static/                   # CSS, JavaScript, images, branding, and favicon files
├── templates/                # Shared project templates
├── tests/                    # Selenium and cross-application tests
├── manage.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## Local Installation on Windows 11

### 1. Clone the repository

```powershell
git clone https://github.com/TStrubell/FSDI_Ch68_Capstone_Strubell.git
cd FSDI_Ch68_Capstone_Strubell
```

### 2. Create and activate a virtual environment

```powershell
py -m venv venv
.\venv\Scripts\Activate.ps1
```

If PowerShell blocks activation for the current session:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
py -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Create the local environment file

```powershell
Copy-Item .env.example .env
```

Replace the placeholders in `.env` with your own development credentials. Never commit `.env`.

### 5. Apply migrations

```powershell
py manage.py migrate
```

### 6. Create a superuser

```powershell
py manage.py createsuperuser
```

### 7. Run the project

```powershell
py manage.py runserver
```

Open `http://127.0.0.1:8000/` in a browser.

## Environment Variables

Use the following structure in the private `.env` file:

```dotenv
DEBUG=True
SECRET_KEY=replace-with-a-unique-local-secret-key
ALLOWED_HOSTS=127.0.0.1,localhost
DATABASE_URL=sqlite:///db.sqlite3

DEFAULT_FROM_EMAIL=your_gmail_address@gmail.com
CONTACT_EMAIL=your_recipient_address@gmail.com
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your_gmail_address@gmail.com
EMAIL_HOST_PASSWORD=your_16_character_google_app_password

STRIPE_SECRET_KEY=sk_test_replace_with_your_test_secret_key
STRIPE_PUBLIC_KEY=pk_test_replace_with_your_test_publishable_key
```

The committed `.env.example` must contain only safe placeholders:

```dotenv
DEBUG=True
SECRET_KEY=replace-with-secret-key
ALLOWED_HOSTS=127.0.0.1,localhost
DATABASE_URL=sqlite:///db.sqlite3

DEFAULT_FROM_EMAIL=your_email@example.com
CONTACT_EMAIL=recipient@example.com
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your_email@example.com
EMAIL_HOST_PASSWORD=replace-with-google-app-password

STRIPE_SECRET_KEY=sk_test_replace-with-stripe-secret-key
STRIPE_PUBLIC_KEY=pk_test_replace-with-stripe-public-key
```

## Generate a Django Secret Key

Run this command inside the activated virtual environment:

```powershell
py -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Copy the output into `SECRET_KEY` in `.env`. Do not post it publicly or commit it to GitHub.

## Gmail SMTP Contact Delivery

The current contact form must call Django's mail API before displaying a success message. Gmail SMTP configuration alone does not send a message.

1. Enable 2-Step Verification on the sending Google account.
2. Create a Google App Password for the Django application.
3. Put the Gmail address in `EMAIL_HOST_USER` and `DEFAULT_FROM_EMAIL`.
4. Put the 16-character App Password in `EMAIL_HOST_PASSWORD`.
5. Put the inbox that should receive contact messages in `CONTACT_EMAIL`.
6. Load these variables in `config/settings.py`.
7. Call `send_mail()` or `EmailMessage.send()` from the valid contact-form workflow.
8. Display the success message only after the mail call succeeds.

Do not use the normal Google account password and do not commit the App Password.

## Contact Form Behavior

A valid contact submission should:

- validate the visitor's name, email, subject, and message;
- send the formatted inquiry to `CONTACT_EMAIL`;
- use `DEFAULT_FROM_EMAIL` as the authenticated sender;
- use the visitor's address as `reply_to`, rather than spoofing the SMTP sender;
- display a success message only after successful delivery;
- preserve form errors when validation or delivery fails.

## Database Configuration

Local development uses:

```dotenv
DATABASE_URL=sqlite:///db.sqlite3
```

A production host normally supplies its own PostgreSQL connection URL, similar to:

```dotenv
DATABASE_URL=postgresql://USER:PASSWORD@HOST:5432/DATABASE_NAME
```

Use the exact URL issued by the selected host. Do not invent production database credentials or commit them.

## Stripe Configuration

Create or select a Stripe sandbox and copy the test credentials from the Stripe Dashboard API keys area:

- `STRIPE_PUBLIC_KEY` receives the publishable test key beginning with `pk_test_`.
- `STRIPE_SECRET_KEY` receives the secret test key beginning with `sk_test_`.

Never expose the secret key in HTML, JavaScript, screenshots, reports, or the repository. Installing the Stripe package does not by itself implement checkout.

## Testing

Run the complete Django test suite:

```powershell
py manage.py test -v 2
```

Run application tests separately when troubleshooting:

```powershell
py manage.py test accounts -v 2
py manage.py test pages -v 2
py manage.py test contact -v 2
py manage.py test catalog -v 2
```

Run the Selenium suite:

```powershell
py manage.py test tests.selenium -v 2
```

Test Gmail SMTP independently in the Django shell before testing the browser form:

```powershell
py manage.py shell
```

```python
from django.conf import settings
from django.core.mail import send_mail

send_mail(
    subject="SGnG SMTP test",
    message="This is a Django SMTP delivery test.",
    from_email=settings.DEFAULT_FROM_EMAIL,
    recipient_list=[settings.CONTACT_EMAIL],
    fail_silently=False,
)
```

A return value of `1` means the email backend accepted one message for sending. Also check Inbox, Spam, and the sending account's Sent folder.

## Dependency Notes

The project currently uses `python-dotenv`, so `django-environ` is not required unless the project deliberately migrates to that package. Avoid maintaining two `.env` loaders.

`django-crispy-forms` and `crispy-bootstrap5` are optional. Add them only if the templates are changed to render forms through crispy tags and the corresponding applications are added to `INSTALLED_APPS`. The current SGnG contact template uses custom markup and `forms.css`, so crispy forms are not required for that layout.

## Security and Production Checklist

Before deployment:

- set `DEBUG=False`;
- create a unique production `SECRET_KEY`;
- configure the production hostname in `ALLOWED_HOSTS`;
- use the production database URL supplied by the host;
- store all secrets in the hosting platform's environment settings;
- configure static-file collection and serving;
- run `py manage.py collectstatic --noinput`;
- run `py manage.py check --deploy`;
- run the complete automated test suite;
- use test Stripe keys until payment functionality has been intentionally implemented and verified.

## Git Workflow

```powershell
git status
git add .
git commit -m "Configure environment-based email delivery and project documentation"
git push origin main
```

Before every push, verify that `.env` remains ignored:

```powershell
git check-ignore .env
```

The expected output is `.env`.

## Academic Context

This repository is the capstone project for FSDI Cohort 68 and supports work across FSDI 118-120. It demonstrates planning, architecture, implementation, responsive UX, validation, testing, API development, security preparation, and deployment readiness.

## Author

Timothy O. Strubell  
Strubell Publishing LLC  
Strubell Goods & Gear (SGnG)

## License

This academic capstone repository does not currently declare an open-source license. Unless a license is added, all rights remain reserved.
