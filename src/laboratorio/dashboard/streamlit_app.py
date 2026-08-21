import streamlit as st
import pandas as pd
import plotly.express as px
import streamlit.components.v1 as components
import os

# 1. Configuración de la página (Dark Mode por defecto)
st.set_page_config(
    page_title="SpaceX Executive Dashboard",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Carga y Preparación de Datos (Usamos caché para que sea ultra rápido)
@st.cache_data
def load_data():
    URL = "spacex_launch_dash.csv"
    return pd.read_csv(URL)

try:
    spacex_df = load_data()
    max_payload = int(spacex_df["Payload Mass (kg)"].max())
    min_payload = int(spacex_df["Payload Mass (kg)"].min())
except FileNotFoundError:
    st.error("⚠️ Archivo no encontrado. Asegúrate de subir 'spacex_launch_dash.csv' a GitHub.")
    st.stop()

# 3. Encabezado
st.title("🚀 SpaceX Falcon 9: Executive Dashboard")
st.markdown("Análisis predictivo, métricas de éxito y auditoría de aterrizajes de la primera etapa")
st.markdown("---")

# 4. Panel de Controles
col1, col2 = st.columns(2)

with col1:
    # Creamos la lista de opciones para el Dropdown
    sites = ["ALL"] + list(spacex_df["Launch Site"].unique())
    entered_site = st.selectbox("📍 Seleccionar Base de Lanzamiento:", sites)

with col2:
    # Slider de rango
    payload_range = st.slider(
        "⚖️ Rango de Carga (Payload en Kg):",
        min_value=0,
        max_value=10000,
        value=(min_payload, max_payload),
        step=1000
    )

# 5. Lógica de Filtrado (Reemplaza a los callbacks)
low, high = payload_range
mask = (spacex_df["Payload Mass (kg)"] >= low) & (spacex_df["Payload Mass (kg)"] <= high)
filtered_df = spacex_df[mask].copy()

if entered_site != "ALL":
    filtered_df = filtered_df[filtered_df["Launch Site"] == entered_site]

# 6. Cálculos de KPIs
total_flights = len(filtered_df)
success_rate = (filtered_df["class"].mean() * 100) if total_flights > 0 else 0
avg_payload = filtered_df["Payload Mass (kg)"].mean() if total_flights > 0 else 0

# 7. Mostrar KPIs usando las métricas nativas de Streamlit
kpi1, kpi2, kpi3 = st.columns(3)
kpi1.metric(label="Total Vuelos Analizados", value=f"{total_flights}")
kpi2.metric(label="Tasa de Éxito Global", value=f"{success_rate:.1f}%")
kpi3.metric(label="Carga Promedio (Kg)", value=f"{avg_payload:,.0f} Kg")

st.markdown("---")

# 8. Generación de Gráficos
color_success = "#00e676"  # Verde Neón
color_fail = "#ff5252"     # Rojo Carmesí

# Gráfico de Pastel
if entered_site == "ALL":
    pie_fig = px.pie(
        filtered_df, values="class", names="Launch Site",
        title="Aportación al Éxito por Base", hole=0.4,
        color_discrete_sequence=px.colors.diverging.Tealrose
    )
else:
    counts = filtered_df["class"].value_counts().reset_index()
    counts.columns = ["class", "count"]
    counts["Resultado"] = counts["class"].map({1: "Éxito", 0: "Fracaso"})
    pie_fig = px.pie(
        counts, values="count", names="Resultado",
        title=f"Tasa de Aterrizaje en {entered_site}", hole=0.4,
        color="Resultado", color_discrete_map={"Éxito": color_success, "Fracaso": color_fail}
    )
pie_fig.update_layout(template="plotly_dark", plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", margin=dict(t=50, b=20, l=20, r=20))

# Gráfico de Barras
booster_success = filtered_df.groupby("Booster Version Category")["class"].agg(["mean"]).reset_index()
booster_success["mean"] = booster_success["mean"] * 100
bar_fig = px.bar(
    booster_success, x="Booster Version Category", y="mean",
    text=booster_success["mean"].apply(lambda x: f"{x:.1f}%"),
    title="Tasa de Éxito por Versión del Cohete",
    labels={"mean": "Tasa de Éxito (%)", "Booster Version Category": "Versión"},
    color="mean", color_continuous_scale="Greens"
)
bar_fig.update_traces(textposition="outside")
bar_fig.update_layout(template="plotly_dark", plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", coloraxis_showscale=False, yaxis_range=[0, 115], margin=dict(t=50, b=20, l=20, r=20))

# Mostramos Pastel y Barras en dos columnas
chart_col1, chart_col2 = st.columns([5, 7])
with chart_col1:
    st.plotly_chart(pie_fig, use_container_width=True)
with chart_col2:
    st.plotly_chart(bar_fig, use_container_width=True)

# Gráfico de Dispersión
scatter_title = f"Distribución: Peso de Carga vs. Resultado ({'Todas las Bases' if entered_site == 'ALL' else entered_site})"
scatter_fig = px.scatter(
    filtered_df, x="Payload Mass (kg)", y="class", color="Booster Version Category",
    size_max=12, hover_data=["Flight Number"], title=scatter_title, opacity=0.9
)
scatter_fig.update_traces(marker=dict(size=12, line=dict(width=1, color="White")))
scatter_fig.update_yaxes(tickvals=[0, 1], ticktext=["Fracaso (0)", "Éxito (1)"])
scatter_fig.update_layout(template="plotly_dark", plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", margin=dict(t=50, b=20, l=20, r=20))

st.plotly_chart(scatter_fig, use_container_width=True)

# 9. Mapa de Folium
st.markdown("### 🗺️ Mapa Geoespacial de Bases")
map_path = "assets/mapa_spacex.html"
if os.path.exists(map_path):
    with open(map_path, "r", encoding="utf-8") as f:
        html_data = f.read()
        # Incrustamos el HTML del mapa directamente
        components.html(html_data, height=500)
else:
    st.warning(f"⚠️ No se encontró el mapa en la ruta `{map_path}`. Recuerda subir la carpeta 'assets' con el archivo.")

# 10. Tabla de Auditoría
st.markdown("### 📊 Registro Detallado de Vuelos (Auditoría)")
filtered_df["class_label"] = filtered_df["class"].map({1: "Éxito", 0: "Fracaso"})

# Preparamos los datos para mostrar
display_df = filtered_df[["Flight Number", "Launch Site", "Booster Version Category", "Payload Mass (kg)", "class_label"]].sort_values(by="Flight Number")
display_df = display_df.rename(columns={
    "Flight Number": "Vuelo Nº",
    "Launch Site": "Base de Lanzamiento",
    "Booster Version Category": "Versión del Cohete",
    "Payload Mass (kg)": "Carga (Kg)",
    "class_label": "Resultado"
})

# Formato condicional de la tabla simulando tu estilo de Dash
def highlight_results(val):
    if val == "Éxito":
        return 'color: #a5d6a7; background-color: #233329'
    elif val == "Fracaso":
        return 'color: #ef9a9a; background-color: #332323'
    return ''

styled_df = display_df.style.map(highlight_results, subset=["Resultado"])
st.dataframe(styled_df, use_container_width=True, hide_index=True)