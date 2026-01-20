"""
Rutas del formulario EDAN - Wizard multi-paso.
"""

import json
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app import db
from app.models.edan import Evaluador, FormularioEDAN
from app.data_maestros import (
    COMUNAS_POR_PROVINCIA,
    COMUNA_A_PROVINCIA,
    ESTABLECIMIENTOS,
)

bp = Blueprint("formulario", __name__)


# === DATOS DE REFERENCIA (Factores y Necesidades) ===

FACTORES_RIESGO = [
    (1, "Existencia de un gran número de heridos o lesionados"),
    (2, "Existencia de un gran número de fallecidos"),
    (3, "Existencia de un gran número de desaparecidos (como producto del suceso)"),
    (4, "Existencia de población aislada"),
    (5, "Carencia de servicios básicos (electricidad, agua, gas)"),
    (6, "Desorden social (pleitos, riñas, protestas)"),
    (7, "Enfrentamientos étnicos, políticos, religiosos o de otra índole"),
    (8, "Grupos violentos, delictivos o destructores"),
    (9, "Violencia intrafamiliar"),
    (10, "Delitos sexuales"),
    (11, "Secuestros"),
    (12, "Víctimas de tortura"),
    (13, "Grupos de población desplazada"),
    (14, "Personas en albergues o refugios"),
    (15, "Separación de familias"),
    (
        16,
        "Personas con mucha aflicción, alarmadas, con miedo u otras reacciones emocionales",
    ),
    (17, "Consumo o abuso de alcohol, drogas o ambos"),
    (18, "Personas con trastornos mentales evidentes / descompensaciones"),
    (19, "Desintegración de las organizaciones comunitarias"),
    (20, "Inconformidad comunitaria por las acciones de ayuda o humanitaria"),
    (21, "Rechazo de la población a cooperar"),
    (22, "Información insuficiente, contradictoria o poco confiable"),
    (23, "Existencia de rumores o chismes"),
    (24, "Equipos de respuesta afectados"),
    (25, "Gran número de voluntarios desorganizados"),
    (26, "Pérdida de fuentes de trabajo"),
    (27, "Gran afectación infraestructura sanitaria"),
    (28, "Gran número de funcionarios públicos afectados"),
]

FACTORES_PROTECTORES = [
    (
        29,
        "Plan de Gestión del riesgo con componente de protección de la salud mental previo al desastre",
    ),
    (30, "Organización comunitaria previa al desastre"),
    (
        31,
        "Grupos de ciudadanos que participan activamente en la solución de los problemas derivados del desastre",
    ),
    (32, "Acceso a información confiable y sistemática"),
    (33, "Miembros de la comunidad capacitados en salud mental"),
    (34, "Servicios sociales disponibles"),
    (35, "Servicios de salud mental disponibles"),
    (36, "Programas externos de ayuda humanitaria funcionando"),
    (37, "Ayuda gubernamental"),
    (38, "Coordinación intersectorial previa al desastre"),
    (39, "Otros (especifique)"),
]

RECURSOS_HUMANOS = [
    (40, "Personal de APS con entrenamiento en salud mental"),
    (41, "Personal de enfermería con entrenamiento en salud mental"),
    (42, "Médicos con entrenamiento en salud mental"),
    (43, "Trabajadores sociales"),
    (44, "Psicólogos"),
    (45, "Terapeutas ocupacionales"),
    (46, "Psiquiatras"),
    (
        47,
        "Estudiantes de carreras afines (psicología, trabajo social, psicopedagogía, etc.)",
    ),
    (48, "Voluntarios de ONG"),
    (49, "Otros"),
]

RECURSOS_MATERIALES = [
    (
        50,
        "Material de información y difusión sobre el cuidado de la salud mental disponible",
    ),
    (51, "Instalaciones y servicios de salud mental"),
    (52, "Medicamentos (para trastornos de salud mental)"),
    (53, "Juegos o juguetes"),
    (54, "Otros"),
]

RECURSOS_ECONOMICOS = [
    (55, "Fondos disponibles para acciones de salud mental"),
]

NECESIDADES_PSICOSOCIALES = [
    (56, "Orientación e Información"),
    (57, "Contacto y apoyo entre los miembros de la familia"),
    (58, "Primera Ayuda Psicológica"),
    (59, "Apoyo emocional a la población afectada"),
    (60, "Apoyo emocional a equipos de salud"),
    (61, "Apoyo emocional a funcionarios públicos"),
    (62, "Apoyo social e institucional"),
    (63, "Organización comunitaria"),
    (64, "Continuidad de la educación para niños, niñas y jóvenes"),
    (65, "Liderazgo (desarrollar en consideraciones finales)"),
    (66, "Culturales (acorde con las costumbres y tradiciones locales)"),
    (67, "Religiosas o espirituales"),
]

