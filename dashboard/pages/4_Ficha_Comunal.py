import streamlit as st
import utils
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Ficha Comunal - EDAN", page_icon="🏙️", layout="wide")

st.title("🏙️ Ficha Comunal")
st.caption("Resumen agregado de situación por Comuna")
st.markdown("---")

# --- Filtro General ---
st.sidebar.header("Selección Territorial")

# Cargar comunas
query_comunas = "SELECT DISTINCT comuna FROM formularios_edan ORDER BY comuna"
df_comunas = utils.load_data(query_comunas)

if df_comunas.empty:
    st.warning("No hay datos disponibles.")
    st.stop()

comunas_lista = df_comunas['comuna'].tolist()
comuna_selec = st.sidebar.selectbox("Seleccionar Comuna", comunas_lista)

st.header(f"📍 Comuna: {comuna_selec}")

# --- KPIs Comunales ---
col1, col2, col3 = st.columns(3)

# Total Reportes
query_kpi = f"SELECT count(*) as total, sum(poblacion_estimada) as pob FROM formularios_edan WHERE comuna = '{comuna_selec}'"
df_kpi = utils.load_data(query_kpi)
total_reportes = df_kpi.iloc[0]['total']
pob_estimada = df_kpi.iloc[0]['pob']

col1.metric("Reportes Emitidos", total_reportes)
col2.metric("Población Estimada Afectada", f"{int(pob_estimada):,}" if pob_estimada else "0")

# --- ALERTAS CRÍTICAS DE LA COMUNA ---
st.subheader("🔴 Riesgos Críticos Detectados")

query_riesgos_comuna = f"""
SELECT DISTINCT
    c.descripcion as factor,
    COUNT(*) as frecuencia
FROM respuestas_edan r
JOIN catalogo_edan c ON r.item_id = c.id
JOIN formularios_edan f ON r.formulario_id = f.id
WHERE f.comuna = '{comuna_selec}' 
  AND c.seccion = 'FACTORES_RIESGO' 
  AND r.valor_escala::text IN ('GRAVE', 'MEDIO')
GROUP BY c.descripcion
ORDER BY frecuencia DESC
"""
df_riesgos = utils.load_data(query_riesgos_comuna)

if not df_riesgos.empty:
    for _, row in df_riesgos.iterrows():
        st.error(f"⚠️ {row['factor']} (Detectado en {row['frecuencia']} reportes)")
else:
    st.success("✅ No se detectan riesgos GRAVES o MEDIOS en esta comuna.")

st.markdown("---")

# --- NECESIDADES PRIORITARIAS DE LA COMUNA ---
st.subheader("⚠️ Necesidades NO Resueltas")

query_necesidades_comuna = f"""
SELECT 
    c.descripcion as necesidad,
    c.seccion,
    COUNT(*) as cantidad
FROM respuestas_edan r
JOIN catalogo_edan c ON r.item_id = c.id
JOIN formularios_edan f ON r.formulario_id = f.id
WHERE f.comuna = '{comuna_selec}' 
  AND c.seccion::text LIKE 'NECESIDADES_%' 
  AND r.valor_escala::text = 'NO_RESUELTO'
GROUP BY c.descripcion, c.seccion
ORDER BY cantidad DESC
"""
df_necesidades = utils.load_data(query_necesidades_comuna)

if not df_necesidades.empty:
    fig = px.bar(
        df_necesidades,
        y='necesidad',
        x='cantidad',
        orientation='h',
        title="Necesidades No Resueltas (Frecuencia)",
        color='seccion',
        text='cantidad'
    )
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("No hay necesidades pendientes de resolución crítica.")

st.markdown("---")

# --- RECURSOS DISPONIBLES ---
st.subheader("🟢 Recursos Habilitados")
query_recursos = f"""
SELECT 
    c.descripcion as recurso,
    COUNT(*) as cantidad
FROM respuestas_edan r
JOIN catalogo_edan c ON r.item_id = c.id
JOIN formularios_edan f ON r.formulario_id = f.id
WHERE f.comuna = '{comuna_selec}' 
  AND c.seccion IN ('RECURSOS_HUMANOS', 'RECURSOS_MATERIALES')
  AND r.valor_bool = true
GROUP BY c.descripcion
"""
df_recursos = utils.load_data(query_recursos)

if not df_recursos.empty:
    st.dataframe(df_recursos, use_container_width=True, hide_index=True)
else:
    st.warning("No se reportan recursos activos.")
