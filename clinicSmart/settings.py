import os
from pathlib import Path
from django.contrib import messages
import dj_database_url

# Load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # Silently ignore if python-dotenv not available

# Build paths
BASE_DIR = Path(__file__).resolve().parent.parent

# Security - Production secret key (NEVER commit this to version control)
# For development, use a different key in .env file
SECRET_KEY = os.environ.get('SECRET_KEY', 'y@_k9q=+f9v7!t$b8^7m$#5z!*6@5!8j+@u6k%7!x@$j5+9!')

DEBUG = os.environ.get('DEBUG', 'False') == 'True'
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '*').split(',')
# Assurez-vous que STATIC_URL est bien défini AVANT l'import des apps
STATIC_URL = '/static/'  # Doit être avant INSTALLED_APPS

# Configuration TinyMCE explicite
TINYMCE_JS_URL = f"{STATIC_URL}tinymce/tinymce.min.js"  # Force le chemin
TINYMCE_COMPRESSOR = False
TINYMCE_DEFAULT_CONFIG = {
    'theme': 'silver',
    'height': 500,
    'menubar': False,
    'plugins': 'link image code',
    'toolbar': 'undo redo | formatselect | bold italic | alignleft aligncenter alignright | bullist numlist | link image code'
}

# Application definition
INSTALLED_APPS = [
    'django.contrib.postgres',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Third-party
    'tinymce',
    'widget_tweaks',
    'django_cleanup.apps.CleanupConfig',
    'django_extensions',
    'whitenoise.runserver_nostatic',
    
    # Local apps
    'first_app.apps.FirstAppConfig',
    'consultation.apps.ConsultationConfig',
    'statchart.apps.StatchartConfig',
    'appcon.apps.AppconConfig',
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

ROOT_URLCONF = 'clinicSmart.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'clinicSmart.wsgi.application'

# Database
DATABASES = {
    'default': dj_database_url.config(
        default=os.environ.get('DATABASE_URL'),
        conn_max_age=600,
        conn_health_checks=True,
    )
}

# [Rest of your existing configuration remains exactly the same...]
# (Keep all your password validators, internationalization, 
# static files, authentication, and other settings exactly as they were)
