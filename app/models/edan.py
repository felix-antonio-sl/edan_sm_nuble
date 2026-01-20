"""
Modelos de base de datos para EDAN Salud Mental.
"""

import uuid
from datetime import datetime
from app import db


class Evaluador(db.Model):
    """Persona que completa el formulario EDAN."""

    __tablename__ = "evaluadores"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    run = db.Column(db.String(12), nullable=False)  # RUN chileno (ej: 12.345.678-9)
    nombre = db.Column(db.String(100), nullable=False)
    apellido1 = db.Column(db.String(100), nullable=False)
    apellido2 = db.Column(db.String(100), nullable=True)
    establecimiento = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relación con formularios
    formularios = db.relationship("FormularioEDAN", backref="evaluador", lazy=True)

    def nombre_completo(self):
        """Retorna nombre completo del evaluador."""
        if self.apellido2:
            return f"{self.nombre} {self.apellido1} {self.apellido2}"
        return f"{self.nombre} {self.apellido1}"


class FormularioEDAN(db.Model):
    """Formulario EDAN de Salud Mental."""

    __tablename__ = "formularios_edan"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    evaluador_id = db.Column(
        db.String(36), db.ForeignKey("evaluadores.id"), nullable=False
    )
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    # Estado del wizard
    estado = db.Column(db.String(20), default="borrador")  # borrador, completado
    paso_actual = db.Column(db.Integer, default=1)

    # === DATOS GENERALES ===
    nivel_aplicacion = db.Column(db.String(50), nullable=True)
    fecha_informe = db.Column(db.Date, nullable=True)
    hora_informe = db.Column(db.Time, nullable=True)
    responsable = db.Column(db.String(200), nullable=True)
    cargo_funcion = db.Column(db.String(200), nullable=True)
    institucion = db.Column(db.String(200), nullable=True)
    poblacion_estimada = db.Column(db.Integer, nullable=True)

    # Ubicación
    comuna = db.Column(db.String(100), nullable=True)
    provincia = db.Column(db.String(100), nullable=True)
    region = db.Column(db.String(100), default="Ñuble")

    # Evento
    fecha_suceso = db.Column(db.Date, nullable=True)
    tipo_suceso = db.Column(db.String(200), nullable=True)
    principales_danos = db.Column(db.Text, nullable=True)

    # === SECCIÓN 1: FACTORES DE RIESGO (JSONB) ===
    # Formato: {"1": "G", "2": "M", ...} donde G=Grave, M=Medio, B=Bajo, NE=No Existe
    factores_riesgo = db.Column(db.JSON, default=dict)

    # === SECCIÓN 2: FACTORES PROTECTORES (JSONB) ===
    # Formato: {"29": true, "30": false, ...}
    factores_protectores = db.Column(db.JSON, default=dict)
    comentarios_informacion = db.Column(db.Text, nullable=True)
    otras_consideraciones = db.Column(db.Text, nullable=True)

    # === SECCIÓN 3: RECURSOS ===
    # Humanos: {"40": 5, "41": 3, ...} (cantidades)
    recursos_humanos = db.Column(db.JSON, default=dict)
    # Materiales: {"50": true, "51": false, ...}
    recursos_materiales = db.Column(db.JSON, default=dict)
    # Económicos: {"55": true}
    recursos_economicos = db.Column(db.JSON, default=dict)

    # === SECCIÓN 4: NECESIDADES ===
    # Formato: {"56": "R", "57": "NR", ...} donde R=Resuelto, NR=No Resuelto
    necesidades_psicosociales = db.Column(db.JSON, default=dict)
    necesidades_institucionales = db.Column(db.JSON, default=dict)
    necesidades_basicas = db.Column(db.JSON, default=dict)
    comentarios_necesidades = db.Column(db.Text, nullable=True)

    # === SÍNTESIS ===
    sintesis_necesidades = db.Column(db.Text, nullable=True)
    acciones_realizar = db.Column(db.Text, nullable=True)

    def to_dict(self):
        """Convierte el formulario a diccionario."""
        return {
            "id": self.id,
            "estado": self.estado,
            "paso_actual": self.paso_actual,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
