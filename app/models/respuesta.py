"""
Modelo de respuestas EDAN - Respuestas normalizadas a ítems del catálogo.
"""

from app import db
from app.models.enums import ValorEscala


class RespuestaEDAN(db.Model):
    """Respuesta individual a un ítem del catálogo EDAN."""

    __tablename__ = "respuestas_edan"

    id = db.Column(db.Integer, primary_key=True)
    formulario_id = db.Column(
        db.String(36),
        db.ForeignKey("formularios_edan.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    item_id = db.Column(db.Integer, db.ForeignKey("catalogo_edan.id"), nullable=False)

    # Campos de valor (solo uno será NOT NULL según tipo_respuesta)
    valor_escala = db.Column(db.Enum(ValorEscala), nullable=True)
    valor_bool = db.Column(db.Boolean, nullable=True)
    valor_cantidad = db.Column(db.Integer, nullable=True)

    # Relaciones
    formulario = db.relationship(
        "FormularioEDAN",
        backref=db.backref("respuestas", lazy="dynamic", cascade="all, delete-orphan"),
    )
    item = db.relationship("CatalogoEDAN")

    __table_args__ = (
        db.UniqueConstraint("formulario_id", "item_id", name="uq_respuesta_por_item"),
    )

    def __repr__(self):
        return f"<RespuestaEDAN form={self.formulario_id[:8]} item={self.item_id}>"

    @property
    def valor(self):
        """Retorna el valor de la respuesta según su tipo."""
        if self.valor_escala:
            return self.valor_escala.value
        if self.valor_bool is not None:
            return self.valor_bool
        if self.valor_cantidad is not None:
            return self.valor_cantidad
        return None

    @classmethod
    def set_respuesta(
        cls, formulario_id: str, item_id: int, valor, tipo_respuesta: str
    ):
        """Crea o actualiza una respuesta."""
        respuesta = cls.query.filter_by(
            formulario_id=formulario_id, item_id=item_id
        ).first()

        if not respuesta:
            respuesta = cls(formulario_id=formulario_id, item_id=item_id)
            db.session.add(respuesta)

        # Reset valores
        respuesta.valor_escala = None
        respuesta.valor_bool = None
        respuesta.valor_cantidad = None

        # Setear según tipo
        if tipo_respuesta in ("escala_gravedad", "escala_resolucion"):
            respuesta.valor_escala = ValorEscala(valor) if valor else None
        elif tipo_respuesta == "booleano":
            respuesta.valor_bool = valor
        elif tipo_respuesta == "cantidad":
            respuesta.valor_cantidad = int(valor) if valor else None

        return respuesta
