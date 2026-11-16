# Cinematic Strubell Goods & Gear Marketplace

**Repository:** `FSDI_Ch68_Capstone_Strubell`  
**Project:** Cinematic SGnG Marketplace  
**Academic Context:** FSDI Cohort 68 Capstone project  
**Current Milestone:** FSDI-119 Assignment 4 Final Report

## Project Overview

The **Cinematic Strubell Goods & Gear Marketplace** is a responsive full-stack Django application developed for Strubell Goods & Gear (SGnG). The project combines a cinematic branded interface with persistent Marketplace data, account workflows, protected product management, contact/email processing, legal-information pages, REST API support, responsive design, accessibility-aware interaction states, and automated Django and Selenium testing.

The project uses an integration-first approach. Existing Django architecture is retained when it satisfies the project requirement, while targeted enhancements are added when they improve maintainability, usability, verification, accessibility, or architectural clarity.

## Current Implemented Features

- Cinematic SGnG Home and About experiences
- Dedicated About pages for:
  - Military Service
  - Craftsmanship
  - Entrepreneurship
  - Software Development
- Clickable and keyboard-accessible About story cards
- Responsive founder/avatar presentation
- Persistent Category and Product data
- Marketplace listing and Product Detail workflows
- Product search and supported filtering
- User registration, login, and logout
- Authentication-aware navigation
- Staff-protected Product create, update, and delete workflows
- Django Admin support
- Read-only Django REST Framework endpoints
- Contact-form validation and configured email delivery
- Standalone Terms of Service and Privacy Policy pages
- Global legal-information footer navigation
- Responsive desktop, tablet, and mobile layouts
- Keyboard focus and accessibility-related interaction states
- Django application tests and Selenium browser-flow tests
- Git/GitHub version control and Trello project traceability

## Intentionally Deferred or Future Scope

The following items are not represented as completed functionality:

- JavaScript destructive-action modal enhancement
- Production payment/checkout implementation
- Final shipping, warranty, return, and refund policies
- Cookie consent/preference management
- Production legal review
- Performance metrics and user-behavior analytics
- Optional multilingual and user-selectable theme systems

The Stripe SDK is installed for possible future integration, but checkout is not claimed as implemented or verified.

## Technology Stack

- Python
- Django 6.1.2
- Django REST Framework
- HTML5
- CSS3
- Vanilla JavaScript
- SQLite for local development
- Environment-based database configuration through `dj-database-url`
- Pillow for image handling
- Selenium with Microsoft Edge for browser-level testing
- Gunicorn and WhiteNoise for production preparation
- Git and GitHub for version control
- Trello for Agile planning and traceability

## Repository Structure

```text
FSDI_Ch68_Capstone_Strubell/
├── accounts/                  # Registration, login, logout, account workflows
├── catalog/                   # Products, Marketplace, staff CRUD, and API
├── config/                    # Project settings and root URL configuration
├── contact/                   # Contact form, email workflow, and tests
├── media/                     # Development media files
├── pages/                     # Home, About, legal, and About-detail pages
│   ├── static/css/about.css
│   ├── templates/about/
│   │   ├── craftsmanship.html
│   │   ├── entrepreneurship.html
│   │   ├── military_service.html
│   │   └── software_development.html
│   └── templates/pages/
│       ├── about.html
│       ├── home.html
│       ├── privacy_policy.html
│       └── terms_of_service.html
├── static/                    # Shared CSS, JavaScript, images, and branding
├── templates/                 # Shared base template
├── tests/selenium/            # End-to-end browser-flow tests
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
py -m pip install -r requirements.txt
```

### 4. Create the local environment file

```powershell
Copy-Item .env.example .env
```

Replace the placeholders in `.env` with private local-development values. Never commit `.env`.

### 5. Apply migrations

```powershell
py manage.py migrate
```

### 6. Create a superuser

```powershell
py manage.py createsuperuser
```

### 7. Start the development server

```powershell
py manage.py runserver
```

Open `http://127.0.0.1:8000/` in a browser.

## Environment Variables

Use safe placeholders in `.env.example` and private values in `.env`.

