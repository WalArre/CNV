import streamlit as st
import streamlit.components.v1 as components
import os

# CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="ACCESO RESTRINGIDO", layout="wide")

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

# --- RESUMEN EJECUTIVO (Agregado arriba del Dashboard) ---
st.markdown("<h3 style='color: #00f3ff; font-family: monospace; margin-bottom: 0;'>📄 SÍNTESIS OPERATIVA - IPP 415/26</h3>", unsafe_allow_html=True)
st.info(
    "La IPP 415/26 detalla una estafa de ingeniería social contra E. Urruchúa, con un perjuicio neto de $21.824.909 "
    "tras descontar maniobras de cebo. La organización utilizó la plataforma alliance-bernstein.top y falsos avales "
    "de la CNV para captar depósitos iniciales destinados a Adrex S.A. Posteriormente, mediante el bloqueo de fondos "
    "bajo la figura de una SPO ficticia, se exigieron pagos extorsivos remitidos a Bringarez S.A., Finanzas Int. SRL "
    "y Nicole Zamorano. Como tareas inmediatas, se enviará el informe a la Fiscalía para solicitar el levantamiento "
    "del secreto bancario de las cuentas denunciadas y sus historiales de transferencia. Además, se cursarán notas a "
    "las empresas de telefonía tras las consultas en ENACOM y se realizarán compulsas en distintas bases de datos "
    "sobre todos los involucrados."
)
st.markdown("---")

# --- RENDERIZADO DEL DASHBOARD ORIGINAL (HTML) ---
try:
    with open("dash FINAL CNV.html", "r", encoding="utf-8") as f:
        html_content = f.read()
    
    # Inyectamos el HTML de forma segura
    components.html(html_content, height=850, scrolling=True)
    
except FileNotFoundError:
    st.error("⚠️ No se encontró el archivo 'dash FINAL CNV.html'. Asegúrese de que el nombre sea exacto y esté subido al repositorio.")

# --- MÓDULO DE EXPORTACIÓN Y SALIDA ---
st.markdown("---")
c1, c2 = st.columns(2)

with c1:
    # Lógica para descargar el PDF estático subido a GitHub
    nombre_pdf = "Resumen_55-26.pdf"
    
    if os.path.exists(nombre_pdf):
        with open(nombre_pdf, "rb") as pdf_file:
            pdf_bytes = pdf_file.read()
            st.download_button(
                label="📥 Descargar Dossier PDF (Resumen 55/26)", 
                data=pdf_bytes, 
                file_name="Resumen_55-26.pdf",
                mime="application/pdf",
                use_container_width=True
            )
    else:
        st.warning(f"⚠️ El archivo '{nombre_pdf}' no se detectó en el servidor. Verifique que esté subido al repositorio de GitHub.")

with c2:
    if st.button("🚪 Cerrar Sesión Operativa", use_container_width=True):
        st.session_state.autenticado = False
        st.rerun()
