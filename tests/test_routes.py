"""
Tests de integración para rutas de formulario.
"""

import pytest
from app.models import (
    Evaluador,
    FormularioEDAN,
    CatalogoEDAN,
    SeccionEDAN,
    TipoRespuesta,
)


class TestFormularioRoutes:
    """Tests para flujos de formulario."""

    def test_index_route(self, client):
        """Test carga de página de inicio."""
        response = client.get("/")
        assert response.status_code == 200
        assert b"EDAN Salud Mental" in response.data

    def test_iniciar_evaluacion(self, client, session):
        """Test inicio de evaluación crea evaluador y formulario."""
        data = {
            "run": "99.999.999-9",
            "nombre": "Tester",
            "apellido1": "Integration",
            "apellido2": "Route",
            "establecimiento": "Test Hospital",
        }

        response = client.post("/iniciar", data=data, follow_redirects=True)
        assert response.status_code == 200

        # Verificar BD
        evaluador = Evaluador.query.filter_by(run="99.999.999-9").first()
        assert evaluador is not None
        assert evaluador.nombre == "Tester"

        formulario = FormularioEDAN.query.filter_by(evaluador_id=evaluador.id).first()
        assert formulario is not None
        assert formulario.paso_actual == 1

    def test_flujo_paso1_guardado(self, client, session, evaluador_factory):
        """Test guardado de paso 1."""
        # 1. Setup inicial
        evaluador = evaluador_factory(run="88.888.888-8")

        # Simulamos POST a /iniciar para setear sesión
        with client.session_transaction() as sess:
            # Crear formulario manualmente para el test
            formulario = FormularioEDAN(evaluador_id=evaluador.id)
            session.add(formulario)
            session.commit()

            sess["evaluador_id"] = evaluador.id
            sess["formulario_id"] = formulario.id

        # 2. Enviar datos Paso 1
        data = {
            "nivel_aplicacion": "regional",
            "fecha_informe": "2026-01-20",
            "responsable": "Auto Tester",
            "comuna": "Chillán",
            "tipo_suceso": "Incendio",
            "accion": "siguiente",
        }

        response = client.post("/paso/1", data=data, follow_redirects=True)
        assert response.status_code == 200
        assert b"Factores de Riesgo" in response.data  # Verifica que avanzó al paso 2

        # 3. Verificar persistencia
        session.refresh(formulario)
        assert formulario.comuna == "Chillán"
        assert formulario.tipo_suceso == "Incendio"
        assert formulario.paso_actual == 2

    def test_flujo_paso2_respuestas_dinamicas(
        self, client, session, evaluador_factory, catalogo_items
    ):
        """Test guardado de respuestas dinámicas en paso 2."""
        # Setup
        formulario = FormularioEDAN(evaluador_id=evaluador_factory().id, paso_actual=2)
        session.add(formulario)
        session.commit()

        # Item de prueba creado en catalogo_items fixture: FR01
        item_codigo = catalogo_items[0].codigo  # FR01

        with client.session_transaction() as sess:
            sess["formulario_id"] = formulario.id

        # Post data
        data = {f"item_{item_codigo}": "G", "accion": "siguiente"}  # Grave

        response = client.post("/paso/2", data=data, follow_redirects=True)
        assert response.status_code == 200

        # Verificar avance y respuesta
        session.refresh(formulario)
        assert formulario.paso_actual == 3

        # Verificar respuesta normalizada
        from app.models import RespuestaEDAN, ValorEscala

        respuesta = (
            RespuestaEDAN.query.filter_by(formulario_id=formulario.id)
            .join(CatalogoEDAN)
            .filter(CatalogoEDAN.codigo == item_codigo)
            .first()
        )

        assert respuesta is not None
        assert respuesta.valor_escala == ValorEscala.GRAVE