NECESIDADES_INSTITUCIONALES = [
    (68, "Movilización Equipos de Apoyo a la Respuesta en Salud Mental (ARSAM)"),
    (69, "Incremento del personal"),
    (70, "Capacitación y entrenamiento"),
    (71, "Apertura de servicios de salud mental"),
]

NECESIDADES_BASICAS = [
    (72, "Electricidad"),
    (73, "Agua"),
    (74, "Vivienda"),
    (75, "Alimentación"),
    (76, "Vestuario"),
    (77, "Seguridad"),
]


# === RUTAS ===


@bp.route("/")
def index():
    """Página de inicio - Ingreso de evaluador."""
    return render_template("wizard/inicio.html", establecimientos=ESTABLECIMIENTOS)


@bp.route("/iniciar", methods=["POST"])
def iniciar_evaluacion():
    """Procesa el registro del evaluador e inicia el wizard."""
    run = request.form.get("run", "").strip()
    nombre = request.form.get("nombre", "").strip()
    apellido1 = request.form.get("apellido1", "").strip()
    apellido2 = request.form.get("apellido2", "").strip()
    establecimiento = request.form.get("establecimiento", "").strip()

    # Validación básica
    if not all([run, nombre, apellido1, establecimiento]):
        flash("Por favor complete todos los campos obligatorios.", "error")
        return redirect(url_for("formulario.index"))

    # Crear o buscar evaluador
    evaluador = Evaluador.query.filter_by(run=run).first()
    if not evaluador:
        evaluador = Evaluador(
            run=run,
            nombre=nombre,
            apellido1=apellido1,
            apellido2=apellido2,
            establecimiento=establecimiento,
        )
        db.session.add(evaluador)
    else:
        # Actualizar datos del evaluador si ya existe
        evaluador.nombre = nombre
        evaluador.apellido1 = apellido1
        evaluador.apellido2 = apellido2
        evaluador.establecimiento = establecimiento

    db.session.commit()

    # Crear nuevo formulario
    formulario = FormularioEDAN(evaluador_id=evaluador.id)
    db.session.add(formulario)
    db.session.commit()

    # Guardar ID en sesión
    session["formulario_id"] = formulario.id
    session["evaluador_id"] = evaluador.id

    return redirect(url_for("formulario.paso", num=1))


@bp.route("/paso/<int:num>", methods=["GET", "POST"])
def paso(num):
    """Renderiza y procesa cada paso del wizard."""
    formulario_id = session.get("formulario_id")
    if not formulario_id:
        return redirect(url_for("formulario.index"))

    formulario = FormularioEDAN.query.get_or_404(formulario_id)
    evaluador = Evaluador.query.get(formulario.evaluador_id)

    if request.method == "POST":
        # Guardar datos del paso actual
        guardar_paso(formulario, num, request.form)

        # Determinar siguiente acción
        accion = request.form.get("accion", "siguiente")
        if accion == "anterior" and num > 1:
            return redirect(url_for("formulario.paso", num=num - 1))
        elif accion == "siguiente" and num < 6:
            formulario.paso_actual = num + 1
            db.session.commit()
            return redirect(url_for("formulario.paso", num=num + 1))
        elif accion == "finalizar":
            formulario.estado = "completado"
            db.session.commit()
            return redirect(url_for("formulario.confirmacion"))

    # Precarga automática de datos en Paso 1 si están vacíos
    if num == 1:
        if not formulario.responsable:
            formulario.responsable = f"{evaluador.nombre} {evaluador.apellido1} {evaluador.apellido2 or ''}".strip()
        if not formulario.institucion:
            formulario.institucion = evaluador.establecimiento

    # Contexto común para todos los pasos
    contexto = {
        "formulario": formulario,
        "evaluador": evaluador,
        "paso_actual": num,
        "total_pasos": 6,
    }

    # Datos específicos por paso
    if num == 1:
        # Flatten comunas for the select list
        todas_comunas = []
        for prov, comunas in COMUNAS_POR_PROVINCIA.items():
            todas_comunas.extend(comunas)
        contexto["comunas"] = sorted(list(set(todas_comunas)))
        contexto["mapa_comunas"] = json.dumps(COMUNA_A_PROVINCIA)
    elif num == 2:
        contexto["factores"] = FACTORES_RIESGO
    elif num == 3:
        contexto["factores"] = FACTORES_PROTECTORES
    elif num == 4:
        contexto["recursos_humanos"] = RECURSOS_HUMANOS
        contexto["recursos_materiales"] = RECURSOS_MATERIALES
        contexto["recursos_economicos"] = RECURSOS_ECONOMICOS
    elif num == 5:
        contexto["necesidades_psicosociales"] = NECESIDADES_PSICOSOCIALES
        contexto["necesidades_institucionales"] = NECESIDADES_INSTITUCIONALES
        contexto["necesidades_basicas"] = NECESIDADES_BASICAS

    return render_template(f"wizard/paso{num}.html", **contexto)


