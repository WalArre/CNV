import streamlit as st
import pandas as pd

# CONFIGURACIÓN DE PÁGINA - Responsiva por defecto
st.set_page_config(page_title="MONITOR TÁCTICO IPP 415/26", layout="wide")

# --- CSS HÍBRIDO (PC/CELULAR) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&display=swap');
    
    /* Configuración Base */
    .stApp { background-color: #09090b; color: #f8fafc; font-family: 'JetBrains Mono', monospace; }
    
    /* Tarjetas Tácticas Responsivas */
    .tactic-card {
        background: #18181b;
        border: 1px solid #27272a;
        border-left: 4px solid #00f3ff;
        padding: 1rem;
        border-radius: 4px;
        margin-bottom: 10px;
        min-height: 100px;
    }
    
    .metric-value { font-size: clamp(1.2rem, 5vw, 1.8rem); font-weight: bold; color: #39ff14; }
    .metric-label { font-size: 0.75rem; color: #a1a1aa; text-transform: uppercase; letter-spacing: 1px; }

    /* Línea de Tiempo Adaptada */
    .tl-container { border-left: 2px solid #27272a; margin-left: 10px; padding-left: 15px; }
    .tl-item { margin-bottom: 25px; position: relative; }
    .tl-dot { 
        position: absolute; left: -22px; top: 6px; 
        width: 12px; height: 12px; border-radius: 50%; 
    }
    .dot-cyan { background: #00f3ff; box-shadow: 0 0 10px #00f3ff; }
    .dot-purple { background: #b026ff; box-shadow: 0 0 10px #b026ff; }
    .dot-red { background: #ff003c; box-shadow: 0 0 10px #ff003c; }
    .dot-green { background: #39ff14; box-shadow: 0 0 10px #39ff14; }
    
    .tl-date { color: #00f3ff; font-weight: bold; font-size: 0.8rem; }
    .tl-event { color: #f8fafc; font-weight: bold; margin: 2px 0; font-size: 0.95rem; }
    .tl-desc { color: #a1a1aa; font-size: 0.85rem; line-height: 1.3; }

    /* Ajuste de tablas para móvil */
    [data-testid="stDataFrame"] { width: 100%; border: 1px solid #27272a; border-radius: 4px; }
</style>
""", unsafe_allow_html=True)

# --- CARGA DE DATOS ---
@st.cache_data
def load_data():
    df_tx = pd.read_csv("transacciones.csv")
    df_crono = pd.read_csv("cronologia.csv")
    return df_tx, df_crono

df_tx, df_crono = load_data()

# --- HEADER TÁCTICO ---
st.markdown("""
    <div style='border-bottom: 2px solid #00f3ff; padding-bottom:10px; margin-bottom:20px; text-align: left;'>
        <h2 style='margin:0; color:#00f3ff; font-size: clamp(1.2rem, 6vw, 2rem);'>🛰️ MONITOR IPP 415/26</h2>
        <small style='color:#a1a1aa;'>UNIDAD DE INTELIGENCIA - VILLA SANTA RITA</small>
    </div>
""", unsafe_allow_html=True)

# --- SECCIÓN DE MÉTRICAS (KPIs) ---
# En móvil, Streamlit apila estas columnas automáticamente
c1, c2, c3, c4 = st.columns([1,1,1,1])
with c1:
    st.markdown("<div class='tactic-card'><div class='metric-label'>Perjuicio Neto</div><div class='metric-value'>$ 23.4M</div></div>", unsafe_allow_html=True)
with c2:
    st.markdown("<div class='tactic-card' style='border-left-color:#ffb000'><div class='metric-label'>Estado Dominio</div><div class='metric-value' style='color:#ffb000'>HOLD</div></div>", unsafe_allow_html=True)
with c3:
    st.markdown("<div class='tactic-card' style='border-left-color:#b026ff'><div class='metric-label'>Causas</div><div class='metric-value' style='color:#b026ff'>PUENTE</div></div>", unsafe_allow_html=True)
with c4:
    st.markdown("<div class='tactic-card' style='border-left-color:#39ff14'><div class='metric-label'>Recupero</div><div class='metric-value' style='color:#39ff14'>$ 556K</div></div>", unsafe_allow_html=True)

# --- CUERPO PRINCIPAL (TABS PARA MEJOR NAVEGACIÓN EN MÓVIL) ---
# Usar pestañas permite que en el celular no tengas que hacer un scroll infinito
tab1, tab2, tab3 = st.tabs(["📊 FLUJO BANCARIO", "⏳ TIMELINE", "📂 REPORTES"])

with tab1:
    st.subheader("Análisis de Transacciones")
    busqueda = st.text_input("🔍 Buscar CUIT, Alias o Entidad...", placeholder="Ej: Adrex")
    
    if busqueda:
        mask = df_tx.apply(lambda x: x.astype(str).str.contains(busqueda, case=False)).any(axis=1)
        df_filtrado = df_tx[mask]
    else:
        df_filtrado = df_tx
        
    st.dataframe(df_filtrado, use_container_width=True, hide_index=True)

with tab2:
    st.subheader("Línea de Tiempo Operativa")
    st.markdown("<div class='tl-container'>", unsafe_allow_html=True)
    for _, row in df_crono.iterrows():
        # Lógica de colores según la fase del HTML original
        color_class = "dot-cyan" # Fase 1/2
        if "Extorsion" in row['Fase']: color_class = "dot-red"
        if "Judicial" in row['Fase']: color_class = "dot-purple"
        if "Recupero" in row['Evento'] or "Repatriación" in row['Evento']: color_class = "dot-green"
        
        st.markdown(f"""
            <div class='tl-item'>
                <div class='tl-dot {color_class}'></div>
                <div class='tl-date'>{row['Fecha']}</div>
                <div class='tl-event'>{row['Evento']}</div>
                <div class='tl-desc'>{row['Detalle_Operativo']}</div>
            </div>
        """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

with tab3:
    st.subheader("Exportación de Datos")
    st.info("Desde aquí podés descargar la matriz completa para pericias externas.")
    
    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        st.download_button(
            label="📄 Descargar Excel (.csv)",
            data=df_tx.to_csv(index=False),
            file_name="Matriz_IPP415_26.csv",
            mime="text/csv",
            use_container_width=True
        )
    with col_btn2:
        # Botón placeholder para el PDF
        if st.button("📑 Generar Reporte PDF", use_container_width=True):
            st.warning("Función de PDF en preparación para descarga móvil.")

# --- FOOTER ---
st.markdown("---")
st.caption("Acceso Restringido - Sistema de Monitoreo PFA - Actualizado vía GitHub")
