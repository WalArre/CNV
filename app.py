import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import os

# CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="SISTEMA TÁCTICO - ACCESO RESTRINGIDO", layout="wide")

# --- SISTEMA DE SEGURIDAD ---
if 'autenticado' not in st.session_state:
    st.session_state.autenticado = False

def verificar_password():
    if st.session_state["password_input"] == "Dicco1272":
        st.session_state.autenticado = True
    else:
        st.error("❌ Credencial de acceso incorrecta. Intente nuevamente.")

if not st.session_state.autenticado:
    # Pantalla de Login
    st.markdown("<br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/c/c8/Escudo_de_la_Polic%C3%ADa_Federal_Argentina.svg/1200px-Escudo_de_la_Polic%C3%ADa_Federal_Argentina.svg.png", width=120)
        st.title("🔐 Acceso Operativo")
        st.text_input("Ingrese Contraseña de Brigada:", type="password", key="password_input", on_change=verificar_password)
        st.info("Investigación Criminal - IPP 415/26 - Sumario 55/26")
    st.stop()

# --- RENDERIZADO DEL DASHBOARD ORIGINAL ---
# Leemos directamente tu archivo HTML
try:
    with open("dash FINAL CNV.html", "r", encoding="utf-8") as f:
        html_content = f.read()
    
    # Inyectamos el HTML de forma segura con un alto fijo para que se vea bien en PC y Celu
    components.html(html_content, height=850, scrolling=True)
    
except FileNotFoundError:
    st.error("⚠️ No se encontró el archivo 'dash FINAL CNV.html'. Asegúrese de que el nombre sea exacto y esté subido al repositorio.")

# --- MÓDULO DE EXPORTACIÓN Y SALIDA ---
st.markdown("---")
c1, c2 = st.columns(2)

with c1:
    # Botón para descargar la base de datos CSV si el archivo existe
    if os.path.exists("transacciones.csv"):
        df_tx = pd.read_csv("transacciones.csv")
        csv_data = df_tx.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Descargar Matriz CSV (Transacciones)", 
            data=csv_data, 
            file_name="investigacion_ipp415.csv", 
            use_container_width=True
        )
    else:
        st.info("El archivo 'transacciones.csv' no está en el servidor para su descarga.")

with c2:
    if st.button("🚪 Cerrar Sesión Operativa", use_container_width=True):
        st.session_state.autenticado = False
        st.rerun()
