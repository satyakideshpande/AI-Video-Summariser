import os
import firebase_admin
from firebase_admin import credentials
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Secret Key (Replace with an environment variable in production)
SECRET_KEY = 'your-secret-key'

# Debug mode (Set to False in production)
DEBUG = True

# Allow all hosts for now (Change for production)
ALLOWED_HOSTS = ['*']

# Installed apps
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',

    # Your Django apps
    'video_summarizer',  # Update with your actual app name
    'api',
    
    # Third-party apps
    'rest_framework',
    'drf_yasg',  # Swagger for API documentation
]

# Middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',  # Ensure this is before CommonMiddleware
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# CORS Settings
CORS_ALLOW_ALL_ORIGINS = True  # Allow all frontend origins (for testing)

# If you want to restrict it to only your React app, use:
# CORS_ALLOWED_ORIGINS = [
#     "http://localhost:3000",  # React development server
# ]

# Root URL configuration
ROOT_URLCONF = 'video_summarizer.urls'

# Templates Configuration (Fix for admin panel)
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],  # Create a templates folder if needed
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

# WSGI Application
WSGI_APPLICATION = 'video_summarizer.wsgi.application'

# Database Configuration (SQLite for now, change to PostgreSQL/MySQL in production)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'video_processing',
        'USER': 'db_name',
        'PASSWORD': 'db_password',
        'HOST': 'localhost',  # Or your PostgreSQL server's IP address or hostname
        'PORT': '5432',  # Or your PostgreSQL server's port number
    }
}

# Firebase Configuration
#Create a firebase_credentials file in the project with your credentials
FIREBASE_CRED_PATH = os.path.join(BASE_DIR, 'firebase_credentials.json')

if not os.path.exists(FIREBASE_CRED_PATH):
    raise FileNotFoundError(f"Firebase credentials file not found at {FIREBASE_CRED_PATH}")

cred = credentials.Certificate(FIREBASE_CRED_PATH)
firebase_admin.initialize_app(cred, {
    'storageBucket': "--your-storage-bucket--name"
})

# Static Files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Django REST Framework settings
REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema'
}

# Swagger Configuration
SWAGGER_SETTINGS = {
    'USE_SESSION_AUTH': False,
    'SECURITY_DEFINITIONS': {
        'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header'
        }
    },
    'JSON_EDITOR': True,
}
