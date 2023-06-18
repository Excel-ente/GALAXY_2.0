"""
Django settings for zeta project.

Generated by 'django-admin startproject' using Django 4.2.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-f_7j+nblg!c6w4*l7+&6ebfa+_zi0-ce*jha&%e@orm5$ea_*c'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'simpleui',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'administracion',
    'import_export',
]



MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'zeta.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'administracion', 'templates'),  # Agrega esta línea
        ],
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


WSGI_APPLICATION = 'zeta.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'es-ar'

TIME_ZONE = 'America/Argentina/Buenos_Aires'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'

STATIC_ROOT=os.path.join(BASE_DIR, 'static')

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_REDIRECT_URL = '/'


# Emoticones del menú de UI
SIMPLEUI_CONFIG = {
    
    'system_keep': True,
    'menu_display': ['Materiales', 'Presupuestos', 'Pedidos Entregados','Gastos Fijos', 'Gastos Adicionales','Clientes', 'Proveedores',],
    'dynamic': True,
    'font_url': 'https://fonts.googleapis.com/css2?family=Poppins:wght@400;700&display=swap',
    'menus': [
        {
            'name': 'Presupuestos',
            'icon': 'fas fa-clipboard-list',
            'url': 'administracion/receta/',
            'newTab': False,
        },
        {
            'name': 'Materiales',
            'icon': 'fas fa-cubes',
            'url': 'administracion/insumo/',
            'newTab': False,
        },
        {
            'name': 'Clientes',
            'icon': 'fas fa-user',
            'url': 'administracion/cliente',
            'newTab': False,
        },
        {
            'name': 'Proveedores',
            'icon': 'fas fa-users',
            'url': 'administracion/proveedor/',
            'newTab': False,
        },
        {
            'name': 'Gastos Fijos',
            'icon': 'fa fa-file-invoice-dollar',
            'url': 'administracion/gastosfijos/',
            'newTab': False,
        },
        {
            'name': 'Gastos Adicionales',
            'icon': 'fas fa-dollar',
            'url': 'administracion/gastosadicionales/',
            'newTab': False,
        },
        {
            'name': 'Pedidos Entregados',
            'icon': 'fas fa-dolly',
            'url': 'administracion/pedidosentregados/',
            'newTab': False,
        }
    ]
}

SIMPLEUI_HOME_INFO = {
    'title': 'Galaxy 2.0',
    'author': 'Kevin Turkienich',
    'description': 'Aplicacion desarrollada en Django/Python para la gestion de presupuestos para un emprendimiento.',
    'home': 'https://www.linkedin.com/in/kevinturkienich/',
    'github': 'https://github.com/tunombre',
}

SIMPLEUI_HOME_PAGE = False#SIMPLEUI_HOME_INFO.get('home')

SIMPLEUI_ANALYSIS = False

SIMPLEUI_STATIC_OFFLINE = True

SIMPLEUI_HOME_ACTION =  True