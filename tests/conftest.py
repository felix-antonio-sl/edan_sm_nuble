"""
Fixtures y configuración para tests de EDAN.
"""

import pytest
from app import create_app, db
from app.models import Evaluador, FormularioEDAN, CatalogoEDAN, RespuestaEDAN
from app.models.enums import SeccionEDAN, TipoRespuesta


@pytest.fixture(scope="session")
def app():
    """Crea instancia de la aplicación para tests."""
    app = create_app()
    app.config.update(
        {
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
            "WTF_CSRF_ENABLED": False,
        }
    )

    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()


@pytest.fixture(scope="function")
def client(app):
    """Cliente de prueba para requests HTTP."""
    return app.test_client()


@pytest.fixture(scope="function")
def session(app):
    """Sesión de base de datos para tests."""
    from sqlalchemy.orm import scoped_session, sessionmaker

    with app.app_context():
        connection = db.engine.connect()
        transaction = connection.begin()

        # Crear session factory vinculada a la conexión
        session_factory = sessionmaker(bind=connection)
        session = scoped_session(session_factory)

        # Mocker la sesión global de SQLAlchemy con nuestra sesión transaccional
        db.session = session

        yield session

        transaction.rollback()
        connection.close()
        session.remove()


@pytest.fixture
def evaluador_factory(session):
    """Factory para crear evaluadores de prueba."""

    def _create_evaluador(
        run="12.345.678-9",
        nombre="Test",
        apellido1="Evaluador",
        apellido2="Prueba",
        establecimiento="CESFAM Test",
    ):
        evaluador = Evaluador(
            run=run,
            nombre=nombre,
            apellido1=apellido1,
            apellido2=apellido2,
            establecimiento=establecimiento,
        )
        session.add(evaluador)
        session.commit()
        return evaluador

    return _create_evaluador


@pytest.fixture
def formulario_factory(session, evaluador_factory):
    """Factory para crear formularios de prueba."""

    def _create_formulario(evaluador=None):
        if evaluador is None:
            evaluador = evaluador_factory()

        formulario = FormularioEDAN(evaluador_id=evaluador.id)
        session.add(formulario)
        session.commit()
        return formulario

    return _create_formulario


@pytest.fixture
def catalogo_items(session):
    """Crea ítems de catálogo mínimos para tests."""
    items = [
        CatalogoEDAN(
            codigo="FR01",
            seccion=SeccionEDAN.FACTORES_RIESGO,
            descripcion="Factor de riesgo 1",
            tipo_respuesta=TipoRespuesta.ESCALA_GRAVEDAD,
            orden=1,
        ),
        CatalogoEDAN(
            codigo="FR02",
            seccion=SeccionEDAN.FACTORES_RIESGO,
            descripcion="Factor de riesgo 2",
            tipo_respuesta=TipoRespuesta.ESCALA_GRAVEDAD,
            orden=2,
        ),
        CatalogoEDAN(
            codigo="FP01",
            seccion=SeccionEDAN.FACTORES_PROTECTORES,
            descripcion="Factor protector 1",
            tipo_respuesta=TipoRespuesta.BOOLEANO,
            orden=1,
        ),
        CatalogoEDAN(
            codigo="RH01",
            seccion=SeccionEDAN.RECURSOS_HUMANOS,
            descripcion="Recurso humano 1",
            tipo_respuesta=TipoRespuesta.CANTIDAD,
            orden=1,
        ),
        CatalogoEDAN(
            codigo="NP01",
            seccion=SeccionEDAN.NECESIDADES_PSICOSOCIALES,
            descripcion="Necesidad psicosocial 1",
            tipo_respuesta=TipoRespuesta.ESCALA_RESOLUCION,
            orden=1,
        ),
    ]

    for item in items:
        session.add(item)
    session.commit()

    return items
