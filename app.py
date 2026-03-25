import streamlit as st
import pandas as pd
import networkx as nx
from pyvis.network import Network
import streamlit.components.v1 as components
import plotly.express as px
import io
from fpdf import FPDF

# --- CONFIGURACIÓN DE PÁGINA Y ESTÉTICA TÁCTICA ---
st.set_page_config(page_title="Monitor Táctico - IPP 415/26", layout="wide", initial_sidebar_state="expanded")

# Inyección de CSS para forzar el Dark Mode y estilo Neón (Monitor Táctico)
st.markdown("""
    <style>
    .stApp { background-color: #09090b; color: #f8fafc; }
    .css-1d391kg { background-color: #18181b; } /* Sidebar */
    h1, h2, h3 { color: #00f3ff; font-family: 'JetBrains Mono', monospace; }
    .stMetric label { color: #a1a1aa !important; }
    .stMetric [data-testid="stMetricValue"] { color: #39ff14 !important; }
    </style>
""", unsafe_allow_html=True)

# --- CARGA DE DATOS ---
@st.cache_data
def load_data():
    df_tx = pd.read_csv("transacciones.csv")
    df_nodos = pd.read_csv("nodos_objetivos.csv")
    df_crono = pd.read_csv("cronologia.csv")
    return df_tx, df_nodos, df_crono

df_tx, df_nodos, df_crono = load_data()

# --- SIDEBAR: FILTROS TÁCTICOS ---
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/thumb/c/c8/Escudo_de_la_Polic%C3%ADa_Federal_Argentina.svg/1200px-Escudo_de_la_Polic%C3%ADa_Federal_Argentina.svg.png", width=100)
st.sidebar.title("Comandos de Filtrado")
st.sidebar.markdown("---")

# Filtro por tipo de transacción
tipos_tx = st.sidebar.multiselect("Filtrar Tipo de Operación", options=df_tx["Tipo"].unique(), default=df_tx["Tipo"].unique())
df_tx_filtrado = df_tx[df_tx["Tipo"].isin(tipos_tx)]

# Buscador Global
st.sidebar.markdown("### Buscador Global (Nodos)")
search_query = st.sidebar.text_input("Ingresar CUIT, Teléfono, Alias o Nombre:")

# --- PANEL CENTRAL ---
st.title("🖥️ Monitor Táctico de Inteligencia - Sumario 55/26")
st.markdown("Visualización en tiempo real de flujos financieros y mapeo de actores involucrados en la estructura investigada.")

# --- KPIs (Métricas Financieras) ---
col1, col2, col3, col4 = st.columns(4)
total_inversion = df_tx_filtrado[df_tx_filtrado["Tipo"] == "Inversion"]["Monto"].sum()
total_extorsion = df_tx_filtrado[df_tx_filtrado["Tipo"] == "Extorsion"]["Monto"].sum()
total_recupero = df_tx_filtrado[df_tx_filtrado["Tipo"] == "Recupero"]["Monto"].sum()
perjuicio_neto = (total_inversion + total_extorsion) - total_recupero

col1.metric("Capital Invertido (Real)", f"${total_inversion:,.2f}")
col2.metric("Pagos Extorsivos", f"${total_extorsion:,.2f}")
col3.metric("Fondos Recuperados", f"${total_recupero:,.2f}")
col4.metric("Perjuicio Neto", f"${perjuicio_neto:,.2f}")

st.markdown("---")

# --- GRAFO DE CONEXIONES (Link Analysis) ---
st.subheader("🕸️ Análisis de Vínculos Financieros")

# Construcción del grafo con NetworkX
G = nx.DiGraph()
for _, row in df_tx_filtrado.iterrows():
    origen = str(row["Origen"])
    destino = str(row["Entidad_Receptora"])
    monto = f"${row['Monto']:,.2f}"
    
    G.add_node(origen, color="#00f3ff", title="Origen")
    G.add_node(destino, color="#ff003c", title="Destino")
    G.add_edge(origen, destino, label=monto, title=f"{row['Tipo']} - {monto}")

# Renderizar PyVis
net = Network(height="500px", width="100%", bgcolor="#09090b", font_color="white", directed=True)
net.from_nx(G)
net.repulsion(node_distance=150, central_gravity=0.2, spring_length=200, spring_strength=0.05, damping=0.09)

# Guardar y mostrar el HTML del grafo
try:
    net.save_graph("grafo.html")
    with open("grafo.html", "r", encoding="utf-8") as f:
        html_string = f.read()
    components.html(html_string, height=510)
except Exception as e:
    st.error(f"Error al generar el grafo: {e}")

st.markdown("---")

# --- TABLAS INTERACTIVAS Y BUSCADOR ---
col_A, col_B = st.columns([2, 1])

with col_A:
    st.subheader("Flujo de Transacciones")
    st.dataframe(df_tx_filtrado, use_container_width=True)

with col_B:
    st.subheader("Base de Nodos")
    if search_query:
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
