import os
import pandas as pd
from sqlalchemy import create_engine, text

# Configuración de conexión (usando variables de entorno o defaults de Docker)
DB_USER = os.getenv("POSTGRES_USER", "edan")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", "edan_secret")
DB_HOST = os.getenv("DB_HOST", "db")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("POSTGRES_DB", "edan_db")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

def get_engine():
    """Retorna el motor de conexión SQLAlchemy."""
    return create_engine(DATABASE_URL)

def load_data(query):
    """Carga datos desde la base de datos usando Pandas."""
    engine = get_engine()
    with engine.connect() as conn:
        return pd.read_sql(text(query), conn)

def get_kpis():
    """Obtiene KPIs generales."""
    total_formularios = load_data("SELECT count(*) as total FROM formularios_edan").iloc[0]['total']
    poblacion_afectada = load_data("SELECT sum(poblacion_estimada) as total FROM formularios_edan").iloc[0]['total']
    comunas_afectadas = load_data("SELECT count(distinct comuna) as total FROM formularios_edan").iloc[0]['total']
    
    return {
        "formularios": total_formularios,
        "poblacion": poblacion_afectada if poblacion_afectada else 0,
        "comunas": comunas_afectadas
    }
