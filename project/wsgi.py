"""
WSGI config for project project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""

import os, django
from django.conf import settings
from django.core.wsgi import get_wsgi_application
from fastapi.applications import FastAPI
from fastapi.middleware.wsgi import WSGIMiddleware
from starlette.middleware.cors import CORSMiddleware


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

# https://docs.djangoproject.com/en/3.2/topics/settings/#calling-django-setup-is-required-for-standalone-django-usage
# to load your settings and populate Django’s application registry. 
django.setup()

# ----------------------------------------------FASTAPI CONFIG---------------------------------------------------

# Some metadata
app = FastAPI(
    title=settings.API_NAME,
    description=settings.API_DESCRIPTION,
    version=settings.API_VERSION,
    docs_url=settings.API_DOCS_URL,
    redoc_url=settings.API_REDOC_URL)

# CORS backend is in a different "origin" than the frontend.
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_HOSTS or ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Yours routers (API)
from book.routers import router_book
app.include_router(router_book)

# "Mounting" means adding a completely "independent" application in a specific path, 
# that then takes care of handling everything under that path, with the path 
# operations declared in that sub-application.

# Now, every request under the path 'PREFIX_MOUNT' will be handled by the django application.
# https://fastapi.tiangolo.com/advanced/wsgi/
app.mount(settings.PREFIX_MOUNT, WSGIMiddleware(get_wsgi_application()))

application = app
