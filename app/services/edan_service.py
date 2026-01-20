"""
Servicio de lógica de negocio para formularios EDAN.
"""

from typing import Optional, Dict, Any, List
from app import db
from app.models.edan import Evaluador, FormularioEDAN
from app.models.catalogo import CatalogoEDAN
from app.models.respuesta import RespuestaEDAN
from app.models.enums import SeccionEDAN, TipoRespuesta, ValorEscala


class EdanService:
    """Servicio para gestionar formularios EDAN."""

    # === EVALUADOR ===

    @staticmethod
    def get_or_create_evaluador(
        run: str,
        nombre: str,
        apellido1: str,
        apellido2: Optional[str],
        establecimiento: str,
    ) -> Evaluador:
        """Obtiene o crea un evaluador por RUN."""
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
            # Actualizar datos si ya existe
            evaluador.nombre = nombre
            evaluador.apellido1 = apellido1
            evaluador.apellido2 = apellido2
            evaluador.establecimiento = establecimiento

        db.session.commit()
        return evaluador

    # === FORMULARIO ===

    @staticmethod
    def crear_formulario(evaluador_id: str) -> FormularioEDAN:
        """Crea un nuevo formulario para un evaluador."""
        formulario = FormularioEDAN(evaluador_id=evaluador_id)
        db.session.add(formulario)
        db.session.commit()
        return formulario

    @staticmethod
    def get_formulario(formulario_id: str) -> Optional[FormularioEDAN]:
        """Obtiene un formulario por ID."""
        return db.session.get(FormularioEDAN, formulario_id)

    @staticmethod
    def actualizar_paso(formulario: FormularioEDAN, nuevo_paso: int) -> None:
        """Actualiza el paso actual del formulario."""
        formulario.paso_actual = nuevo_paso
        db.session.commit()

    @staticmethod
    def completar_formulario(formulario: FormularioEDAN) -> None:
        """Marca un formulario como completado."""
        formulario.estado = "completado"
        db.session.commit()

    # === DATOS GENERALES (PASO 1) ===

    @staticmethod
    def guardar_datos_generales(
        formulario: FormularioEDAN, datos: Dict[str, Any]
    ) -> None:
        """Guarda los datos generales del formulario (Paso 1)."""
        formulario.nivel_aplicacion = datos.get("nivel_aplicacion")
        formulario.fecha_informe = datos.get("fecha_informe") or None
        formulario.hora_informe = datos.get("hora_informe") or None
        formulario.responsable = datos.get("responsable")
        formulario.cargo_funcion = datos.get("cargo_funcion")
        formulario.institucion = datos.get("institucion")
        formulario.poblacion_estimada = datos.get("poblacion_estimada") or None
        formulario.comuna = datos.get("comuna")
        formulario.provincia = datos.get("provincia")
        formulario.fecha_suceso = datos.get("fecha_suceso") or None
        formulario.tipo_suceso = datos.get("tipo_suceso")
        formulario.principales_danos = datos.get("principales_danos")
        db.session.commit()

    # === RESPUESTAS NORMALIZADAS ===

    @staticmethod
    def guardar_respuestas_escala(
        formulario_id: str, seccion: SeccionEDAN, respuestas: Dict[str, str]
    ) -> None:
        """
        Guarda respuestas de escala (G/M/B/NE o R/NR) para una sección.

        Args:
            formulario_id: ID del formulario
            seccion: Sección del catálogo
            respuestas: Dict {codigo_item: valor_escala}
        """
        items = CatalogoEDAN.query.filter_by(seccion=seccion, activo=True).all()
        item_map = {item.codigo: item for item in items}

        for codigo, valor in respuestas.items():
            if codigo in item_map and valor:
                item = item_map[codigo]
                RespuestaEDAN.set_respuesta(
                    formulario_id=formulario_id,
                    item_id=item.id,
                    valor=valor,
                    tipo_respuesta=item.tipo_respuesta.value,
                )

        db.session.commit()

    @staticmethod
    def guardar_respuestas_bool(
        formulario_id: str, seccion: SeccionEDAN, respuestas: Dict[str, bool]
    ) -> None:
        """
        Guarda respuestas booleanas para una sección.
        """
        items = CatalogoEDAN.query.filter_by(seccion=seccion, activo=True).all()
        item_map = {item.codigo: item for item in items}

        for codigo, valor in respuestas.items():
            if codigo in item_map:
                item = item_map[codigo]
                RespuestaEDAN.set_respuesta(
                    formulario_id=formulario_id,
                    item_id=item.id,
                    valor=valor,
                    tipo_respuesta="booleano",
                )

        db.session.commit()

    @staticmethod
    def guardar_respuestas_cantidad(
        formulario_id: str, seccion: SeccionEDAN, respuestas: Dict[str, int]
    ) -> None:
        """
        Guarda respuestas de cantidad para una sección.
        """
        items = CatalogoEDAN.query.filter_by(seccion=seccion, activo=True).all()
        item_map = {item.codigo: item for item in items}

        for codigo, valor in respuestas.items():
            if codigo in item_map and valor is not None:
                item = item_map[codigo]
                RespuestaEDAN.set_respuesta(
                    formulario_id=formulario_id,
                    item_id=item.id,
                    valor=valor,
                    tipo_respuesta="cantidad",
                )

        db.session.commit()

    @staticmethod
    def get_respuestas_por_seccion(
        formulario_id: str, seccion: SeccionEDAN
    ) -> Dict[str, Any]:
        """
        Obtiene las respuestas de una sección como diccionario.

        Returns:
            Dict {codigo_item: valor}
        """
        respuestas = (
            RespuestaEDAN.query.join(CatalogoEDAN)
            .filter(
                RespuestaEDAN.formulario_id == formulario_id,
                CatalogoEDAN.seccion == seccion,
            )
            .all()
        )

        return {r.item.codigo: r.valor for r in respuestas}

    # === COMENTARIOS Y SÍNTESIS ===

    @staticmethod
    def guardar_comentarios_paso3(
        formulario: FormularioEDAN,
        comentarios_informacion: str,
        otras_consideraciones: str,
    ) -> None:
        """Guarda comentarios del paso 3 (Factores Protectores)."""
        formulario.comentarios_informacion = comentarios_informacion
        formulario.otras_consideraciones = otras_consideraciones
        db.session.commit()

    @staticmethod
    def guardar_comentarios_paso5(
        formulario: FormularioEDAN, comentarios_necesidades: str
    ) -> None:
        """Guarda comentarios del paso 5 (Necesidades)."""
        formulario.comentarios_necesidades = comentarios_necesidades
        db.session.commit()

    @staticmethod
    def guardar_sintesis(
        formulario: FormularioEDAN, sintesis_necesidades: str, acciones_realizar: str
    ) -> None:
        """Guarda síntesis del paso 6."""
        formulario.sintesis_necesidades = sintesis_necesidades
        formulario.acciones_realizar = acciones_realizar
        db.session.commit()

    # === CATÁLOGO ===

    @staticmethod
    def get_catalogo_por_seccion(seccion: SeccionEDAN) -> List[CatalogoEDAN]:
        """Obtiene ítems del catálogo por sección."""
        return CatalogoEDAN.get_by_seccion(seccion)

    @staticmethod
    def get_catalogo_completo() -> Dict[SeccionEDAN, List[CatalogoEDAN]]:
        """Obtiene el catálogo completo organizado por sección."""
        return {
            seccion: CatalogoEDAN.get_by_seccion(seccion) for seccion in SeccionEDAN
        }
