"""Contains the Flask configuration."""
from datetime import timedelta
from os import environ, path

from dotenv import load_dotenv

# Contains the path of the module containing this file
project_root_dir = path.abspath(path.dirname(__file__))

# Loads the environment variables contained in the .env file
load_dotenv(path.join(project_root_dir, ".env"))


class BaseConfig:
    """Sets the basic Flask configuration variables."""

    # Basic Configurations
    SECRET_KEY = environ.get("SECRET_KEY", "Default Secret Key")
    SESSION_COOKIE_NAME = environ.get(
        "SESSION_COOKIE_NAME", "Default Session Cookie Name"
    )
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=5)

    # Database Configurations
    DATABASE_NAME = environ.get("DATABASE_NAME", "default.db")
    SQLALCHEMY_DATABASE_URI = environ.get(
        "SQLALCHEMY_DATABASE_URI", f"sqlite:///${DATABASE_NAME}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(BaseConfig):
    """Optimizes the Flask configuration variables for a development
    environment."""

    TESTING = True


class ProductionConfig(BaseConfig):
    """Optimizes the Flask configuration variables for a production
    environment."""

    TESTING = False
