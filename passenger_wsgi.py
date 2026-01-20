import sys
import os

# Agregamos el directorio actual al path de Python para que pueda encontrar el módulo 'app'
sys.path.insert(0, os.path.dirname(__file__))

from app import create_app

# Passenger (el gestor de cPanel) busca por defecto un objeto llamado 'application'
application = create_app()
