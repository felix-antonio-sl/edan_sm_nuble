"""
Tests para modelos EDAN.
"""

import pytest
from app.models import (
    Evaluador,
    FormularioEDAN,
    CatalogoEDAN,
    RespuestaEDAN,
    SeccionEDAN,
    ValorEscala,
)


class TestEvaluador:
    """Tests para el modelo Evaluador."""

    def test_crear_evaluador(self, session, evaluador_factory):
        """Test creación de evaluador."""
        evaluador = evaluador_factory(
            run="11.111.111-1", nombre="María", apellido1="González", apellido2="Pérez"
        )

        assert evaluador.id is not None
        assert evaluador.run == "11.111.111-1"
        assert evaluador.nombre == "María"

    def test_nombre_completo_con_apellido2(self, evaluador_factory):
        """Test nombre completo con ambos apellidos."""
        evaluador = evaluador_factory(
            nombre="Juan", apellido1="Pérez", apellido2="García"
        )

        assert evaluador.nombre_completo() == "Juan Pérez García"

    def test_nombre_completo_sin_apellido2(self, session):
        """Test nombre completo sin segundo apellido."""
        evaluador = Evaluador(
            run="22.222.222-2",
            nombre="Ana",
            apellido1="López",
            apellido2=None,
            establecimiento="Hospital Test",
        )
        session.add(evaluador)
        session.commit()

        assert evaluador.nombre_completo() == "Ana López"


class TestFormularioEDAN:
    """Tests para el modelo FormularioEDAN."""

    def test_crear_formulario(self, formulario_factory):
        """Test creación de formulario."""
        formulario = formulario_factory()

        assert formulario.id is not None
        assert formulario.estado == "borrador"
        assert formulario.paso_actual == 1

    def test_formulario_tiene_evaluador(self, formulario_factory, evaluador_factory):
        """Test relación formulario-evaluador."""
        evaluador = evaluador_factory(run="33.333.333-3")
        formulario = formulario_factory(evaluador=evaluador)

        assert formulario.evaluador_id == evaluador.id


class TestCatalogoEDAN:
    """Tests para el modelo CatalogoEDAN."""

    def test_get_by_seccion(self, session, catalogo_items):
        """Test obtener ítems por sección."""
        items = CatalogoEDAN.get_by_seccion(SeccionEDAN.FACTORES_RIESGO)

        assert len(items) == 2
        assert all(i.seccion == SeccionEDAN.FACTORES_RIESGO for i in items)

    def test_items_ordenados(self, session, catalogo_items):
        """Test que ítems vienen ordenados."""
        items = CatalogoEDAN.get_by_seccion(SeccionEDAN.FACTORES_RIESGO)

        ordenes = [i.orden for i in items]
        assert ordenes == sorted(ordenes)


class TestRespuestaEDAN:
    """Tests para el modelo RespuestaEDAN."""

    def test_set_respuesta_escala(self, session, formulario_factory, catalogo_items):
        """Test guardar respuesta de escala."""
        formulario = formulario_factory()
        item = catalogo_items[0]  # FR01 - escala gravedad

        respuesta = RespuestaEDAN.set_respuesta(
            formulario_id=formulario.id,
            item_id=item.id,
            valor="G",
            tipo_respuesta="escala_gravedad",
        )
        session.commit()

        assert respuesta.valor_escala == ValorEscala.GRAVE
        assert respuesta.valor == "G"

    def test_set_respuesta_bool(self, session, formulario_factory, catalogo_items):
        """Test guardar respuesta booleana."""
        formulario = formulario_factory()
        item = catalogo_items[2]  # FP01 - booleano

        respuesta = RespuestaEDAN.set_respuesta(
            formulario_id=formulario.id,
            item_id=item.id,
            valor=True,
            tipo_respuesta="booleano",
        )
        session.commit()

        assert respuesta.valor_bool is True
        assert respuesta.valor is True

    def test_set_respuesta_cantidad(self, session, formulario_factory, catalogo_items):
        """Test guardar respuesta de cantidad."""
        formulario = formulario_factory()
        item = catalogo_items[3]  # RH01 - cantidad

        respuesta = RespuestaEDAN.set_respuesta(
            formulario_id=formulario.id,
            item_id=item.id,
            valor=5,
            tipo_respuesta="cantidad",
        )
        session.commit()

        assert respuesta.valor_cantidad == 5
        assert respuesta.valor == 5

    def test_update_respuesta_existente(
        self, session, formulario_factory, catalogo_items
    ):
        """Test actualizar respuesta existente."""
        formulario = formulario_factory()
        item = catalogo_items[0]

        # Primera respuesta
        RespuestaEDAN.set_respuesta(
            formulario_id=formulario.id,
            item_id=item.id,
            valor="G",
            tipo_respuesta="escala_gravedad",
        )
        session.commit()

        # Actualizar
        RespuestaEDAN.set_respuesta(
            formulario_id=formulario.id,
            item_id=item.id,
            valor="M",
            tipo_respuesta="escala_gravedad",
        )
        session.commit()

        # Verificar que solo hay una respuesta
        count = RespuestaEDAN.query.filter_by(
            formulario_id=formulario.id, item_id=item.id
        ).count()

        assert count == 1

        respuesta = RespuestaEDAN.query.filter_by(
            formulario_id=formulario.id, item_id=item.id
        ).first()

        assert respuesta.valor_escala == ValorEscala.MEDIO
