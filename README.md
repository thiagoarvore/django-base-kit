# django-base-kit

A bootstrap library for Django projects with:

- an abstract `BaseModel` using UUID v4 as the primary key
- a custom `User` model (`AbstractUser` + `BaseModel`)
- ready-to-use authentication views and templates:
  - login
  - logout
  - change password
  - password reset ("forgot password")

## Installation

```bash
pip install django-base-kit
```

## What this package provides

### 1) Reusable BaseModel

File: `django_base_kit.models.BaseModel`

Included fields:

- `id` (`UUIDField`, `primary_key=True`, `default=uuid.uuid4`)
- `created_at`
- `updated_at`
- `active`
- `changelog`

Example usage in any app:

```python
from django.db import models
from django_base_kit.models import BaseModel


class Product(BaseModel):
    name = models.CharField(max_length=120)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name
```

### 2) Custom User model

File: `django_base_kit.models.User`

- inherits from `BaseModel`
- inherits from `AbstractUser`
- unique `email`
- model app label: `base_kit`

So in `settings.py`, use:

```python
AUTH_USER_MODEL = "base_kit.User"
```

### 3) Auth stack (views + forms + templates)

The package already includes forms, views, and templates for:

- login
- logout
- change password
- password reset (form, done, confirm, complete)

Routes are exposed through `django_base_kit.urls.user_urlpatterns`.

## Consumer project setup

### 1) `settings.py`

Add/update:

```python
INSTALLED_APPS = [
    # django apps...
    "auditlog",
    "widget_tweaks",
    "django_base_kit",
]

AUTH_USER_MODEL = "base_kit.User"

# Email sender used by password reset views
# The view reads FROM_MAIL and falls back to DEFAULT_FROM_EMAIL
FROM_MAIL = "no-reply@example.com"
DEFAULT_FROM_EMAIL = FROM_MAIL

# Local development (prints emails in the console)
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# Recommended so Django can find package templates
TEMPLATES = [
    {
        # ...
        "APP_DIRS": True,
    },
]

# Optional: override package templates and success_urls per view
BASE_KIT = {
    # success_urls configuration
    "signup_success_url": "/",
    "login_success_url": "/",
    "logout_success_url": "/accounts/login/",

    # templates configuration
    "signup_template": "my_auth/signup.html",
    "login_template": "my_auth/login.html",
    "change_password_template": "my_auth/change_password.html",
    "reset_password_template": "my_auth/reset_password_form.html",
    "reset_password_done_template": "my_auth/reset_password_done.html",
    "reset_password_confirm_template": "my_auth/reset_password_confirm.html",
    "reset_password_complete_template": "my_auth/reset_password_complete.html",
    "reset_password_email_template": "my_auth/reset_password_email.html",
}
```

If a key is omitted, the default template shipped with `django_base_kit` is used.

### 2) Auditlog integration

To enable audit logs in consumer projects:

1. Make sure `auditlog` is installed and enabled in `INSTALLED_APPS`.

2. Add middleware in `settings.py`:

```python
MIDDLEWARE = [
    # ...
    "auditlog.middleware.AuditlogMiddleware",
]
```

3. In your model files, import and register the model:

```python
from auditlog.registry import auditlog


class MyModel(BaseModel):
    # your fields...
    pass


auditlog.register(MyModel)
```

### 3) Project `urls.py`

```python
from django.contrib import admin
from django.urls import path
from django_base_kit.urls import user_urlpatterns

urlpatterns = [
    path("admin/", admin.site.urls),
] + user_urlpatterns
```

### 4) Base template requirement (`base.html`)

The package templates use:

```django
{% extends "base.html" %}
```

So your project must provide a `base.html` template.

Minimal example:

```html
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{% block title %}My Project{% endblock %}</title>
</head>
<body>
  {% block content %}{% endblock %}
</body>
</html>
```

Recommended location:

- `templates/base.html` in your Django project (with your `TEMPLATES` setting pointing to this directory), or
- any template directory already configured in your project.

### 5) Migrations

In a new project:

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

## Available routes

- `/accounts/signup/`
- `/accounts/login/`
- `/accounts/logout/`
- `/change_password/`
- `/reset_password/`
- `/reset_password/done`
- `/reset_password/confirm/<uidb64>/<token>/`
- `/reset_password/complete/`

## Important notes

- Set `AUTH_USER_MODEL = "base_kit.User"` before your first migration.
- If your project already migrated with `auth.User`, you will need a user migration plan.
- For password reset in production, configure SMTP (`EMAIL_HOST`, `EMAIL_PORT`, `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`, `EMAIL_USE_TLS/SSL`).

## License

MIT
