import streamlit as st
import pandas as pd

# CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="MONITOR TÁCTICO IPP 415/26", layout="wide")

# --- ESTILOS NEÓN ORIGINALES (CSS INYECTADO) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&display=swap');
    
    .stApp { background-color: #09090b; color: #f8fafc; font-family: 'JetBrains Mono', monospace; }
    
    /* Contenedores Estilo Tarjeta */
    .tactic-card {
        background: #18181b;
        border: 1px solid #27272a;
        border-left: 4px solid #00f3ff;
        padding: 15px;
        border-radius: 4px;
        margin-bottom: 10px;
    }
    
    .metric-value { font-size: 24px; font-weight: bold; color: #39ff14; }
    .metric-label { font-size: 12px; color: #a1a1aa; text-transform: uppercase; }

    /* Estilo Timeline (Copiado de tu original) */
    .tl-container { border-left: 2px solid #27272a; margin-left: 20px; padding-left: 20px; position: relative; }
    .tl-item { margin-bottom: 20px; position: relative; }
    .tl-dot { 
        position: absolute; left: -27px; top: 5px; 
        width: 12px; height: 12px; border-radius: 50%; 
    }
    .dot-cyan { background: #00f3ff; box-shadow: 0 0 10px #00f3ff; }
    .dot-purple { background: #b026ff; box-shadow: 0 0 10px #b026ff; }
    .dot-red { background: #ff003c; box-shadow: 0 0 10px #ff003c; }
    .tl-date { color: #00f3ff; font-weight: bold; font-size: 0.85em; }
    .tl-event { color: #f8fafc; font-weight: bold; margin: 5px 0; }
    .tl-desc { color: #a1a1aa; font-size: 0.9em; }
</style>
""", unsafe_allow_html=True)

# --- CARGA DE DATOS ---
df_tx = pd.read_csv("transacciones.csv")
df_crono = pd.read_csv("cronologia.csv")

# --- HEADER TÁCTICO ---
st.markdown("""
    <div style='border-bottom: 2px solid #00f3ff; padding-bottom:10px; margin-bottom:20px'>
        <h2 style='margin:0; color:#00f3ff;'>🛰️ SISTEMA DE MONITOREO - IPP 415/26</h2>
        <small style='color:#a1a1aa;'>UNIDAD DE INTELIGENCIA OPERATIVA - BASE VILLA SANTA RITA</small>
    </div>
""", unsafe_allow_html=True)

# --- FILAS SUPERIORES: KPIs ---
c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown(f"<div class='tactic-card'><div class='metric-label'>Perjuicio Neto</div><div class='metric-value'>$ 23.444.647</div></div>", unsafe_allow_html=True)
with c2:
    st.markdown(f"<div class='tactic-card' style='border-left-color:#ffb000'><div class='metric-label'>Estado Dominio</div><div class='metric-value' style='color:#ffb000'>CLIENT HOLD</div></div>", unsafe_allow_html=True)
with c3:
    st.markdown(f"<div class='tactic-card' style='border-left-color:#b026ff'><div class='metric-label'>Causas Conexas</div><div class='metric-value' style='color:#b026ff'>PUENTE HNOS</div></div>", unsafe_allow_html=True)
with c4:
    st.markdown(f"<div class='tactic-card' style='border-left-color:#39ff14'><div class='metric-label'>Recupero Parcial</div><div class='metric-value' style='color:#39ff14'>$ 556.869</div></div>", unsafe_allow_html=True)

# --- CUERPO PRINCIPAL ---
col_main, col_side = st.columns([2, 1])

with col_main:
    st.subheader("📊 Análisis de Nodos y Transacciones")
    # Filtro rápido
    busqueda = st.text_input("🔍 Buscar CUIT / Alias / CBU...", "")
    
    if busqueda:
        resultado = df_tx[df_tx.astype(str).apply(lambda x: x.str.contains(busqueda, case=False)).any(axis=1)]
        st.dataframe(resultado, use_container_width=True)
    else:
        st.dataframe(df_tx, use_container_width=True)

    st.markdown("### 🗺️ Mapa de Billeteras Mulas")
    # Aquí podrías poner el mapa de red anterior o una tabla resumen
    st.info("Visualización optimizada para 55 pulgadas. Use Ctrl+R para refrescar datos desde GitHub.")

with col_side:
    st.subheader("⏳ Línea de Tiempo Operativa")
    
    # Generador de Timeline con el estilo de tu HTML
    st.markdown("<div class='tl-container'>", unsafe_allow_html=True)
    for _, row in df_crono.iterrows():
        # Lógica de colores según fase
        color_class = "dot-cyan"
        if "Extorsion" in row['Fase']: color_class = "dot-red"
        if "Judicial" in row['Fase']: color_class = "dot-purple"
        
        st.markdown(f"""
            <div class='tl-item'>
                <div class='tl-dot {color_class}'></div>
                <div class='tl-date'>{row['Fecha']}</div>
                <div class='tl-event'>{row['Evento']}</div>
                <div class='tl-desc'>{row['Detalle_Operativo']}</div>
            </div>
        """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# --- BOTONES DE ACCIÓN (Sidebar para no ensuciar el monitor) ---
with st.sidebar:
    st.title("OPCIONES")
    if st.button("📥 Generar Reporte PDF"):
        st.write("Generando dossier...")
    st.download_button("📂 Descargar Excel", df_tx.to_csv(), "investigacion_415.csv")
        df_nodos_filtrado = df_nodos[df_nodos.apply(lambda row: row.astype(str).str.contains(search_query, case=False).any(), axis=1)]
        st.dataframe(df_nodos_filtrado, use_container_width=True)
        if not df_nodos_filtrado.empty:
            st.success("¡Coincidencia encontrada!")
        else:
            st.warning("Sin resultados.")
    else:
        st.dataframe(df_nodos, use_container_width=True)

# --- MÓDULO DE EXPORTACIÓN (REPORTES) ---
st.sidebar.markdown("---")
st.sidebar.title("📥 Exportar Inteligencia")

# 1. Exportar a CSV/Excel
csv = df_tx_filtrado.to_csv(index=False).encode('utf-8')
st.sidebar.download_button(
    label="Descargar Transacciones (CSV)",
    data=csv,
    file_name='reporte_transacciones_ipp415.csv',
    mime='text/csv',
)

# 2. Generador de PDF
def generar_pdf():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt="Dossier de Inteligencia - IPP 415/26", ln=True, align='C')
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"Perjuicio Neto Calculado: ${perjuicio_neto:,.2f}", ln=True, align='L')
    pdf.cell(200, 10, txt="Resumen de Operaciones Filtradas:", ln=True, align='L')
    
    # Agregar algunos datos al PDF
    pdf.set_font("Arial", size=10)
    for i, row in df_tx_filtrado.head(10).iterrows():
        texto_linea = f"{row['Fecha']} - {row['Tipo']} - ${row['Monto']} -> {row['Entidad_Receptora']}"
        pdf.cell(200, 8, txt=texto_linea, ln=True, align='L')
        
    return pdf.output(dest='S').encode('latin1')

st.sidebar.download_button(
    label="Generar Dossier Policial (PDF)",
    data=generar_pdf(),
    file_name="Dossier_Tactico_IPP415.pdf",
    mime="application/pdf"
)
