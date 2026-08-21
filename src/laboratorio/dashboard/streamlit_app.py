import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px

# 1. Carga y Preparación de Datos
URL = "/workspaces/laboratorio/src/laboratorio/dashboard/spacex_launch_dash.csv"
spacex_df = pd.read_csv(URL)
max_payload = spacex_df["Payload Mass (kg)"].max()
min_payload = spacex_df["Payload Mass (kg)"].min()

# 2. Inicialización de la App (Tema CYBORG para Alto Contraste / Dark Mode)
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])
server = app.server


# 3. Componentes UI Reutilizables (Tarjetas KPI Dark Mode)
def create_kpi_card(title, id_value, color):
    return dbc.Card(
        [
            dbc.CardBody(
                [
                    html.H6(
                        title,
                        className="text-uppercase mb-2",
                        style={"color": "#b0bec5", "fontSize": "0.85rem"},
                    ),
                    html.H3(
                        id=id_value,
                        className="mb-0 font-weight-bold",
                        style={"color": color},
                    ),
                ]
            )
        ],
        style={
            "backgroundColor": "#1e1e1e",
            "borderLeft": f"5px solid {color}",
            "borderRadius": "5px",
        },
        className="shadow",
    )


# 4. Diseño del Dashboard (Layout)
app.layout = dbc.Container(
    [
        # Encabezado
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H2(
                            "🚀 SpaceX Falcon 9: Executive Dashboard",
                            className="font-weight-bold mt-4 mb-1 text-white",
                        ),
                        html.P(
                            "Análisis predictivo, métricas de éxito y auditoría de aterrizajes de la primera etapa",
                            style={"color": "#9e9e9e"},
                            className="mb-4",
                        ),
                    ],
                    width=12,
                )
            ]
        ),
        # Panel de Controles
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Card(
                            [
                                dbc.CardBody(
                                    [
                                        dbc.Row(
                                            [
                                                dbc.Col(
                                                    [
                                                        html.Label(
                                                            "📍 Seleccionar Base de Lanzamiento:",
                                                            className="font-weight-bold text-white",
                                                        ),
                                                        dcc.Dropdown(
                                                            id="site-dropdown",
                                                            options=[
                                                                {
                                                                    "label": "🌍 Todas las Bases",
                                                                    "value": "ALL",
                                                                }
                                                            ]
                                                            + [
                                                                {
                                                                    "label": site,
                                                                    "value": site,
                                                                }
                                                                for site in spacex_df[
                                                                    "Launch Site"
                                                                ].unique()
                                                            ],
                                                            value="ALL",
                                                            clearable=False,
                                                            style={
                                                                "color": "#000000"
                                                            },  # Texto negro en el dropdown para contraste
                                                        ),
                                                    ],
                                                    md=6,
                                                ),
                                                dbc.Col(
                                                    [
                                                        html.Label(
                                                            "⚖️ Rango de Carga (Payload en Kg):",
                                                            className="font-weight-bold text-white",
                                                        ),
                                                        dcc.RangeSlider(
                                                            id="payload-slider",
                                                            min=0,
                                                            max=10000,
                                                            step=1000,
                                                            marks={
                                                                i: {
                                                                    "label": f"{i}k",
                                                                    "style": {
                                                                        "color": "#b0bec5"
                                                                    },
                                                                }
                                                                for i in range(
                                                                    0, 10001, 2000
                                                                )
                                                            },
                                                            value=[
                                                                min_payload,
                                                                max_payload,
                                                            ],
                                                            tooltip={
                                                                "placement": "bottom",
                                                                "always_visible": True,
                                                            },
                                                        ),
                                                    ],
                                                    md=6,
                                                ),
                                            ]
                                        )
                                    ]
                                )
                            ],
                            style={"backgroundColor": "#2c2c2c", "border": "none"},
                            className="mb-4 shadow",
                        )
                    ],
                    width=12,
                )
            ]
        ),
        # Panel de KPIs
        dbc.Row(
            [
                dbc.Col(
                    create_kpi_card(
                        "Total Vuelos Analizados", "kpi-total-flights", "#00bcd4"
                    ),
                    md=4,
                    className="mb-4",
                ),
                dbc.Col(
                    create_kpi_card(
                        "Tasa de Éxito Global", "kpi-success-rate", "#00e676"
                    ),
                    md=4,
                    className="mb-4",
                ),
                dbc.Col(
                    create_kpi_card(
                        "Carga Promedio (Kg)", "kpi-avg-payload", "#ffca28"
                    ),
                    md=4,
                    className="mb-4",
                ),
            ]
        ),
        # Gráficos Principales
        dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        dcc.Graph(id="success-pie-chart"),
                        style={"backgroundColor": "#1e1e1e", "border": "none"},
                        className="mb-4",
                    ),
                    md=5,
                ),
                dbc.Col(
                    dbc.Card(
                        dcc.Graph(id="booster-bar-chart"),
                        style={"backgroundColor": "#1e1e1e", "border": "none"},
                        className="mb-4",
                    ),
                    md=7,
                ),
            ]
        ),
        # Gráfico de Dispersión
        dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        dcc.Graph(id="success-payload-scatter-chart"),
                        style={"backgroundColor": "#1e1e1e", "border": "none"},
                        className="mb-4",
                    ),
                    width=12,
                )
            ]
        ),
        # Folium
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H4(
                            "🗺️ Mapa Geoespacial de Bases",
                            className="text-white mt-4 mb-3",
                        ),
                        html.Iframe(
                            src="/assets/mapa_spacex.html",  # Llama al mapa que creamos con Folium
                            style={
                                "width": "100%",
                                "height": "500px",
                                "border": "none",
                                "borderRadius": "5px",
                            },
                        ),
                    ],
                    width=12,
                )
            ]
        ),
        # NUEVO: Tabla de Datos Interactiva para auditoría
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H4(
                            "📊 Registro Detallado de Vuelos (Auditoría)",
                            className="text-white mt-2 mb-3",
                        ),
                        dash_table.DataTable(
                            id="flights-data-table",
                            columns=[
                                {"name": "Vuelo Nº", "id": "Flight Number"},
                                {"name": "Base de Lanzamiento", "id": "Launch Site"},
                                {
                                    "name": "Versión del Cohete",
                                    "id": "Booster Version Category",
                                },
                                {
                                    "name": "Carga (Kg)",
                                    "id": "Payload Mass (kg)",
                                    "type": "numeric",
                                    "format": {"specifier": ",.0f"},
                                },
                                {"name": "Resultado", "id": "class_label"},
                            ],
                            page_size=10,
                            sort_action="native",
                            style_table={"overflowX": "auto"},
                            # Diseño de cabecera más plano y elegante
                            style_header={
                                "backgroundColor": "#2b2b2b",
                                "color": "#e0e0e0",  # Blanco roto, menos agresivo que el blanco puro
                                "fontWeight": "normal",  # Quitamos la negrita para un look más limpio
                                "border": "1px solid #333333",
                            },
                            # Datos base en gris suave
                            style_data={
                                "backgroundColor": "#1e1e1e",
                                "color": "#cccccc",
                                "border": "1px solid #333333",
                            },
                            # Formato condicional con paleta FLAT / PASTEL
                            style_data_conditional=[
                                {
                                    # Verde pastel desaturado para los éxitos
                                    "if": {"filter_query": '{class_label} = "Éxito"'},
                                    "backgroundColor": "#233329",  # Fondo verde-grisáceo muy oscuro y sutil
                                    "color": "#a5d6a7",  # Texto verde pastel
                                },
                                {
                                    # Rojo pastel desaturado para los fracasos
                                    "if": {"filter_query": '{class_label} = "Fracaso"'},
                                    "backgroundColor": "#332323",  # Fondo rojo-grisáceo muy oscuro y sutil
                                    "color": "#ef9a9a",  # Texto rojo pastel
                                },
                            ],
                        ),
                    ],
                    width=12,
                    className="mb-5",
                )
            ]
        ),
    ],
    fluid=True,
    className="p-4",
    style={"backgroundColor": "#000000"},
)


