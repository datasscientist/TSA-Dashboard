import dash_bootstrap_components as dbc
from dash import Dash, dcc, html, Input, Output, callback
import pandas as pd
import utils.data_extractor as de  # importar nuestro módulo utils.py
import components.filters as filters  # importar nuestro módulo components.py
import plotly.express as px
import datetime as dt

# Cargar datos al iniciar la aplicación
data = de.load_data()
df_reservas = data["reservaciones"]
df_estatus = data["estatus"]
df_agencias = data["agencias"]
df_empresas = data["empresas"]
df_canales = data["canales"]

# Unir descripción de estatus al dataframe principal de reservas
df_reservas = df_reservas.merge(
    df_estatus[['ID_estatus_reservaciones', 'descripcion']],
    on="ID_estatus_reservaciones",
    how="left"
).rename(columns={"descripcion": "estatus_desc"})

# Inicializar la aplicación Dash
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "Dashboard KPI Hoteleros"

# Para el RangeSlider de fechas necesitamos los min/max como enteros
start_year = dt.datetime(2019, 1, 1)
end_year   = dt.datetime(2021, 12, 31)
min_ts = int(start_year.timestamp())
max_ts = int(end_year.timestamp())

# Generar marcas mensuales legibles
all_months = pd.date_range(start_year, end_year, freq="MS")
marks = {
    int(dt.datetime(ts.year, ts.month, 1).timestamp()): ts.strftime("%Y-%m-01")
    for ts in all_months
}

# Definir el layout de la aplicación
app.layout = html.Div([
    html.H1("Dashboard de Reservas Hoteleras", style={"textAlign": "center"}),
    html.Div([
        # FECHA
        html.Div([
            html.Label("Fecha (rango)"),
            dcc.RangeSlider(
                id='filter-fechas-slider',
                min=min_ts,
                max=max_ts,
                step=86400 * 7,      # mueve en semanas
                value=[min_ts, max_ts],
                marks=marks,
                allowCross=False,
                tooltip={
                    "placement": "bottom",
                    "always_visible": False
                }
            ),
            html.Div(id='output-fecha', style={'marginTop': '5px', 'fontWeight': 'bold'})
        ], style={"flex": "2", "padding": "0 10px"}),

        # EMPRESA
        html.Div([
            html.Label("Empresa"),
            dcc.Dropdown(
                id="filter-empresa",
                options=[{"label": n, "value": i}
                         for i, n in zip(df_empresas["ID_empresa"], df_empresas["Empresa_nombre"])],
                multi=True,
                placeholder="Filtrar por empresa..."
            )
        ], style={"flex": "1", "padding": "0 10px"}),

        # CANAL
        html.Div([
            html.Label("Canal"),
            dcc.Dropdown(
                id="filter-canal",
                options=[{"label": n, "value": i}
                         for i, n in zip(df_canales["ID_canal"], df_canales["Canal_nombre"])],
                multi=True,
                placeholder="Filtrar por canal..."
            )
        ], style={"flex": "1", "padding": "0 10px"}),

        # AGENCIA
        html.Div([
            html.Label("Agencia"),
            dcc.Dropdown(
                id="filter-agencia",
                options=[{"label": n, "value": i}
                         for i, n in zip(df_agencias["ID_Agencia"], df_agencias["Agencia_nombre"])],
                multi=True,
                placeholder="Filtrar por agencia..."
            )
        ], style={"flex": "1", "padding": "0 10px"}),

        # FRECUENCIA
        html.Div([
            html.Label("Frecuencia"),
            dcc.RadioItems(
                id="filter-freq",
                options=[
                    {"label": "Diario", "value": "D"},
                    {"label": "Semanal", "value": "W"},
                    {"label": "Mensual", "value": "M"}
                ],
                value="D",
                inline=True
            )
        ], style={"flex": "1", "padding": "0 10px"})
    ], style={
        "display": "flex",
        "alignItems": "flex-end",
        "marginBottom": "20px"
    }),

    # Indicadores globales
    html.Div(className="indicadores", children=[
        dcc.Graph(id="indicador-adr"),
        dcc.Graph(id="indicador-revpar"),
        dcc.Graph(id="indicador-ocupacion"),
        dcc.Graph(id="indicador-estancia")
    ], style={"display": "flex", "justifyContent": "space-around"}),

    # Gráficas de series temporales
    dcc.Graph(id="grafico-volumen"),
    dcc.Graph(id="grafico-roomnights"),
    dcc.Graph(id="grafico-ocupacion"),
    dcc.Graph(id="grafico-revpar"),

    # Distribuciones
    dcc.Graph(id="grafico-leadtime"),
    dcc.Graph(id="grafico-estancia"),
    dcc.Graph(id="grafico-cancel")
])

