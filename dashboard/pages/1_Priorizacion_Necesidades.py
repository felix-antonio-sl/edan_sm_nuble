import streamlit as st
import utils
import pandas as pd

st.set_page_config(page_title="Priorización - EDAN", page_icon="📋", layout="wide")

st.title("📋 Priorización de Necesidades")
st.caption("Necesidades ordenadas por urgencia para toma de decisiones")
st.markdown("---")

# --- Selector de tipo de necesidad ---
tipo_necesidad = st.selectbox(
    "Filtrar por tipo de necesidad:",
    ["TODAS", "NECESIDADES_PSICOSOCIALES", "NECESIDADES_INSTITUCIONALES", "NECESIDADES_BASICAS"]
)

where_clause = ""
if tipo_necesidad != "TODAS":
    where_clause = f"AND c.seccion = '{tipo_necesidad}'"

# --- NECESIDADES NO RESUELTAS ---
st.subheader("🔴 Necesidades NO RESUELTAS")

query_no_resueltas = f"""
SELECT 
    c.seccion,
    c.descripcion as necesidad,
    COUNT(DISTINCT f.comuna) as comunas,
    COUNT(*) as reportes,
    STRING_AGG(DISTINCT f.comuna, ', ') as comunas_lista
FROM respuestas_edan r
JOIN catalogo_edan c ON r.item_id = c.id
JOIN formularios_edan f ON r.formulario_id = f.id
WHERE c.seccion::text LIKE 'NECESIDADES_%' AND r.valor_escala::text = 'NO_RESUELTO' {where_clause}
GROUP BY c.seccion, c.descripcion
ORDER BY comunas DESC, reportes DESC
"""
df_no_resueltas = utils.load_data(query_no_resueltas)

if not df_no_resueltas.empty:
    for _, row in df_no_resueltas.iterrows():
        with st.expander(f"❌ {row['necesidad']} ({row['comunas']} comunas)"):
            st.write(f"**Categoría:** {row['seccion'].replace('_', ' ').title()}")
            st.write(f"**Comunas afectadas:** {row['comunas_lista']}")
            st.write(f"**Total reportes:** {row['reportes']}")
else:
    st.success("✅ No hay necesidades marcadas como NO RESUELTAS.")

st.markdown("---")


# --- RESUMEN ESTADÍSTICO ---
st.subheader("📊 Resumen de Estado de Necesidades")

query_resumen = """
SELECT 
    r.valor_escala as estado,
    COUNT(*) as cantidad
FROM respuestas_edan r
JOIN catalogo_edan c ON r.item_id = c.id
WHERE c.seccion::text LIKE 'NECESIDADES_%'
GROUP BY r.valor_escala
ORDER BY cantidad DESC
"""
df_resumen = utils.load_data(query_resumen)

if not df_resumen.empty:
    col1, col2, col3 = st.columns(3)
    for _, row in df_resumen.iterrows():
        estado = row['estado']
        cantidad = row['cantidad']
        if estado == 'NO_RESUELTO':
            col1.metric("❌ No Resuelto", cantidad)
        elif estado == 'RESUELTO':
            col2.metric("✅ Resuelto", cantidad)
