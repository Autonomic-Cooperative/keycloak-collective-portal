"""Application configuraiton."""

import logging
from os import environ
from pathlib import Path

# Application secret key, used for the SessionMiddleware
APP_SECRET_KEY = environ.get("APP_SECRET_KEY")

# Keycloak client details
KEYCLOAK_CLIENT_ID = environ.get("KEYCLOAK_CLIENT_ID")
KEYCLOAK_CLIENT_SECRET = environ.get("KEYCLOAK_CLIENT_SECRET")
KEYCLOAK_DOMAIN = environ.get("KEYCLOAK_DOMAIN")
KEYCLOAK_REALM = environ.get("KEYCLOAK_REALM")
KEYCLOAK_SCOPES = environ.get("KEYCLOAK_SCOPES", "openid profile email")
KEYCLOAK_BASE_URL = f"https://{KEYCLOAK_DOMAIN}/auth/realms/{KEYCLOAK_REALM}/protocol/openid-connect"  # noqa

# Redis connection details, our main storage
REDIS_DB = environ.get("REDIS_DB")
REDIS_HOST = environ.get("REDIS_HOST")
REDIS_PORT = environ.get("REDIS_PORT")

# How many days do we want the invites to be valid for?
INVITE_TIME_LIMIT = int(environ.get("INVITE_TIME_LIMIT", 30))

# Static and template configuration
STATIC_DIR = Path(".").absolute() / "keycloak_collective_portal" / "static"
TEMPLATE_DIR = Path(".").absolute() / "keycloak_collective_portal" / "templates"

# Theme selection
APP_THEME = environ.get("APP_THEME", "default")

# Log level
LOG_LEVEL = environ.get("APP_LOG_LEVEL", "info")
if LOG_LEVEL == "info":
    APP_LOG_LEVEL = logging.INFO
elif LOG_LEVEL == "debug":
    APP_LOG_LEVEL = logging.DEBUG
else:
    APP_LOG_LEVEL = logging.INFO

# Automatically log folks in or show the default log in page?
AUTOMATICALLY_LOG_IN = environ.get("AUTOMATICALLY_LOG_IN", False)