# Definir el callback para actualizar las gráficas y el texto de fecha
@app.callback(
    Output("grafico-volumen", "figure"),
    Output("grafico-roomnights", "figure"),
    Output("grafico-ocupacion", "figure"),
    Output("grafico-revpar", "figure"),
    Output("grafico-leadtime", "figure"),
    Output("grafico-estancia", "figure"),
    Output("grafico-cancel", "figure"),
    Output("indicador-adr", "figure"),
    Output("indicador-revpar", "figure"),
    Output("indicador-ocupacion", "figure"),
    Output("indicador-estancia", "figure"),
    Output("output-fecha", "children"),
    Input("filter-fechas-slider", "value"),
    Input("filter-empresa", "value"),
    Input("filter-canal", "value"),
    Input("filter-agencia", "value"),
    Input("filter-freq", "value")
)
def actualizar_dashboard(fecha_slider, empresas, canales, agencias, freq):
    # Convertir timestamps a date
    start_date = dt.datetime.fromtimestamp(fecha_slider[0]).date()
    end_date   = dt.datetime.fromtimestamp(fecha_slider[1]).date()
    # Aplicar filtros
    empresas_sel = empresas if empresas else None
    canales_sel  = canales  if canales  else None
    agencias_sel = agencias if agencias else None
    df_filtrado  = de.filtrar_datos(df_reservas, start_date, end_date,
                                    empresas_sel, canales_sel, agencias_sel)
    # Calcular KPI
    kpis = de.calcular_kpis(df_filtrado, freq, total_habs=100)

    # Figuras temporales
    fig_vol = filters.grafica_linea(
        x=kpis["volumen"].index, y=kpis["volumen"],
        titulo="Volumen de Reservas", eje_y="Reservas"
    )
    fig_rn = filters.grafica_linea(
        x=kpis["room_nights"].index, y=kpis["room_nights"],
        titulo="Noches de Habitación Vendidas", eje_y="Room Nights"
    )
    fig_occ = filters.grafica_linea(
        x=kpis["ocupacion"].index, y=kpis["ocupacion"],
        titulo="Tasa de Ocupación", eje_y="Porcentaje", formato_y="pct"
    )
    fig_rp = filters.grafica_linea(
        x=kpis["revpar"].index, y=kpis["revpar"],
        titulo="RevPAR", eje_y="RevPAR", formato_y="money"
    )

    # Distribuciones
    if not df_filtrado.empty:
        lead_times = (df_filtrado["h_fec_lld_ok"] -
                      df_filtrado["h_res_fec_ok"]).dt.days
    else:
        lead_times = []
    fig_lead  = filters.grafica_histograma(
        lead_times, titulo="Anticipación de Reserva",
        xaxis_title="Días de anticipación"
    )
    fig_stay  = filters.grafica_boxplot(
        df_filtrado["h_num_noc"] if not df_filtrado.empty else [],
        titulo="Duración de Estancia",
        yaxis_title="Noches por reserva"
    )
    tasas = {"Cancelación": kpis["global"]["tasa_cancel"],
             "No Show":     kpis["global"]["tasa_noshow"]}
    fig_cancel = px.bar(
        x=list(tasas.keys()), y=list(tasas.values()),
        labels={"x": "", "y": "% de reservas"},
        title="Tasa de Cancelación y No-Show"
    )
    fig_cancel.update_layout(yaxis_range=[0,100])
    fig_cancel.update_traces(marker_color=["#d62728", "#9467bd"])

    # Indicadores
    fig_ind_adr      = filters.grafica_indicador(
        kpis["global"]["adr"],      titulo="ADR"
    )
    fig_ind_revpar   = filters.grafica_indicador(
        kpis["global"]["revpar"],   titulo="RevPAR"
    )
    fig_ind_ocup     = filters.grafica_indicador(
        kpis["global"]["ocupacion"], titulo="Ocupación", sufijo="%"
    )
    fig_ind_estancia = filters.grafica_indicador(
        kpis["global"]["avg_stay"],  titulo="Estancia Prom.", sufijo=" noches"
    )

    # Texto del rango de fechas
    rango_texto = f"{start_date.strftime('%Y-%m-%d')}  ⇄  {end_date.strftime('%Y-%m-%d')}"

    return (
        fig_vol, fig_rn, fig_occ, fig_rp,
        fig_lead, fig_stay, fig_cancel,
        fig_ind_adr, fig_ind_revpar, fig_ind_ocup, fig_ind_estancia,
        rango_texto
    )

# Ejecutar la aplicación en modo debug
if __name__ == "__main__":
    app.run(debug=True)
