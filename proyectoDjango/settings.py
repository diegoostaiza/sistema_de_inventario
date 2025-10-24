from pathlib import Path
import os, dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-uc%@3eryznu!j7b#9kv@ns^d&gxs)@!azckzg**f7gl8=1m@-1')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'

ALLOWED_HOSTS = [
    '.railway.app',
    '127.0.0.1', 
    'localhost',
    '0.0.0.0'
]

# Application definition
THIRD_APPS = [
    'django_filters',
    'crispy_forms',
    'crispy_bootstrap5',
    'whitenoise.runserver_nostatic',
    'cloudinary_storage',  # Añadir Cloudinary
    'cloudinary',          # Añadir Cloudinary
]

LOCAL_APPS = [
    'apps.dashboard.apps.DashboardConfig',
    'apps.authentication.apps.AuthenticationConfig',
    'apps.empresa.apps.EmpresaConfig',
    'apps.articulos.apps.ArticulosConfig',
    'apps.categorias.apps.CategoriasConfig',
    'apps.clientes.apps.ClientesConfig',
    'apps.proveedores.apps.ProveedoresConfig',
    'apps.ventas.apps.VentasConfig',
    'apps.compras.apps.ComprasConfig',
    'apps.usuarios.apps.UsuariosConfig',
    'apps.roles.apps.RolesConfig',
    'apps.lotes.apps.LotesConfig',
    'apps.notificaciones.apps.NotificacionesConfig',
    'apps.informe.apps.InformeConfig',
]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
] + THIRD_APPS + LOCAL_APPS


CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

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

ROOT_URLCONF = 'proyectoDjango.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates'),
                 os.path.join(BASE_DIR, 'templates/errors'),],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'apps.notificaciones.context_processors.notificaciones',
            ],
        },
    },
]

WSGI_APPLICATION = 'proyectoDjango.wsgi.application'

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

# Configuración para Railway
DATABASES = {
    'default': dj_database_url.config(
        default=os.environ.get('DATABASE_URL'),
        conn_max_age=600,
        conn_health_checks=True,
    )
}

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators
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
# https://docs.djangoproject.com/en/5.0/topics/i18n/
LANGUAGE_CODE = 'es'
TIME_ZONE = 'America/Guayaquil'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/
STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# --- CONFIGURACIÓN DE CLOUDINARY ---
import cloudinary
import cloudinary.uploader
import cloudinary.api

# Configuración principal de Cloudinary
cloudinary.config(
    cloud_name=os.environ.get('CLOUDINARY_CLOUD_NAME'),
    api_key=os.environ.get('CLOUDINARY_API_KEY'),
    api_secret=os.environ.get('CLOUDINARY_API_SECRET'),
    secure=True
)

# Configuración para django-cloudinary-storage
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': os.environ.get('CLOUDINARY_CLOUD_NAME'),
    'API_KEY': os.environ.get('CLOUDINARY_API_KEY'),
    'API_SECRET': os.environ.get('CLOUDINARY_API_SECRET'),
}

# Usar Cloudinary para archivos multimedia
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

# Opcional: Si quieres mantener la URL /media/ para compatibilidad
MEDIA_URL = '/media/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField' 

# Configuracion reset password
EMAIL_BACKEND = os.environ.get('EMAIL_BACKEND', 'django.core.mail.backends.smtp.EmailBackend')
EMAIL_HOST = os.environ.get('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_PORT = os.environ.get('EMAIL_PORT', 587)
EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS', True)
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', 'cjmm227@gmail.com')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', 'wkdj qgeo ksjg qscm')

# Variables de redireccion
LOGIN_REDIRECT_URL = 'authentication:login'
LOGOUT_REDIRECT_URL = 'authentication:login'

# Convertidores boostrap
CRISPY_CLASS_CONVERTERS = {
    'textinput': 'form-control',
    'fileinput': 'form-control-file',
    'select': 'custom-select',
    'numberinput': 'form-control',
}

#Duración de la sesión en segundos (120 minutos)
SESSION_COOKIE_AGE = 7200
SESSION_SAVE_EVERY_REQUEST = True

# Usar models de usuario personalizado
AUTH_USER_MODEL = 'usuarios.CustomUser'

# Configuraciones de CELERY (deshabilitar temporalmente para Railway)
CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL', '')  # Vacío para deshabilitar
CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND', '')
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'America/Guayaquil'

# Seguridad en producción
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')