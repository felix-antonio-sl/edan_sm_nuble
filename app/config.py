"""
Configuración de la aplicación EDAN.
"""

import os
from datetime import timedelta


class Config:
    """Configuración base."""

    # Flask
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-key-change-me")

    # SQLAlchemy
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL", "postgresql://edan:edan_secret@localhost:5432/edan_db"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,
        "pool_recycle": 300,
    }

    # Sesión
    PERMANENT_SESSION_LIFETIME = timedelta(hours=24)
    SESSION_COOKIE_SECURE = False  # True en producción con HTTPS
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"


class DevelopmentConfig(Config):
    """Configuración de desarrollo."""

    DEBUG = True
    SQLALCHEMY_ECHO = True  # Log de queries SQL


class ProductionConfig(Config):
    """Configuración de producción."""

    DEBUG = False
    SESSION_COOKIE_SECURE = True

    # Asegurar que SECRET_KEY está configurado
    @classmethod
    def init_app(cls, app):
        if app.config["SECRET_KEY"] == "dev-key-change-me":
            raise ValueError("SECRET_KEY no configurado para producción")


class TestingConfig(Config):
    """Configuración para tests."""

    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    WTF_CSRF_ENABLED = False


# Mapeo de nombres de entorno a clases
config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig,
    "default": DevelopmentConfig,
}


def get_config():
    """Obtiene la configuración según FLASK_ENV."""
    env = os.environ.get("FLASK_ENV", "production")
    return config.get(env, config["default"])
