"""
Rutas del formulario EDAN - Wizard multi-paso.
"""

import json
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app.services.edan_service import EdanService
from app.models.enums import SeccionEDAN
from app.data_maestros import (
    COMUNAS_POR_PROVINCIA,
    COMUNA_A_PROVINCIA,
    ESTABLECIMIENTOS,
)

bp = Blueprint("formulario", __name__)


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
    evaluador = EdanService.get_or_create_evaluador(
        run=run,
        nombre=nombre,
        apellido1=apellido1,
        apellido2=apellido2,
        establecimiento=establecimiento,
    )

    # Crear nuevo formulario
    formulario = EdanService.crear_formulario(evaluador.id)

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

    formulario = EdanService.get_formulario(formulario_id)
    if not formulario:
        return redirect(url_for("formulario.index"))

    evaluador = formulario.evaluador

    if request.method == "POST":
        # Guardar datos del paso actual
        guardar_paso(formulario, num, request.form)

        # Determinar siguiente acción
        accion = request.form.get("accion", "siguiente")
        if accion == "anterior" and num > 1:
            return redirect(url_for("formulario.paso", num=num - 1))
        elif accion == "siguiente" and num < 6:
            EdanService.actualizar_paso(formulario, num + 1)
            return redirect(url_for("formulario.paso", num=num + 1))
        elif accion == "finalizar":
            EdanService.completar_formulario(formulario)
            return redirect(url_for("formulario.confirmacion"))

    # Precarga automática de datos en Paso 1 si están vacíos
    if num == 1:
        if not formulario.responsable:
            formulario.responsable = evaluador.nombre_completo()
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
        contexto["items"] = EdanService.get_catalogo_por_seccion(
            SeccionEDAN.FACTORES_RIESGO
        )
        contexto["respuestas"] = EdanService.get_respuestas_por_seccion(
            formulario.id, SeccionEDAN.FACTORES_RIESGO
        )
    elif num == 3:
        contexto["items"] = EdanService.get_catalogo_por_seccion(
            SeccionEDAN.FACTORES_PROTECTORES
        )
        contexto["respuestas"] = EdanService.get_respuestas_por_seccion(
            formulario.id, SeccionEDAN.FACTORES_PROTECTORES
        )
    elif num == 4:
        contexto["recursos_humanos"] = EdanService.get_catalogo_por_seccion(
            SeccionEDAN.RECURSOS_HUMANOS
        )
        contexto["recursos_materiales"] = EdanService.get_catalogo_por_seccion(
            SeccionEDAN.RECURSOS_MATERIALES
        )
        contexto["recursos_economicos"] = EdanService.get_catalogo_por_seccion(
            SeccionEDAN.RECURSOS_ECONOMICOS
        )

        # Obtener respuestas de todas las secciones de recursos
        rh = EdanService.get_respuestas_por_seccion(
            formulario.id, SeccionEDAN.RECURSOS_HUMANOS
        )
        rm = EdanService.get_respuestas_por_seccion(
            formulario.id, SeccionEDAN.RECURSOS_MATERIALES
        )
        re = EdanService.get_respuestas_por_seccion(
            formulario.id, SeccionEDAN.RECURSOS_ECONOMICOS
        )

        contexto["respuestas"] = {**rh, **rm, **re}

    elif num == 5:
        contexto["necesidades_psicosociales"] = EdanService.get_catalogo_por_seccion(
            SeccionEDAN.NECESIDADES_PSICOSOCIALES
        )
        contexto["necesidades_institucionales"] = EdanService.get_catalogo_por_seccion(
            SeccionEDAN.NECESIDADES_INSTITUCIONALES
        )
        contexto["necesidades_basicas"] = EdanService.get_catalogo_por_seccion(
            SeccionEDAN.NECESIDADES_BASICAS
        )

        # Obtener respuestas de todas las secciones de necesidades
        np = EdanService.get_respuestas_por_seccion(
            formulario.id, SeccionEDAN.NECESIDADES_PSICOSOCIALES
        )
        ni = EdanService.get_respuestas_por_seccion(
            formulario.id, SeccionEDAN.NECESIDADES_INSTITUCIONALES
        )
        nb = EdanService.get_respuestas_por_seccion(
            formulario.id, SeccionEDAN.NECESIDADES_BASICAS
        )

        contexto["respuestas"] = {**np, **ni, **nb}

    return render_template(f"wizard/paso{num}.html", **contexto)


