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
    run = db.Column(db.String(12), nullable=False, unique=True)
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

    def __repr__(self):
        return f"<Evaluador {self.run}: {self.nombre_completo()}>"


class FormularioEDAN(db.Model):
    """
    Formulario EDAN de Salud Mental.

    Los datos de pasos 2-5 (factores, recursos, necesidades) se almacenan
    en la tabla `respuestas_edan` de forma normalizada.
    """

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

    # === PASO 1: DATOS GENERALES ===
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

    # === PASO 3: COMENTARIOS FACTORES PROTECTORES ===
    comentarios_informacion = db.Column(db.Text, nullable=True)
    otras_consideraciones = db.Column(db.Text, nullable=True)

    # === PASO 5: COMENTARIOS NECESIDADES ===
    comentarios_necesidades = db.Column(db.Text, nullable=True)

    # === PASO 6: SÍNTESIS ===
    sintesis_necesidades = db.Column(db.Text, nullable=True)
    acciones_realizar = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f"<FormularioEDAN {self.id[:8]}... estado={self.estado}>"

    def to_dict(self):
        """Convierte el formulario a diccionario."""
        return {
            "id": self.id,
            "evaluador_id": self.evaluador_id,
            "estado": self.estado,
            "paso_actual": self.paso_actual,
            "nivel_aplicacion": self.nivel_aplicacion,
            "fecha_informe": (
                self.fecha_informe.isoformat() if self.fecha_informe else None
            ),
            "comuna": self.comuna,
            "provincia": self.provincia,
            "tipo_suceso": self.tipo_suceso,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
