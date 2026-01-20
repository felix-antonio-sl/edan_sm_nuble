import streamlit as st
import utils
import pandas as pd

st.set_page_config(page_title="Detalle EDAN - EDAN", page_icon="📄", layout="wide")

st.title("📄 Detalle de Formularios EDAN")
st.caption("Revisión completa de cada evaluación realizada")
st.markdown("---")

# --- Filtros Globales ---
st.sidebar.header("Filtros")

# Cargar comunas disponibles
query_comunas = "SELECT DISTINCT comuna FROM formularios_edan ORDER BY comuna"
df_comunas = utils.load_data(query_comunas)
todas_comunas = ["TODAS"] + df_comunas['comuna'].tolist() if not df_comunas.empty else ["TODAS"]

comuna_selec = st.sidebar.selectbox("Filtrar por Comuna", todas_comunas)

# Filtro por Establecimiento (Institución)
query_inst = "SELECT DISTINCT institucion FROM formularios_edan WHERE institucion IS NOT NULL ORDER BY institucion"
df_inst = utils.load_data(query_inst)
todas_inst = ["TODOS"] + df_inst['institucion'].tolist() if not df_inst.empty else ["TODOS"]

inst_selec = st.sidebar.selectbox("Filtrar por Establecimiento", todas_inst)

# --- Cargar lista de formularios ---
conditions = []
if comuna_selec != "TODAS":
    conditions.append(f"f.comuna = '{comuna_selec}'")
if inst_selec != "TODOS":
    conditions.append(f"f.institucion = '{inst_selec}'")

where_clause = ""
if conditions:
    where_clause = "WHERE " + " AND ".join(conditions)
    
# Se elimina referencia a 'folio' column que no existe. Usamos ID corto.
query_formularios = f"""
SELECT 
    f.id,
    SUBSTRING(f.id, 1, 8) as folio_corto,
    f.comuna,
    f.provincia,
    f.fecha_informe::date as fecha,
    f.poblacion_estimada,
    e.nombre as evaluador
FROM formularios_edan f
LEFT JOIN evaluadores e ON f.evaluador_id = e.id
{where_clause}
ORDER BY f.fecha_informe DESC
"""
df_formularios = utils.load_data(query_formularios)

if df_formularios.empty:
    st.info("No hay formularios EDAN completados.")
    st.stop()

# --- Selector de formulario ---
st.subheader("Seleccionar Formulario")

# Crear opciones legibles
opciones = {}
for _, row in df_formularios.iterrows():
    # Usamos el substring del ID como folio visual
    folio_visual = f"{row['folio_corto']}..."
    label = f"📋 {folio_visual} - {row['comuna']} ({row['fecha']})"
    opciones[label] = row['id']

seleccion = st.selectbox("Formulario:", list(opciones.keys()))
formulario_id = opciones[seleccion]

st.markdown("---")

# --- Datos Generales del Formulario ---
st.subheader("📌 Datos Generales")

df_seleccionado = df_formularios[df_formularios['id'] == formulario_id].iloc[0]

# Obtener instancia completa para datos que no estaban en la vista previa
col1, col2, col3 = st.columns(3)
col1.write(f"**Folio ID:** {df_seleccionado['id']}")
col1.write(f"**Comuna:** {df_seleccionado['comuna']}")
col2.write(f"**Provincia:** {df_seleccionado['provincia']}")
col2.write(f"**Población Estimada:** {df_seleccionado['poblacion_estimada']:,}")
col3.write(f"**Fecha:** {df_seleccionado['fecha']}")
col3.write(f"**Evaluador:** {df_seleccionado['evaluador'] or 'No registrado'}")

st.markdown("---")

# --- Respuestas por Sección ---
st.subheader("📝 Respuestas Detalladas")

# Cast valor_escala a text para evitar problemas con Enums en python
query_respuestas = f"""
SELECT 
    c.seccion,
    c.codigo,
    c.descripcion,
    r.valor_escala::text as valor_escala_str,
    r.valor_bool,
    r.valor_cantidad
FROM respuestas_edan r
JOIN catalogo_edan c ON r.item_id = c.id
WHERE r.formulario_id = '{formulario_id}'
ORDER BY c.seccion, c.orden
"""
df_respuestas = utils.load_data(query_respuestas)

if df_respuestas.empty:
    st.warning("Este formulario no tiene respuestas registradas.")
else:
    # Agrupar por sección
    secciones = df_respuestas['seccion'].unique()
    
    for seccion in secciones:
        seccion_label = seccion.replace('_', ' ').title()
        
        with st.expander(f"📂 {seccion_label}", expanded=True):
            df_seccion = df_respuestas[df_respuestas['seccion'] == seccion]
            
            for _, resp in df_seccion.iterrows():
                codigo = resp['codigo']
                descripcion = resp['descripcion']
                
                # Determinar el valor a mostrar
                if resp['valor_escala_str']:
                    valor = resp['valor_escala_str']
                    if valor == 'GRAVE':
                        st.error(f"**{codigo}** - {descripcion}: 🔴 {valor}")
                    elif valor == 'MEDIO':
                        st.warning(f"**{codigo}** - {descripcion}: 🟠 {valor}") # MEDIO, no MODERADO
                    elif valor == 'BAJO':
                        st.info(f"**{codigo}** - {descripcion}: 🟡 {valor}") # BAJO, no LEVE
                    elif valor == 'NO_RESUELTO':
                        st.error(f"**{codigo}** - {descripcion}: ❌ NO RESUELTO")
                    elif valor == 'RESUELTO':
                        st.success(f"**{codigo}** - {descripcion}: ✅ RESUELTO")
                    else:
                        st.write(f"**{codigo}** - {descripcion}: {valor}")
                elif resp['valor_bool'] is not None:
                    if resp['valor_bool']:
                        st.success(f"**{codigo}** - {descripcion}: ✅ Sí")
                    else:
                        st.write(f"**{codigo}** - {descripcion}: ❌ No")
                elif resp['valor_cantidad'] is not None:
                    st.write(f"**{codigo}** - {descripcion}: **{resp['valor_cantidad']}**")
                else:
                    st.write(f"**{codigo}** - {descripcion}: *Sin respuesta*")

st.markdown("---")

# --- Comentarios de Síntesis ---
st.subheader("💬 Comentarios de Síntesis")

query_comentarios = f"""
SELECT sintesis_necesidades, comentarios_necesidades, acciones_realizar
FROM formularios_edan
WHERE id = '{formulario_id}'
"""
df_comentarios = utils.load_data(query_comentarios)

if not df_comentarios.empty:
    row = df_comentarios.iloc[0]
    
    if row['sintesis_necesidades']:
        st.write("**Síntesis de Necesidades:**")
        st.info(row['sintesis_necesidades'])
        
    if row['comentarios_necesidades']:
        st.write("**Comentarios Adicionales:**")
        st.text_area("", row['comentarios_necesidades'], height=100, disabled=True, key="com_nec")
        
    if row['acciones_realizar']:
        st.write("**Acciones a Realizar:**")
        st.success(row['acciones_realizar'])
        
    if not (row['sintesis_necesidades'] or row['comentarios_necesidades'] or row['acciones_realizar']):
        st.info("No se registraron comentarios de síntesis.")