@bp.route("/confirmacion")
def confirmacion():
    """Página de confirmación al finalizar."""
    formulario_id = session.get("formulario_id")
    if not formulario_id:
        return redirect(url_for("formulario.index"))

    formulario = EdanService.get_formulario(formulario_id)
    if not formulario:
        return redirect(url_for("formulario.index"))

    evaluador = formulario.evaluador

    # Limpiar sesión
    session.pop("formulario_id", None)
    session.pop("evaluador_id", None)

    return render_template(
        "wizard/confirmacion.html", formulario=formulario, evaluador=evaluador
    )


def guardar_paso(formulario, num, form_data):
    """Guarda los datos de un paso específico usando el servicio."""
    if num == 1:
        # Datos generales
        EdanService.guardar_datos_generales(formulario, form_data)

    elif num == 2:
        # Factores de riesgo (Escala Gravedad)
        respuestas = {}
        for key, value in form_data.items():
            if key.startswith("item_"):
                codigo = key.replace("item_", "")
                respuestas[codigo] = value

        EdanService.guardar_respuestas_escala(
            formulario.id, SeccionEDAN.FACTORES_RIESGO, respuestas
        )

    elif num == 3:
        # Factores protectores (Booleanos)
        # Notas: items de catálogo tienen códigos FP01, FP02...
        # Form data vendrá como item_FP01="si"
        respuestas = {}
        items = EdanService.get_catalogo_por_seccion(SeccionEDAN.FACTORES_PROTECTORES)

        for item in items:
            key = f"item_{item.codigo}"
            valor = form_data.get(key)
            if valor:
                respuestas[item.codigo] = valor == "si"
            # Si no viene, es None (no false explicito, salvo checkbox)

        EdanService.guardar_respuestas_bool(
            formulario.id, SeccionEDAN.FACTORES_PROTECTORES, respuestas
        )

        EdanService.guardar_comentarios_paso3(
            formulario,
            form_data.get("comentarios_informacion"),
            form_data.get("otras_consideraciones"),
        )

    elif num == 4:
        # Recursos
        # Humanos (Cantidad)
        humanos = {}
        for key, value in form_data.items():
            if key.startswith("item_RH"):
                codigo = key.replace("item_", "")
                try:
                    if value:
                        humanos[codigo] = int(value)
                except ValueError:
                    pass
        EdanService.guardar_respuestas_cantidad(
            formulario.id, SeccionEDAN.RECURSOS_HUMANOS, humanos
        )

        # Materiales (Bool)
        materiales = {}
        items_m = EdanService.get_catalogo_por_seccion(SeccionEDAN.RECURSOS_MATERIALES)
        for item in items_m:
            key = f"item_{item.codigo}"
            valor = form_data.get(key)
            if valor:
                materiales[item.codigo] = valor == "si"
        EdanService.guardar_respuestas_bool(
            formulario.id, SeccionEDAN.RECURSOS_MATERIALES, materiales
        )

        # Económicos (Bool)
        economicos = {}
        items_e = EdanService.get_catalogo_por_seccion(SeccionEDAN.RECURSOS_ECONOMICOS)
        for item in items_e:
            key = f"item_{item.codigo}"
            valor = form_data.get(key)
            if valor:
                economicos[item.codigo] = valor == "si"
        EdanService.guardar_respuestas_bool(
            formulario.id, SeccionEDAN.RECURSOS_ECONOMICOS, economicos
        )

    elif num == 5:
        # Necesidades (Escala Resolución)
        process_necesidades(
            formulario, form_data, SeccionEDAN.NECESIDADES_PSICOSOCIALES, "NP"
        )
        process_necesidades(
            formulario, form_data, SeccionEDAN.NECESIDADES_INSTITUCIONALES, "NI"
        )
        process_necesidades(
            formulario, form_data, SeccionEDAN.NECESIDADES_BASICAS, "NB"
        )

        EdanService.guardar_comentarios_paso5(
            formulario, form_data.get("comentarios_necesidades")
        )

    elif num == 6:
        # Síntesis
        EdanService.guardar_sintesis(
            formulario,
            form_data.get("sintesis_necesidades"),
            form_data.get("acciones_realizar"),
        )


def process_necesidades(formulario, form_data, seccion, prefix):
    """Helper para procesar necesidades."""
    respuestas = {}
    for key, value in form_data.items():
        if key.startswith(f"item_{prefix}"):
            codigo = key.replace("item_", "")
            respuestas[codigo] = value

    EdanService.guardar_respuestas_escala(formulario.id, seccion, respuestas)
