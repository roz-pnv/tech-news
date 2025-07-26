from pathlib import Path
import os
import environ

BASE_DIR = Path(__file__).resolve().parent.parent.parent
env = environ.Env()
environ.Env.read_env(BASE_DIR / '.env')

SECRET_KEY = env('SECRET_KEY')

# Application definition
INSTALLED_APPS = [
	'rest_framework',
    'djoser',
	'django_filters',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
	'django_celery_beat',
	'django_celery_results',
	'drf_spectacular',
	'news.apps.NewsConfig',
	'scraper_control.apps.ScraperControlConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

REST_FRAMEWORK = {
	'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ],
	"DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend"
    ],
	'DEFAULT_SCHEMA_CLASS':
        'drf_spectacular.openapi.AutoSchema',
}

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

MEDIA_URL = '/media/'

MEDIA_ROOT = BASE_DIR / 'media'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = 'static/'

STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

STATIC_ROOT = BASE_DIR / 'staticfiles'

STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# save Celery task results in Django's database
CELERY_RESULT_BACKEND = "django-db"

# store additional task metadata like name, args, retries (only works with supported result backends)
CELERY_RESULT_EXTENDED = True

# broker_connection_retry_on_startup
CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True

# This configures Redis as the datastore between Django + Celery
CELERY_BROKER_URL = os.environ.get("CELERY_BROKER", "redis://redis:6379/0")

# this allows you to schedule items in the Django admin.
CELERY_BEAT_SCHEDULER = "django_celery_beat.schedulers.DatabaseScheduler"

SPECTACULAR_SETTINGS = {
    'TITLE': 'TechNews REST API',
    'DESCRIPTION': (
        "TechNews is a Django project that collects, filters, and shares tech news through a secure API. It’s built in a way that makes it easy to maintain, automate, and scale over time.\n\n"
        "• API Setup:\n\n"
        "  Users can search news by tags or keywords. The API uses JWT (via Djoser) to keep things secure, and has extra tools like slug generation, file/media support, and access control based on user roles. "
        "Everything is well tested, and there are different settings for development, testing, and production.\n\n"
        "• News Gathering:\n\n"
        "  Scrapy and Selenium work together to get articles from websites like Zoomit. Persian dates are converted with a custom tool, duplicates are skipped, and only complete news posts are saved and shown. "
        "All images from each article—including embedded visuals and cover images—are collected, saved to the database, and included in API responses.\n\n"
        "• Automation & Background Tasks:\n\n"
        "  Celery runs scraping tasks in the background, and Celery Beat sets the schedule. Redis handles message passing, and Flower gives a dashboard to see how tasks are doing. "
        "Everything runs inside Docker containers—including Django, Celery, Redis, Flower—so it’s easy to deploy and update.\n\n"
    ),
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': True,
}

