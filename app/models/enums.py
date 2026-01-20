"""
Enums para el modelo de datos EDAN.
"""

from enum import Enum


class SeccionEDAN(str, Enum):
    """Secciones del instrumento EDAN."""

    FACTORES_RIESGO = "factores_riesgo"
    FACTORES_PROTECTORES = "factores_protectores"
    RECURSOS_HUMANOS = "recursos_humanos"
    RECURSOS_MATERIALES = "recursos_materiales"
    RECURSOS_ECONOMICOS = "recursos_economicos"
    NECESIDADES_PSICOSOCIALES = "necesidades_psicosociales"
    NECESIDADES_INSTITUCIONALES = "necesidades_institucionales"
    NECESIDADES_BASICAS = "necesidades_basicas"


class TipoRespuesta(str, Enum):
    """Tipos de respuesta permitidos."""

    ESCALA_GRAVEDAD = "escala_gravedad"  # G/M/B/NE
    ESCALA_RESOLUCION = "escala_resolucion"  # R/NR
    BOOLEANO = "booleano"  # Sí/No
    CANTIDAD = "cantidad"  # Número entero


class ValorEscala(str, Enum):
    """Valores posibles para respuestas de escala."""

    # Escala de Gravedad (Factores de Riesgo)
    GRAVE = "G"
    MEDIO = "M"
    BAJO = "B"
    NO_EXISTE = "NE"
    # Escala de Resolución (Necesidades)
    RESUELTO = "R"
    NO_RESUELTO = "NR"


class EstadoFormulario(str, Enum):
    """Estados del formulario EDAN."""

    BORRADOR = "borrador"
    COMPLETADO = "completado"


class NivelAplicacion(str, Enum):
    """Niveles de aplicación del EDAN."""

    COMUNAL = "comunal"
    PROVINCIAL = "provincial"
    REGIONAL = "regional"


class TipoSuceso(str, Enum):
    """Tipos de suceso/emergencia."""

    INCENDIO_FORESTAL = "Incendio forestal"
    INCENDIO_ESTRUCTURAL = "Incendio estructural"
    INUNDACION = "Inundación"
    TERREMOTO = "Terremoto"
    ALUVION = "Aluvión"
    OTRO = "Otro"