# 5. Lógica del Servidor (Callbacks)
@app.callback(
    [
        Output("kpi-total-flights", "children"),
        Output("kpi-success-rate", "children"),
        Output("kpi-avg-payload", "children"),
        Output("success-pie-chart", "figure"),
        Output("booster-bar-chart", "figure"),
        Output("success-payload-scatter-chart", "figure"),
        Output("flights-data-table", "data"),
    ],  # Salida para la tabla
    [Input("site-dropdown", "value"), Input("payload-slider", "value")],
)
def update_dashboard(entered_site, payload_range):
    low, high = payload_range
    mask = (spacex_df["Payload Mass (kg)"] >= low) & (
        spacex_df["Payload Mass (kg)"] <= high
    )
    filtered_df = spacex_df[mask].copy()

    if entered_site != "ALL":
        filtered_df = filtered_df[filtered_df["Launch Site"] == entered_site]

    # --- 1. Cálculos de KPIs ---
    total_flights = len(filtered_df)
    success_rate = (filtered_df["class"].mean() * 100) if total_flights > 0 else 0
    avg_payload = filtered_df["Payload Mass (kg)"].mean() if total_flights > 0 else 0

    kpi_flights_text = f"{total_flights}"
    kpi_success_text = f"{success_rate:.1f}%"
    kpi_payload_text = f"{avg_payload:,.0f} Kg"

    color_success = "#00e676"  # Verde Neón
    color_fail = "#ff5252"  # Rojo Carmesí

    # --- 2. Gráfico de Pastel ---
    if entered_site == "ALL":
        pie_fig = px.pie(
            filtered_df,
            values="class",
            names="Launch Site",
            title="Aportación al Éxito por Base",
            hole=0.4,
            color_discrete_sequence=px.colors.diverging.Tealrose,
        )
    else:
        counts = filtered_df["class"].value_counts().reset_index()
        counts.columns = ["class", "count"]
        counts["Resultado"] = counts["class"].map({1: "Éxito", 0: "Fracaso"})
        pie_fig = px.pie(
            counts,
            values="count",
            names="Resultado",
            title=f"Tasa de Aterrizaje en {entered_site}",
            hole=0.4,
            color="Resultado",
            color_discrete_map={"Éxito": color_success, "Fracaso": color_fail},
        )
    pie_fig.update_layout(
        template="plotly_dark",
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(t=50, b=20, l=20, r=20),
    )

    # --- 3. Gráfico de Barras ---
    booster_success = (
        filtered_df.groupby("Booster Version Category")["class"]
        .agg(["mean"])
        .reset_index()
    )
    booster_success["mean"] = booster_success["mean"] * 100
    bar_fig = px.bar(
        booster_success,
        x="Booster Version Category",
        y="mean",
        text=booster_success["mean"].apply(lambda x: f"{x:.1f}%"),
        title="Tasa de Éxito por Versión del Cohete",
        labels={"mean": "Tasa de Éxito (%)", "Booster Version Category": "Versión"},
        color="mean",
        color_continuous_scale="Greens",
    )
    bar_fig.update_traces(textposition="outside")
    bar_fig.update_layout(
        template="plotly_dark",
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        coloraxis_showscale=False,
        yaxis_range=[0, 115],
        margin=dict(t=50, b=20, l=20, r=20),
    )

    # --- 4. Gráfico de Dispersión ---
    scatter_title = "Distribución: Peso de Carga vs. Resultado" + (
        " (Todas las Bases)" if entered_site == "ALL" else f" ({entered_site})"
    )
    scatter_fig = px.scatter(
        filtered_df,
        x="Payload Mass (kg)",
        y="class",
        color="Booster Version Category",
        size_max=12,
        hover_data=["Flight Number"],
        title=scatter_title,
        opacity=0.9,
    )
    scatter_fig.update_traces(marker=dict(size=12, line=dict(width=1, color="White")))
    scatter_fig.update_yaxes(tickvals=[0, 1], ticktext=["Fracaso (0)", "Éxito (1)"])
    scatter_fig.update_layout(
        template="plotly_dark",
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(t=50, b=20, l=20, r=20),
    )

    # --- 5. Preparar Datos para la Tabla ---
    filtered_df["class_label"] = filtered_df["class"].map({1: "Éxito", 0: "Fracaso"})
    # Ordenamos por número de vuelo para que la tabla tenga sentido temporal
    table_data = filtered_df.sort_values(by="Flight Number").to_dict("records")

    return (
        kpi_flights_text,
        kpi_success_text,
        kpi_payload_text,
        pie_fig,
        bar_fig,
        scatter_fig,
        table_data,
    )


# 6. Arranque de la Aplicación
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8050, debug=False)
