#!/usr/bin/env python
"""
Script para poblar el catálogo EDAN con los ítems del instrumento.
Ejecutar con: flask shell < scripts/seed_catalogo.py
O directamente: python scripts/seed_catalogo.py
"""

import sys
import os

# Agregar directorio raíz al path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db
from app.models.catalogo import CatalogoEDAN
from app.models.enums import SeccionEDAN, TipoRespuesta


# === DEFINICIÓN DEL CATÁLOGO ===

CATALOGO_ITEMS = [
    # === FACTORES DE RIESGO (FR01-FR28) ===
    {
        "codigo": "FR01",
        "seccion": SeccionEDAN.FACTORES_RIESGO,
        "orden": 1,
        "tipo": TipoRespuesta.ESCALA_GRAVEDAD,
        "descripcion": "Existencia de un gran número de heridos o lesionados",
    },
    {
        "codigo": "FR02",
        "seccion": SeccionEDAN.FACTORES_RIESGO,
        "orden": 2,
        "tipo": TipoRespuesta.ESCALA_GRAVEDAD,
        "descripcion": "Existencia de un gran número de fallecidos",
    },
    {
        "codigo": "FR03",
        "seccion": SeccionEDAN.FACTORES_RIESGO,
        "orden": 3,
        "tipo": TipoRespuesta.ESCALA_GRAVEDAD,
        "descripcion": "Existencia de un gran número de desaparecidos (como producto del suceso)",
    },
    {
        "codigo": "FR04",
        "seccion": SeccionEDAN.FACTORES_RIESGO,
        "orden": 4,
        "tipo": TipoRespuesta.ESCALA_GRAVEDAD,
        "descripcion": "Existencia de población aislada",
    },
    {
        "codigo": "FR05",
        "seccion": SeccionEDAN.FACTORES_RIESGO,
        "orden": 5,
        "tipo": TipoRespuesta.ESCALA_GRAVEDAD,
        "descripcion": "Carencia de servicios básicos (electricidad, agua, gas)",
    },
    {
        "codigo": "FR06",
        "seccion": SeccionEDAN.FACTORES_RIESGO,
        "orden": 6,
        "tipo": TipoRespuesta.ESCALA_GRAVEDAD,
        "descripcion": "Desorden social (pleitos, riñas, protestas)",
    },
    {
        "codigo": "FR07",
        "seccion": SeccionEDAN.FACTORES_RIESGO,
        "orden": 7,
        "tipo": TipoRespuesta.ESCALA_GRAVEDAD,
        "descripcion": "Enfrentamientos étnicos, políticos, religiosos o de otra índole",
    },
    {
        "codigo": "FR08",
        "seccion": SeccionEDAN.FACTORES_RIESGO,
        "orden": 8,
        "tipo": TipoRespuesta.ESCALA_GRAVEDAD,
        "descripcion": "Grupos violentos, delictivos o destructores",
    },
    {
        "codigo": "FR09",
        "seccion": SeccionEDAN.FACTORES_RIESGO,
        "orden": 9,
        "tipo": TipoRespuesta.ESCALA_GRAVEDAD,
        "descripcion": "Violencia intrafamiliar",
    },
    {
        "codigo": "FR10",
        "seccion": SeccionEDAN.FACTORES_RIESGO,
        "orden": 10,
        "tipo": TipoRespuesta.ESCALA_GRAVEDAD,
        "descripcion": "Delitos sexuales",
    },
    {
        "codigo": "FR11",
        "seccion": SeccionEDAN.FACTORES_RIESGO,
        "orden": 11,
        "tipo": TipoRespuesta.ESCALA_GRAVEDAD,
        "descripcion": "Secuestros",
    },
    {
        "codigo": "FR12",
        "seccion": SeccionEDAN.FACTORES_RIESGO,
        "orden": 12,
        "tipo": TipoRespuesta.ESCALA_GRAVEDAD,
        "descripcion": "Víctimas de tortura",
    },
    {
        "codigo": "FR13",
        "seccion": SeccionEDAN.FACTORES_RIESGO,
        "orden": 13,
        "tipo": TipoRespuesta.ESCALA_GRAVEDAD,
        "descripcion": "Grupos de población desplazada",
    },
    {
        "codigo": "FR14",
        "seccion": SeccionEDAN.FACTORES_RIESGO,
        "orden": 14,
        "tipo": TipoRespuesta.ESCALA_GRAVEDAD,
        "descripcion": "Personas en albergues o refugios",
    },
    {
        "codigo": "FR15",
        "seccion": SeccionEDAN.FACTORES_RIESGO,
        "orden": 15,
        "tipo": TipoRespuesta.ESCALA_GRAVEDAD,
        "descripcion": "Separación de familias",
    },
    {
        "codigo": "FR16",
        "seccion": SeccionEDAN.FACTORES_RIESGO,
        "orden": 16,
        "tipo": TipoRespuesta.ESCALA_GRAVEDAD,
        "descripcion": "Personas con mucha aflicción, alarmadas, con miedo u otras reacciones emocionales",
    },
    {
        "codigo": "FR17",
        "seccion": SeccionEDAN.FACTORES_RIESGO,
        "orden": 17,
        "tipo": TipoRespuesta.ESCALA_GRAVEDAD,
        "descripcion": "Consumo o abuso de alcohol, drogas o ambos",
    },
    {
        "codigo": "FR18",
        "seccion": SeccionEDAN.FACTORES_RIESGO,
        "orden": 18,
        "tipo": TipoRespuesta.ESCALA_GRAVEDAD,
        "descripcion": "Personas con trastornos mentales evidentes / descompensaciones",
    },
    {
        "codigo": "FR19",
        "seccion": SeccionEDAN.FACTORES_RIESGO,
        "orden": 19,
        "tipo": TipoRespuesta.ESCALA_GRAVEDAD,
        "descripcion": "Desintegración de las organizaciones comunitarias",
    },
    {
        "codigo": "FR20",
        "seccion": SeccionEDAN.FACTORES_RIESGO,
        "orden": 20,
        "tipo": TipoRespuesta.ESCALA_GRAVEDAD,
        "descripcion": "Inconformidad comunitaria por las acciones de ayuda o humanitaria",
    },
    {
        "codigo": "FR21",
        "seccion": SeccionEDAN.FACTORES_RIESGO,
        "orden": 21,
        "tipo": TipoRespuesta.ESCALA_GRAVEDAD,
        "descripcion": "Rechazo de la población a cooperar",
    },
    {
        "codigo": "FR22",
        "seccion": SeccionEDAN.FACTORES_RIESGO,
        "orden": 22,
        "tipo": TipoRespuesta.ESCALA_GRAVEDAD,
        "descripcion": "Información insuficiente, contradictoria o poco confiable",
    },
    {
        "codigo": "FR23",
        "seccion": SeccionEDAN.FACTORES_RIESGO,
        "orden": 23,
        "tipo": TipoRespuesta.ESCALA_GRAVEDAD,
        "descripcion": "Existencia de rumores o chismes",
    },
    {
        "codigo": "FR24",
        "seccion": SeccionEDAN.FACTORES_RIESGO,
        "orden": 24,
        "tipo": TipoRespuesta.ESCALA_GRAVEDAD,
        "descripcion": "Equipos de respuesta afectados",
    },
    {
        "codigo": "FR25",
        "seccion": SeccionEDAN.FACTORES_RIESGO,
        "orden": 25,
        "tipo": TipoRespuesta.ESCALA_GRAVEDAD,
        "descripcion": "Gran número de voluntarios desorganizados",
    },
    {
        "codigo": "FR26",
        "seccion": SeccionEDAN.FACTORES_RIESGO,
        "orden": 26,
        "tipo": TipoRespuesta.ESCALA_GRAVEDAD,
        "descripcion": "Pérdida de fuentes de trabajo",
    },
    {
        "codigo": "FR27",
        "seccion": SeccionEDAN.FACTORES_RIESGO,
        "orden": 27,
        "tipo": TipoRespuesta.ESCALA_GRAVEDAD,
        "descripcion": "Gran afectación infraestructura sanitaria",
    },
    {
        "codigo": "FR28",
        "seccion": SeccionEDAN.FACTORES_RIESGO,
        "orden": 28,
        "tipo": TipoRespuesta.ESCALA_GRAVEDAD,
        "descripcion": "Gran número de funcionarios públicos afectados",
    },
    # === FACTORES PROTECTORES (FP01-FP11) ===
    {
        "codigo": "FP01",
        "seccion": SeccionEDAN.FACTORES_PROTECTORES,
        "orden": 1,
        "tipo": TipoRespuesta.BOOLEANO,
        "descripcion": "Plan de Gestión del riesgo con componente de protección de la salud mental previo al desastre",
    },
    {
        "codigo": "FP02",
        "seccion": SeccionEDAN.FACTORES_PROTECTORES,
        "orden": 2,
        "tipo": TipoRespuesta.BOOLEANO,
        "descripcion": "Organización comunitaria previa al desastre",
    },
    {
        "codigo": "FP03",
        "seccion": SeccionEDAN.FACTORES_PROTECTORES,
        "orden": 3,
        "tipo": TipoRespuesta.BOOLEANO,
        "descripcion": "Grupos de ciudadanos que participan activamente en la solución de los problemas derivados del desastre",
    },
    {
        "codigo": "FP04",
        "seccion": SeccionEDAN.FACTORES_PROTECTORES,
        "orden": 4,
        "tipo": TipoRespuesta.BOOLEANO,
        "descripcion": "Acceso a información confiable y sistemática",
    },
    {
        "codigo": "FP05",
        "seccion": SeccionEDAN.FACTORES_PROTECTORES,
        "orden": 5,
        "tipo": TipoRespuesta.BOOLEANO,
        "descripcion": "Miembros de la comunidad capacitados en salud mental",
    },
    {
        "codigo": "FP06",
        "seccion": SeccionEDAN.FACTORES_PROTECTORES,
        "orden": 6,
        "tipo": TipoRespuesta.BOOLEANO,
        "descripcion": "Servicios sociales disponibles",
    },
    {
        "codigo": "FP07",
        "seccion": SeccionEDAN.FACTORES_PROTECTORES,
        "orden": 7,
        "tipo": TipoRespuesta.BOOLEANO,
        "descripcion": "Servicios de salud mental disponibles",
    },
    {
        "codigo": "FP08",
        "seccion": SeccionEDAN.FACTORES_PROTECTORES,
        "orden": 8,
        "tipo": TipoRespuesta.BOOLEANO,
        "descripcion": "Programas externos de ayuda humanitaria funcionando",
    },
    {
        "codigo": "FP09",
        "seccion": SeccionEDAN.FACTORES_PROTECTORES,
        "orden": 9,
        "tipo": TipoRespuesta.BOOLEANO,
        "descripcion": "Ayuda gubernamental",
    },
    {
        "codigo": "FP10",
        "seccion": SeccionEDAN.FACTORES_PROTECTORES,
        "orden": 10,
        "tipo": TipoRespuesta.BOOLEANO,
        "descripcion": "Coordinación intersectorial previa al desastre",
    },
    {
        "codigo": "FP11",
        "seccion": SeccionEDAN.FACTORES_PROTECTORES,
        "orden": 11,
        "tipo": TipoRespuesta.BOOLEANO,
        "descripcion": "Otros (especifique)",
    },
    # === RECURSOS HUMANOS (RH01-RH10) ===
    {
        "codigo": "RH01",
        "seccion": SeccionEDAN.RECURSOS_HUMANOS,
        "orden": 1,
        "tipo": TipoRespuesta.CANTIDAD,
        "descripcion": "Personal de APS con entrenamiento en salud mental",
    },
    {
        "codigo": "RH02",
        "seccion": SeccionEDAN.RECURSOS_HUMANOS,
        "orden": 2,
        "tipo": TipoRespuesta.CANTIDAD,
        "descripcion": "Personal de enfermería con entrenamiento en salud mental",
    },
    {
        "codigo": "RH03",
        "seccion": SeccionEDAN.RECURSOS_HUMANOS,
        "orden": 3,
        "tipo": TipoRespuesta.CANTIDAD,
        "descripcion": "Médicos con entrenamiento en salud mental",
    },
    {
        "codigo": "RH04",
        "seccion": SeccionEDAN.RECURSOS_HUMANOS,
        "orden": 4,
        "tipo": TipoRespuesta.CANTIDAD,
        "descripcion": "Trabajadores sociales",
    },
    {
        "codigo": "RH05",
        "seccion": SeccionEDAN.RECURSOS_HUMANOS,
        "orden": 5,
        "tipo": TipoRespuesta.CANTIDAD,
        "descripcion": "Psicólogos",
    },
    {
        "codigo": "RH06",
        "seccion": SeccionEDAN.RECURSOS_HUMANOS,
        "orden": 6,
        "tipo": TipoRespuesta.CANTIDAD,
        "descripcion": "Terapeutas ocupacionales",
    },
    {
        "codigo": "RH07",
        "seccion": SeccionEDAN.RECURSOS_HUMANOS,
        "orden": 7,
        "tipo": TipoRespuesta.CANTIDAD,
        "descripcion": "Psiquiatras",
    },
    {
        "codigo": "RH08",
        "seccion": SeccionEDAN.RECURSOS_HUMANOS,
        "orden": 8,
        "tipo": TipoRespuesta.CANTIDAD,
        "descripcion": "Estudiantes de carreras afines (psicología, trabajo social, psicopedagogía, etc.)",
    },
    {
        "codigo": "RH09",
        "seccion": SeccionEDAN.RECURSOS_HUMANOS,
        "orden": 9,
        "tipo": TipoRespuesta.CANTIDAD,
        "descripcion": "Voluntarios de ONG",
    },
    {
        "codigo": "RH10",
        "seccion": SeccionEDAN.RECURSOS_HUMANOS,
        "orden": 10,
        "tipo": TipoRespuesta.CANTIDAD,
        "descripcion": "Otros",
    },
    # === RECURSOS MATERIALES (RM01-RM05) ===
    {
        "codigo": "RM01",
        "seccion": SeccionEDAN.RECURSOS_MATERIALES,
        "orden": 1,
        "tipo": TipoRespuesta.BOOLEANO,
        "descripcion": "Material de información y difusión sobre el cuidado de la salud mental disponible",
    },
    {
        "codigo": "RM02",
        "seccion": SeccionEDAN.RECURSOS_MATERIALES,
        "orden": 2,
        "tipo": TipoRespuesta.BOOLEANO,
        "descripcion": "Instalaciones y servicios de salud mental",
    },
    {
        "codigo": "RM03",
        "seccion": SeccionEDAN.RECURSOS_MATERIALES,
        "orden": 3,
        "tipo": TipoRespuesta.BOOLEANO,
        "descripcion": "Medicamentos (para trastornos de salud mental)",
    },
    {
        "codigo": "RM04",
        "seccion": SeccionEDAN.RECURSOS_MATERIALES,
        "orden": 4,
        "tipo": TipoRespuesta.BOOLEANO,
        "descripcion": "Juegos o juguetes",
    },
    {
        "codigo": "RM05",
        "seccion": SeccionEDAN.RECURSOS_MATERIALES,
        "orden": 5,
        "tipo": TipoRespuesta.BOOLEANO,
        "descripcion": "Otros",
    },
    # === RECURSOS ECONÓMICOS (RE01) ===
    {
        "codigo": "RE01",
        "seccion": SeccionEDAN.RECURSOS_ECONOMICOS,
        "orden": 1,
        "tipo": TipoRespuesta.BOOLEANO,
        "descripcion": "Fondos disponibles para acciones de salud mental",
    },
    # === NECESIDADES PSICOSOCIALES (NP01-NP12) ===
    {
        "codigo": "NP01",
        "seccion": SeccionEDAN.NECESIDADES_PSICOSOCIALES,
        "orden": 1,
        "tipo": TipoRespuesta.ESCALA_RESOLUCION,
        "descripcion": "Orientación e Información",
    },
    {
        "codigo": "NP02",
        "seccion": SeccionEDAN.NECESIDADES_PSICOSOCIALES,
        "orden": 2,
        "tipo": TipoRespuesta.ESCALA_RESOLUCION,
        "descripcion": "Contacto y apoyo entre los miembros de la familia",
    },
    {
        "codigo": "NP03",
        "seccion": SeccionEDAN.NECESIDADES_PSICOSOCIALES,
        "orden": 3,
        "tipo": TipoRespuesta.ESCALA_RESOLUCION,
        "descripcion": "Primera Ayuda Psicológica",
    },
    {
        "codigo": "NP04",
        "seccion": SeccionEDAN.NECESIDADES_PSICOSOCIALES,
        "orden": 4,
        "tipo": TipoRespuesta.ESCALA_RESOLUCION,
        "descripcion": "Apoyo emocional a la población afectada",
    },
    {
        "codigo": "NP05",
        "seccion": SeccionEDAN.NECESIDADES_PSICOSOCIALES,
        "orden": 5,
        "tipo": TipoRespuesta.ESCALA_RESOLUCION,
        "descripcion": "Apoyo emocional a equipos de salud",
    },
    {
        "codigo": "NP06",
        "seccion": SeccionEDAN.NECESIDADES_PSICOSOCIALES,
        "orden": 6,
        "tipo": TipoRespuesta.ESCALA_RESOLUCION,
        "descripcion": "Apoyo emocional a funcionarios públicos",
    },
    {
        "codigo": "NP07",
        "seccion": SeccionEDAN.NECESIDADES_PSICOSOCIALES,
        "orden": 7,
        "tipo": TipoRespuesta.ESCALA_RESOLUCION,
        "descripcion": "Apoyo social e institucional",
    },
    {
        "codigo": "NP08",
        "seccion": SeccionEDAN.NECESIDADES_PSICOSOCIALES,
        "orden": 8,
        "tipo": TipoRespuesta.ESCALA_RESOLUCION,
        "descripcion": "Organización comunitaria",
    },
    {
        "codigo": "NP09",
        "seccion": SeccionEDAN.NECESIDADES_PSICOSOCIALES,
        "orden": 9,
        "tipo": TipoRespuesta.ESCALA_RESOLUCION,
        "descripcion": "Continuidad de la educación para niños, niñas y jóvenes",
    },
    {
        "codigo": "NP10",
        "seccion": SeccionEDAN.NECESIDADES_PSICOSOCIALES,
        "orden": 10,
        "tipo": TipoRespuesta.ESCALA_RESOLUCION,
        "descripcion": "Liderazgo (desarrollar en consideraciones finales)",
    },
    {
        "codigo": "NP11",
        "seccion": SeccionEDAN.NECESIDADES_PSICOSOCIALES,
        "orden": 11,
        "tipo": TipoRespuesta.ESCALA_RESOLUCION,
        "descripcion": "Culturales (acorde con las costumbres y tradiciones locales)",
    },
    {
        "codigo": "NP12",
        "seccion": SeccionEDAN.NECESIDADES_PSICOSOCIALES,
        "orden": 12,
        "tipo": TipoRespuesta.ESCALA_RESOLUCION,
        "descripcion": "Religiosas o espirituales",
    },
    # === NECESIDADES INSTITUCIONALES (NI01-NI04) ===
    {
        "codigo": "NI01",
        "seccion": SeccionEDAN.NECESIDADES_INSTITUCIONALES,
        "orden": 1,
        "tipo": TipoRespuesta.ESCALA_RESOLUCION,
        "descripcion": "Movilización Equipos de Apoyo a la Respuesta en Salud Mental (ARSAM)",
    },
    {
        "codigo": "NI02",
        "seccion": SeccionEDAN.NECESIDADES_INSTITUCIONALES,
        "orden": 2,
        "tipo": TipoRespuesta.ESCALA_RESOLUCION,
        "descripcion": "Incremento del personal",
    },
    {
        "codigo": "NI03",
        "seccion": SeccionEDAN.NECESIDADES_INSTITUCIONALES,
        "orden": 3,
        "tipo": TipoRespuesta.ESCALA_RESOLUCION,
        "descripcion": "Capacitación y entrenamiento",
    },
    {
        "codigo": "NI04",
        "seccion": SeccionEDAN.NECESIDADES_INSTITUCIONALES,
        "orden": 4,
        "tipo": TipoRespuesta.ESCALA_RESOLUCION,
        "descripcion": "Apertura de servicios de salud mental",
    },
    # === NECESIDADES BÁSICAS (NB01-NB06) ===
    {
        "codigo": "NB01",
        "seccion": SeccionEDAN.NECESIDADES_BASICAS,
        "orden": 1,
        "tipo": TipoRespuesta.ESCALA_RESOLUCION,
        "descripcion": "Electricidad",
    },
    {
        "codigo": "NB02",
        "seccion": SeccionEDAN.NECESIDADES_BASICAS,
        "orden": 2,
        "tipo": TipoRespuesta.ESCALA_RESOLUCION,
        "descripcion": "Agua",
    },
    {
        "codigo": "NB03",
        "seccion": SeccionEDAN.NECESIDADES_BASICAS,
        "orden": 3,
        "tipo": TipoRespuesta.ESCALA_RESOLUCION,
        "descripcion": "Vivienda",
    },
    {
        "codigo": "NB04",
        "seccion": SeccionEDAN.NECESIDADES_BASICAS,
        "orden": 4,
        "tipo": TipoRespuesta.ESCALA_RESOLUCION,
        "descripcion": "Alimentación",
    },
    {
        "codigo": "NB05",
        "seccion": SeccionEDAN.NECESIDADES_BASICAS,
        "orden": 5,
        "tipo": TipoRespuesta.ESCALA_RESOLUCION,
        "descripcion": "Vestuario",
    },
    {
        "codigo": "NB06",
        "seccion": SeccionEDAN.NECESIDADES_BASICAS,
        "orden": 6,
        "tipo": TipoRespuesta.ESCALA_RESOLUCION,
        "descripcion": "Seguridad",
    },
]


