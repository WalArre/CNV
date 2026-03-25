import streamlit as st
import pandas as pd

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

# --- CARGA DE DATOS PARA INYECTAR EN EL HTML ---
df_tx = pd.read_csv("transacciones.csv")
df_crono = pd.read_csv("cronologia.csv")

# Cálculo de variables dinámicas
total_perjuicio = df_tx[df_tx['Tipo'].isin(['Inversion', 'Extorsion'])]['Monto'].sum() - df_tx[df_tx['Tipo'] == 'Recupero']['Monto'].sum()

# --- CONSTRUCCIÓN DEL HTML TÁCTICO ---
# Aquí inyectamos el CSS de tu dashboard original
html_template = f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500;700&display=swap');

    :root {{
        --bg-dark: #09090b;
        --surface-dark: #18181b;
        --neon-cyan: #00f3ff;
        --neon-purple: #b026ff;
        --neon-green: #39ff14;
        --neon-red: #ff003c;
        --text-main: #f8fafc;
    }}

    .main-container {{
        background-color: var(--bg-dark);
        color: var(--text-main);
        padding: 20px;
        font-family: 'Inter', sans-serif;
    }}

    .header {{
        border-bottom: 2px solid var(--neon-cyan);
        padding-bottom: 15px;
        margin-bottom: 30px;
    }}

    .grid-kpi {{
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 15px;
        margin-bottom: 30px;
    }}

    .kpi-card {{
        background: var(--surface-dark);
        border: 1px solid #27272a;
        border-left: 4px solid var(--neon-cyan);
        padding: 20px;
        border-radius: 4px;
    }}

    .kpi-value {{
        font-family: 'JetBrains Mono', monospace;
        font-size: 1.8rem;
        color: var(--neon-green);
        font-weight: bold;
    }}

    /* Estilo Timeline Original */
    .timeline {{
        position: relative;
        padding-left: 30px;
        border-left: 2px solid #27272a;
    }}

    .timeline-item {{ margin-bottom: 30px; position: relative; }}
    .dot {{
        position: absolute; left: -37px; top: 5px;
        width: 12px; height: 12px; border-radius: 50%;
        background: var(--neon-cyan);
        box-shadow: 0 0 10px var(--neon-cyan);
    }}

    .dot-red {{ background: var(--neon-red); box-shadow: 0 0 10px var(--neon-red); }}
    .dot-purple {{ background: var(--neon-purple); box-shadow: 0 0 10px var(--neon-purple); }}
</style>

<div class="main-container">
    <div class="header">
        <h1 style="color: var(--neon-cyan); margin:0;">🛰️ MONITOR TÁCTICO V6</h1>
        <p style="color: #a1a1aa; margin:5px 0;">INVESTIGACIÓN: IPP 415/26 - URRUCHÚA</p>
    </div>

    <div class="grid-kpi">
        <div class="kpi-card">
            <div style="font-size: 0.8rem; color: #a1a1aa;">PERJUICIO NETO</div>
            <div class="kpi-value">${total_perjuicio:,.2f}</div>
        </div>
        <div class="kpi-card" style="border-left-color: var(--neon-purple)">
            <div style="font-size: 0.8rem; color: #a1a1aa;">CAUSAS CONEXAS</div>
            <div class="kpi-value" style="color: var(--neon-purple)">PUENTE HNOS</div>
        </div>
    </div>

    <div style="display: flex; flex-wrap: wrap; gap: 30px;">
        <div style="flex: 2; min-width: 300px;">
            <h3 style="border-bottom: 1px solid #27272a; padding-bottom:10px;">📊 Últimos Movimientos</h3>
            <table style="width: 100%; border-collapse: collapse; font-family: 'JetBrains Mono';">
                <tr style="text-align: left; color: #a1a1aa; font-size: 0.8rem;">
                    <th style="padding: 10px; border-bottom: 1px solid #27272a;">FECHA</th>
                    <th style="padding: 10px; border-bottom: 1px solid #27272a;">MONTO</th>
                    <th style="padding: 10px; border-bottom: 1px solid #27272a;">DESTINO</th>
                </tr>
                {"".join([f"<tr style='border-bottom: 1px solid #1f1f23'><td style='padding:10px'>{r['Fecha']}</td><td style='padding:10px; color:var(--neon-green)'>${r['Monto']:,.2f}</td><td style='padding:10px'>{r['Entidad_Receptora']}</td></tr>" for _, r in df_tx.head(10).iterrows()])}
            </table>
        </div>

        <div style="flex: 1; min-width: 300px;">
            <h3 style="border-bottom: 1px solid #27272a; padding-bottom:10px;">⏳ Timeline Operativa</h3>
            <div class="timeline">
                {"".join([f"<div class='timeline-item'><div class='dot'></div><div style='color:var(--neon-cyan); font-weight:bold; font-size:0.8rem;'>{r['Fecha']}</div><div style='font-weight:bold;'>{r['Evento']}</div><div style='color:#a1a1aa; font-size:0.85rem;'>{r['Detalle_Operativo']}</div></div>" for _, r in df_crono.iterrows()])}
            </div>
        </div>
    </div>
</div>
"""

# Renderizado final del HTML
st.markdown(html_template, unsafe_allow_html=True)

# Botones de exportación al final (fuera del HTML inyectado para que funcionen bien)
st.markdown("---")
c1, c2 = st.columns(2)
with c1:
    st.download_button("📥 Descargar CSV", df_tx.to_csv(index=False), "investigacion_ipp415.csv", use_container_width=True)
with c2:
    if st.button("🚪 Cerrar Sesión", use_container_width=True):
        st.session_state.autenticado = False
        st.rerun()