```text
DEBUG=True
SECRET_KEY=replace-with-a-unique-local-secret-key
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

Generate a local Django secret key with:

```powershell
py -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Do not post or commit the generated key.

## Contact and Email Workflow

A valid Contact submission should:

- validate the visitor's name, email, subject, and message;
- send the formatted inquiry to `CONTACT_EMAIL`;
- use `DEFAULT_FROM_EMAIL` as the authenticated sender;
- use the visitor's address as `reply_to`;
- display success feedback only after successful processing; and
- preserve clear validation feedback when input or delivery fails.

Do not commit email passwords or Google App Passwords.

## Database Configuration

Local development uses:

```text
DATABASE_URL=sqlite:///db.sqlite3
```

A deployment platform may provide a PostgreSQL connection URL. Use the exact value supplied by the selected platform and store it through private environment settings.

## Testing and Verification

Activate the virtual environment before running commands.

### Configuration and migration checks

```powershell
py manage.py check
py manage.py makemigrations --check --dry-run
py manage.py migrate
```

### About-page Selenium tests

```powershell
py manage.py test tests.selenium.test_about_pages -v 2
```

### Focused Selenium modules

```powershell
py manage.py test tests.selenium.test_authentication_flow -v 2
py manage.py test tests.selenium.test_marketplace_flow -v 2
py manage.py test tests.selenium.test_product_management_flow -v 2
```

### Complete Selenium suite

```powershell
py manage.py test tests.selenium -v 2
```

### Application suites

```powershell
py manage.py test accounts -v 2
py manage.py test pages -v 2
py manage.py test contact -v 2
py manage.py test catalog -v 2
```

### Complete regression suite

```powershell
py manage.py test -v 2
```

The test count and elapsed time used in the Final Report must come from the same final successful complete-regression run.

## Static-File Verification

```powershell
py manage.py findstatic css/base.css
py manage.py findstatic css/home.css
py manage.py findstatic css/about.css
py manage.py findstatic css/forms.css
py manage.py findstatic css/legal.css
py manage.py findstatic css/marketplace.css
```

## Responsive and Accessibility Verification

Manually verify representative layouts at:

- Desktop: 1440 × 900
- Tablet: 768 × 1024
- Mobile: 390 × 844

Also verify:

- keyboard navigation with Tab and Shift+Tab;
- activation with Enter where applicable;
- visible `:focus-visible` styling;
- readable headings and text;
- usable forms and validation messages;
- no unintended horizontal scrolling; and
- functional About-page cards and return links.

## Security and Production Checklist

Before production deployment:

- set `DEBUG=False`;
- use a unique production `SECRET_KEY`;
- configure production `ALLOWED_HOSTS`;
- use the database URL supplied by the deployment platform;
- keep all secrets in private environment settings;
- run `py manage.py collectstatic --noinput`;
- run `py manage.py check --deploy`;
- run the complete automated test suite;
- use test Stripe keys until payment functionality is deliberately implemented and verified; and
- complete appropriate legal and policy review.

## Final Git Workflow

Before staging changes:

```powershell
git status
git check-ignore .env
git diff --stat
git diff
```

Stage and review:

```powershell
git add .
git status
git diff --cached --stat
git diff --cached
```

Commit and push:

```powershell
git commit -m "Finalize FSDI-119 Assignment 4 implementation and documentation"
git push origin main
```

Final checkpoint evidence:

```powershell
cls
git branch --show-current
git log -1 --oneline
git push origin main
git status
```

The final terminal evidence should show the active `main` branch, the latest commit, successful remote synchronization, and `nothing to commit, working tree clean`.

## Academic Context

This repository supports the FSDI Capstone sequence and documents planning, architecture, implementation, persistence, authentication, communication, API integration, responsive UX, accessibility, testing, Agile traceability, and controlled scope.

## Author

**Timothy O. Strubell**  
Strubell Publishing LLC  
Strubell Goods & Gear (SGnG)

## License

This academic Capstone repository does not currently declare an open-source license. Unless a license is added, all rights remain reserved.
