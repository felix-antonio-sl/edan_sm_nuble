"""
Modelo de catálogo EDAN - Ítems evaluables del instrumento.
"""

from app import db
from app.models.enums import SeccionEDAN, TipoRespuesta


class CatalogoEDAN(db.Model):
    """Catálogo de ítems evaluables del instrumento EDAN."""

    __tablename__ = "catalogo_edan"

    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(
        db.String(10), unique=True, nullable=False
    )  # "FR01", "FP01", etc.
    seccion = db.Column(db.Enum(SeccionEDAN), nullable=False, index=True)
    descripcion = db.Column(db.String(500), nullable=False)
    tipo_respuesta = db.Column(db.Enum(TipoRespuesta), nullable=False)
    orden = db.Column(db.Integer, nullable=False)
    activo = db.Column(db.Boolean, default=True)

    # Constraint de unicidad compuesto
    __table_args__ = (db.UniqueConstraint("seccion", "orden", name="uq_seccion_orden"),)

    def __repr__(self):
        return f"<CatalogoEDAN {self.codigo}: {self.descripcion[:30]}...>"

    @classmethod
    def get_by_seccion(cls, seccion: SeccionEDAN):
        """Obtiene todos los ítems activos de una sección ordenados."""
        return (
            cls.query.filter_by(seccion=seccion, activo=True).order_by(cls.orden).all()
        )
