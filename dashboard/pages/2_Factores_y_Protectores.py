import streamlit as st
import utils
import pandas as pd

st.set_page_config(page_title="Factores - EDAN", page_icon="⚖️", layout="wide")

st.title("⚖️ Balance Riesgo / Protección")
st.caption("Análisis de factores de riesgo y factores protectores")
st.markdown("---")

# --- FACTORES DE RIESGO ---
st.subheader("🔴 Factores de Riesgo identificados")

# Usar cast ::text para evitar errores de enum
query_riesgo = """
SELECT 
    c.descripcion as factor,
    r.valor_escala as gravedad,
    COUNT(*) as reportes
FROM respuestas_edan r
JOIN catalogo_edan c ON r.item_id = c.id
WHERE c.seccion = 'FACTORES_RIESGO' AND r.valor_escala::text IN ('GRAVE', 'MEDIO', 'BAJO')
GROUP BY c.descripcion, r.valor_escala
ORDER BY 
    CASE r.valor_escala::text
        WHEN 'GRAVE' THEN 1 
        WHEN 'MEDIO' THEN 2 
        WHEN 'BAJO' THEN 3 
    END,
    reportes DESC
"""
df_riesgo = utils.load_data(query_riesgo)

if not df_riesgo.empty:
    # Convertir a texto por si acaso
    df_riesgo['gravedad'] = df_riesgo['gravedad'].astype(str)
    
    graves = df_riesgo[df_riesgo['gravedad'] == 'GRAVE']
    medios = df_riesgo[df_riesgo['gravedad'] == 'MEDIO']
    bajos = df_riesgo[df_riesgo['gravedad'] == 'BAJO']
    
    if not graves.empty:
        st.error("**GRAVES:**")
        for _, row in graves.iterrows():
            st.write(f"- 🔴 {row['factor']} ({row['reportes']} reportes)")
    
    if not medios.empty:
        st.warning("**MEDIOS:**")
        for _, row in medios.iterrows():
            st.write(f"- 🟠 {row['factor']} ({row['reportes']} reportes)")
    
    if not bajos.empty:
        with st.expander("Ver factores BAJOS"):
            for _, row in bajos.iterrows():
                st.write(f"- 🟡 {row['factor']} ({row['reportes']} reportes)")
else:
    st.info("No hay factores de riesgo registrados con gravedad considerable.")

st.markdown("---")

# --- FACTORES PROTECTORES ---
st.subheader("🟢 Factores Protectores Presentes")

query_protectores = """
SELECT 
    c.descripcion as factor,
    COUNT(*) as reportes
FROM respuestas_edan r
JOIN catalogo_edan c ON r.item_id = c.id
WHERE c.seccion = 'FACTORES_PROTECTORES' AND r.valor_bool = true
GROUP BY c.descripcion
ORDER BY reportes DESC
"""
df_protectores = utils.load_data(query_protectores)

if not df_protectores.empty:
    for _, row in df_protectores.iterrows():
        st.success(f"✅ {row['factor']} ({row['reportes']} reportes)")
else:
    st.warning("No se han identificado factores protectores.")

st.markdown("---")

# --- RATIO RIESGO/PROTECCIÓN ---
st.subheader("📊 Balance General")

col1, col2, col3 = st.columns(3)

# Conteo de riesgos identificados (GRAVE o MEDIO)
query_count_riesgo = """
SELECT COUNT(DISTINCT c.descripcion) as total
FROM respuestas_edan r
JOIN catalogo_edan c ON r.item_id = c.id
WHERE c.seccion = 'FACTORES_RIESGO' AND r.valor_escala::text IN ('GRAVE', 'MEDIO')
"""
df_count_riesgo = utils.load_data(query_count_riesgo)
riesgos = df_count_riesgo.iloc[0]['total'] if not df_count_riesgo.empty else 0

# Conteo de protectores
query_count_prot = """
SELECT COUNT(DISTINCT c.descripcion) as total
FROM respuestas_edan r
JOIN catalogo_edan c ON r.item_id = c.id
WHERE c.seccion = 'FACTORES_PROTECTORES' AND r.valor_bool = true
"""
df_count_prot = utils.load_data(query_count_prot)
protectores = df_count_prot.iloc[0]['total'] if not df_count_prot.empty else 0

col1.metric("Riesgos (Grave/Medio)", riesgos)
col2.metric("Protectores Activos", protectores)

if riesgos > 0 and protectores > 0:
    ratio = round(riesgos / protectores, 2)
    col3.metric("Ratio Riesgo/Protección", f"{ratio}:1")
elif protectores == 0 and riesgos > 0:
    col3.metric("Ratio Riesgo/Protección", "⚠️ Sin protectores")
else:
    col3.metric("Ratio Riesgo/Protección", "N/A - Datos insuficientes")
