"""
EDAN Salud Mental - Aplicación Flask
Colaboración GORE Ñuble / Servicio de Salud Ñuble
Contexto: Incendios Región de Ñuble 2026
"""

import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()


def create_app():
    """Factory de la aplicación Flask."""
    app = Flask(__name__)

    # Configuración
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-key-change-me")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
        "DATABASE_URL", "postgresql://edan:edan_secret@localhost:5432/edan_db"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Inicializar extensiones
    db.init_app(app)
    migrate.init_app(app, db)

    # Registrar blueprints
    from app.routes import formulario

    app.register_blueprint(formulario.bp)

    # Crear tablas si no existen
    with app.app_context():
        try:
            db.create_all()
        except Exception as e:
            # Las tablas ya existen, ignorar
            app.logger.info(f"Tablas ya existentes o error de inicialización: {e}")

    return app