def seed_catalogo(force: bool = False):
    """
    Pobla el catálogo EDAN.

    Args:
        force: Si True, elimina ítems existentes antes de insertar.
    """
    app = create_app()

    with app.app_context():
        existing_count = CatalogoEDAN.query.count()

        if existing_count > 0 and not force:
            print(
                f"⚠️  Catálogo ya tiene {existing_count} ítems. Use --force para reemplazar."
            )
            return

        if force and existing_count > 0:
            print(f"🗑️  Eliminando {existing_count} ítems existentes...")
            CatalogoEDAN.query.delete()
            db.session.commit()

        print(f"📝 Insertando {len(CATALOGO_ITEMS)} ítems en el catálogo...")

        for item_data in CATALOGO_ITEMS:
            item = CatalogoEDAN(
                codigo=item_data["codigo"],
                seccion=item_data["seccion"],
                descripcion=item_data["descripcion"],
                tipo_respuesta=item_data["tipo"],
                orden=item_data["orden"],
                activo=True,
            )
            db.session.add(item)

        db.session.commit()

        # Verificar
        final_count = CatalogoEDAN.query.count()
        print(f"✅ Catálogo poblado exitosamente: {final_count} ítems")

        # Resumen por sección
        print("\n📊 Resumen por sección:")
        for seccion in SeccionEDAN:
            count = CatalogoEDAN.query.filter_by(seccion=seccion).count()
            if count > 0:
                print(f"   - {seccion.value}: {count} ítems")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Poblar catálogo EDAN")
    parser.add_argument(
        "--force", action="store_true", help="Reemplazar ítems existentes"
    )
    args = parser.parse_args()

    seed_catalogo(force=args.force)
