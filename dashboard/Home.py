import streamlit as st
import utils
import pandas as pd

st.set_page_config(
    page_title="EDAN Salud Mental - Síntesis",
    page_icon="🚨",
    layout="wide"
)

st.title("🚨 Síntesis Ejecutiva EDAN")
st.caption("Evaluación de Daños y Análisis de Necesidades en Salud Mental - Ñuble")
st.markdown("---")

# --- KPIs Rápidos ---
try:
    kpis = utils.get_kpis()
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("📋 Formularios", kpis["formularios"])
    col2.metric("👥 Población Afectada", f"{int(kpis['poblacion']):,}")
    col3.metric("🏘️ Comunas Evaluadas", kpis["comunas"])
    
    # Último reporte
    query_ultimo = "SELECT MAX(fecha_informe) as ultimo FROM formularios_edan"
    df_ultimo = utils.load_data(query_ultimo)
    if df_ultimo is not None and not df_ultimo.empty and df_ultimo.iloc[0]['ultimo']:
        col4.metric("⏰ Último Reporte", str(df_ultimo.iloc[0]['ultimo'])[:10])
    else:
        col4.metric("⏰ Último Reporte", "Sin datos")

except Exception as e:
    st.error(f"Error conectando a la base de datos: {e}")
    st.stop()

st.markdown("---")

# --- ALERTAS CRÍTICAS (Factores GRAVES) ---
st.subheader("🔴 Alertas Críticas (Factores Graves)")

query_alertas = """
SELECT DISTINCT
    c.descripcion as factor,
    f.comuna,
    f.fecha_informe::date as fecha
FROM respuestas_edan r
JOIN catalogo_edan c ON r.item_id = c.id
JOIN formularios_edan f ON r.formulario_id = f.id
WHERE c.seccion = 'FACTORES_RIESGO' AND r.valor_escala::text = 'GRAVE'
ORDER BY f.fecha_informe DESC
"""
df_alertas = utils.load_data(query_alertas)

if not df_alertas.empty:
    for _, row in df_alertas.iterrows():
        st.error(f"**{row['factor']}** - {row['comuna']} ({row['fecha']})")
else:
    st.success("✅ No hay factores clasificados como GRAVES actualmente.")

st.markdown("---")

# --- NECESIDADES NO RESUELTAS ---
st.subheader("⚠️ Necesidades NO Resueltas (Prioridad)")

query_necesidades = """
SELECT 
    c.descripcion as necesidad,
    COUNT(DISTINCT f.comuna) as comunas_afectadas,
    COUNT(*) as reportes
FROM respuestas_edan r
JOIN catalogo_edan c ON r.item_id = c.id
JOIN formularios_edan f ON r.formulario_id = f.id
WHERE c.seccion::text LIKE 'NECESIDADES_%' AND r.valor_escala::text = 'NO_RESUELTO'
GROUP BY c.descripcion
ORDER BY comunas_afectadas DESC, reportes DESC
LIMIT 10
"""
df_necesidades = utils.load_data(query_necesidades)

if not df_necesidades.empty:
    st.dataframe(
        df_necesidades.rename(columns={
            "necesidad": "Necesidad",
            "comunas_afectadas": "Comunas Afectadas",
            "reportes": "Reportes"
        }),
        use_container_width=True,
        hide_index=True
    )
else:
    st.info("No hay necesidades marcadas como NO RESUELTAS.")

st.markdown("---")

# --- COBERTURA POR COMUNA ---
st.subheader("📍 Cobertura Territorial")

query_cobertura = """
SELECT 
    comuna,
    COUNT(*) as evaluaciones,
    MAX(fecha_informe)::date as ultima_evaluacion,
    SUM(poblacion_estimada) as poblacion_total
FROM formularios_edan
GROUP BY comuna
ORDER BY evaluaciones DESC
"""
df_cobertura = utils.load_data(query_cobertura)

if not df_cobertura.empty:
    st.dataframe(
        df_cobertura.rename(columns={
            "comuna": "Comuna",
            "evaluaciones": "Evaluaciones",
            "ultima_evaluacion": "Última Evaluación",
            "poblacion_total": "Población Total"
        }),
        use_container_width=True,
        hide_index=True
    )
