"""
Django settings for social_network project.

Generated by 'django-admin startproject' using Django 4.2.4.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
import os
import environ


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-x4c^a-v0ckmzu(+*w@nd66c9ue=5nek3is@=qb*3r%*02qcyh-'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'api',
    'rest_framework',
    'user',
    'friends',
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

ROOT_URLCONF = 'social_network.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'social_network.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'socialnetwork',
        'USER': 'test',
        'PASSWORD': 'test',
        'HOST': 'db', #localhost
        'PORT': '3306',
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

AUTHENTICATION_BACKENDS = ['user.backends.EmailBackend']

JWT_PUBLIC_KEY = env("JWT_PUBLIC_KEY", default='-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAthgLNpQTVhrmN0N/diaI\ntJJpk/MFMCrJnPOsiXyGKHrB5hkSL9hWoQ5yUG9M9QXXAE29xg9hnLOswDTOGHDH\ngkz76cLp3NJ5mcXQcZKj67/vIszhgqMW49tXpOaPUdODlPoSMXJIRj4J5NY4H1Hl\n5E0duRUQuKjAuhCILDHWpSr07hC7g+FTWklrpJs6drM2wDnQ++6RAQ2kqMEiHjg1\nGjRs90J8QhFI15zoR3h9USkSx2r+zzkVyUsrQ5kNtFoSKBtbJQTnJXMy0Ry4Rhqv\nTSZJ+dp0s/T58Lf5A9E6+hIsydSLnHpood9ozI9zJOBcpbfBAtBfFk5247X0oyjb\nAQIDAQAB\n-----END PUBLIC KEY-----')
JWT_PRIVATE_KEY = env("JWT_PRIVATE_KEY", default='-----BEGIN RSA PRIVATE KEY-----\nMIIEogIBAAKCAQEAthgLNpQTVhrmN0N/diaItJJpk/MFMCrJnPOsiXyGKHrB5hkS\nL9hWoQ5yUG9M9QXXAE29xg9hnLOswDTOGHDHgkz76cLp3NJ5mcXQcZKj67/vIszh\ngqMW49tXpOaPUdODlPoSMXJIRj4J5NY4H1Hl5E0duRUQuKjAuhCILDHWpSr07hC7\ng+FTWklrpJs6drM2wDnQ++6RAQ2kqMEiHjg1GjRs90J8QhFI15zoR3h9USkSx2r+\nzzkVyUsrQ5kNtFoSKBtbJQTnJXMy0Ry4RhqvTSZJ+dp0s/T58Lf5A9E6+hIsydSL\nnHpood9ozI9zJOBcpbfBAtBfFk5247X0oyjbAQIDAQABAoIBAAVUxbCFSB4E5WdC\nHCtepkFE4Xdc4bqo4IhmSg+IBj6ddjN/Gbkt0A6430X5hbkNWM+t/v2zT+USTbce\nfqeQlvc6qzQLPkz+OqQa2nsGP0NG1izEb0Bjl2cgMgAaddEIQHucQQvKffkkPiZ5\ncvkABRs8mp+DaVcCLgsOgomac4+IIldHSelaU1w/akv98A20LHyuyuAFM3Lwd/no\nlmKhnAdKqYenZqlX1DMzvVjw+iUFS6ns3xP6omcsfA+UbT7orn20rwnUvEJ+ON1J\nl1jkKaECdiJAFVEqkPFdLb1krFOrrCs0FAlNzKvHGpILGeFhdihAudDn+1ZkZtFh\nJzHg4CECgYEAx4g/QIE29xVM4f+mv8hXpsrKIRc7jQSsYc5seNYlwdWvS320XADP\n8nnHjCyjTnYaBYWG7fege40bgCa2hZUTeil2/pc6OI1KKJEzmqWMHXBBaYeOAirx\neqxzjLFvyGJOATX9LuLGyxnMCwihQFGIjMnPIaczvF9aaNgjb6NVVeECgYEA6aBs\nZnT9QyfK8cjZATw/PjTmUi9Y58X4pO414ocvi1FWJN9YReOeeAF0cEGy4LqWNpWt\n+rBiHo2bA08WMqMU7IZCXRPHKMMZhyG3mz0DoOdzmDL+fZWVXP6pt/M+1Sq9TK/d\nUUq0H4qVFNa3SNjK8BkIHzAkpNU3dqgdL3vf6SECgYAz4GGJlM7EmL4feAdTj3Py\ngoDg75hlBpUG7NNY61xvs+3ac7lDvlZSVYUjFavzx1Lmopu9HQeVd89xlx8XRfYF\naehtMsZJU7q3J2FCUM5IDRqEpGCwgZe87D8ykiNc9uoO+Il1+jHzNibNq5W5Ejmt\nWP7IYh9aV3Q7FA7KhK24IQKBgGXwbdw259tJna/qZ2W2mBHYmzb5Gd3n8BpnJnP1\ncLVlhCUKn0W/kAHlAJ2KzTZps+mVXhiopeeW+jBzbcgiiJq76nEalCghGR5xg9/k\nu5SV6UZb2deKUWYGaJ+vL5dr0rWHdxZldjrdCTfSiJ7smYAyK+0P4K1bq5vGtxVl\nA8qBAoGAXtwzRAuC/LXK0Xffh2FDH4l/2KZCLpWSgvH6m1CGRJ2opMkKnk3KwaNk\nqmzm+ho4YjzbpbvFDxCZpPRBJ5ygPrLdtY3oCFwIPgSj3SgLSNl/wXTFGHhqw9MW\nWhqXJMIpa1NT7vblMY/FGEHptEyFmv5KAUnuCwW1wAF/rt0DdOk=\n-----END RSA PRIVATE KEY-----')


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_RATES': {
        'anon': '3/minute',
        'user': '3/minute'
    }
}