@bp.route("/confirmacion")
def confirmacion():
    """Página de confirmación al finalizar."""
    formulario_id = session.get("formulario_id")
    if not formulario_id:
        return redirect(url_for("formulario.index"))

    formulario = FormularioEDAN.query.get_or_404(formulario_id)
    evaluador = Evaluador.query.get(formulario.evaluador_id)

    # Limpiar sesión
    session.pop("formulario_id", None)
    session.pop("evaluador_id", None)

    return render_template(
        "wizard/confirmacion.html", formulario=formulario, evaluador=evaluador
    )


def guardar_paso(formulario, num, form_data):
    """Guarda los datos de un paso específico."""
    if num == 1:
        # Datos generales
        formulario.nivel_aplicacion = form_data.get("nivel_aplicacion")
        formulario.fecha_informe = form_data.get("fecha_informe") or None
        formulario.responsable = form_data.get("responsable")
        # El campo 'hora_informe' no estaba siendo guardado explícitamente pero existe en el modelo
        formulario.hora_informe = form_data.get("hora_informe")
        formulario.cargo_funcion = form_data.get("cargo_funcion")
        formulario.institucion = form_data.get("institucion")
        formulario.poblacion_estimada = form_data.get("poblacion_estimada") or None
        formulario.comuna = form_data.get("comuna")
        formulario.provincia = form_data.get("provincia")
        formulario.fecha_suceso = form_data.get("fecha_suceso") or None
        formulario.tipo_suceso = form_data.get("tipo_suceso")
        formulario.principales_danos = form_data.get("principales_danos")

    elif num == 2:
        # Factores de riesgo
        factores = {}
        for i in range(1, 29):
            valor = form_data.get(f"factor_{i}")
            if valor:
                factores[str(i)] = valor
        formulario.factores_riesgo = factores

    elif num == 3:
        # Factores protectores
        factores = {}
        for i in range(29, 40):
            valor = form_data.get(f"factor_{i}")
            if valor:
                factores[str(i)] = valor == "si"
        formulario.factores_protectores = factores
        formulario.comentarios_informacion = form_data.get("comentarios_informacion")
        formulario.otras_consideraciones = form_data.get("otras_consideraciones")

    elif num == 4:
        # Recursos
        humanos = {}
        for i in range(40, 50):
            valor = form_data.get(f"recurso_{i}")
            if valor:
                try:
                    humanos[str(i)] = int(valor)
                except ValueError:
                    pass
        formulario.recursos_humanos = humanos

        materiales = {}
        for i in range(50, 55):
            valor = form_data.get(f"recurso_{i}")
            if valor:
                materiales[str(i)] = valor == "si"
        formulario.recursos_materiales = materiales

        economicos = {}
        valor = form_data.get("recurso_55")
        if valor:
            economicos["55"] = valor == "si"
        formulario.recursos_economicos = economicos

    elif num == 5:
        # Necesidades
        psicosociales = {}
        for i in range(56, 68):
            valor = form_data.get(f"necesidad_{i}")
            if valor:
                psicosociales[str(i)] = valor
        formulario.necesidades_psicosociales = psicosociales

        institucionales = {}
        for i in range(68, 72):
            valor = form_data.get(f"necesidad_{i}")
            if valor:
                institucionales[str(i)] = valor
        formulario.necesidades_institucionales = institucionales

        basicas = {}
        for i in range(72, 78):
            valor = form_data.get(f"necesidad_{i}")
            if valor:
                basicas[str(i)] = valor
        formulario.necesidades_basicas = basicas
        formulario.comentarios_necesidades = form_data.get("comentarios_necesidades")

    elif num == 6:
        # Síntesis
        formulario.sintesis_necesidades = form_data.get("sintesis_necesidades")
        formulario.acciones_realizar = form_data.get("acciones_realizar")

    db.session.commit()
