import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# Función para construir los controles de filtrado (dropdowns y selector de fechas)
def crear_controles(df_empresas, df_canales, df_agencias):
    """Devuelve una lista de componentes Dash (Dropdowns, DatePickerRange, etc.) para los filtros."""
    # Dropdown de Empresa
    dropdown_emp = {
        "id": "filter-empresa",
        "options": [{"label": nombre, "value": eid}
                    for eid, nombre in zip(df_empresas["ID_empresa"], df_empresas["Empresa_nombre"])],
         "multi": True,
        "placeholder": "Filtrar por empresa..."
    }
    # Dropdown de Canal
    dropdown_can = {
        "id": "filter-canal",
        "options": [{"label": nombre, "value": cid}
                    for cid, nombre in zip(df_canales["ID_canal"], df_canales["Canal_nombre"])],
         "multi": True,
        "placeholder": "Filtrar por canal..."
    }
    # Dropdown de Agencia
    dropdown_age = {
        "id": "filter-agencia",
        "options": [{"label": nombre, "value": aid}
                    for aid, nombre in zip(df_agencias["ID_Agencia"], df_agencias["Agencia_nombre"])],
         "multi": True,
        "placeholder": "Filtrar por agencia..."
    }
    # Selector de rango de fechas (DatePickerRange)
    date_picker = {
        "id": "filter-fechas",
        "start_date": None,
        "end_date": None,
        "display_format": "YYYY-MM-DD",  # formato de fecha
        "months_delimiter": " - "
    }
    # Selector de frecuencia (Diario/Semanal/Mensual)
    frecuencia_radio = {
        "id": "filter-freq",
        "options": [
            {"label": "Diario", "value": "D"},
            {"label": "Semanal", "value": "W"},
            {"label": "Mensual", "value": "M"}
        ],
        "value": "D",
        "inline": True
    }
    return dropdown_emp, dropdown_can, dropdown_age, date_picker, frecuencia_radio

# Funciones para construir gráficas Plotly a partir de las series calculadas
def grafica_linea(x, y, titulo="", eje_y="", formato_y=None):
    """Devuelve una figura de línea simple con Plotly Express."""
    # —————— Ajuste para manejar PeriodIndex (agregaciones mensuales) ——————
    # Si 'x' es un PeriodIndex, conviértelo a Timestamp (fecha de inicio del periodo).
    try:
        if isinstance(x, pd.PeriodIndex):
            x_plot = x.to_timestamp()
        else:
            x_plot = [v.to_timestamp() if hasattr(v, "to_timestamp") else v for v in x]

        # — Convertir la serie y a valores puros —
        if hasattr(y, "tolist"):
            y_plot = y.tolist()
        else:
            y_plot = list(y)
    except ImportError:
        x_plot = x

    fig = px.line(x=x_plot, y=y_plot, title=titulo)
    fig.update_traces(mode="lines+markers")  # línea con marcadores
    fig.update_layout(yaxis_title=eje_y, xaxis_title="Fecha")
    # Formato del eje Y (por ejemplo, porcentajes o moneda)
    if formato_y == "pct":
        fig.update_layout(yaxis_tickformat=".1f%")  # formato porcentaje
    elif formato_y == "money":
        fig.update_layout(yaxis_tickprefix="$")
    return fig

def grafica_indicador(valor, titulo="", sufijo=""):
    """Devuelve una figura tipo indicador (número grande) con go.Indicator."""
    fig = go.Figure(go.Indicator(
        mode="number",
        value=valor,
        title={"text": titulo},
        number={"suffix": sufijo}
    ))
    fig.update_layout(height=150)  # altura menor para encajar en dashboard
    return fig

def grafica_histograma(data, titulo="", xaxis_title=""):
    """Devuelve un histograma de la distribución de 'data'."""
    fig = px.histogram(data, nbins=20, title=titulo)
    fig.update_layout(xaxis_title=xaxis_title, yaxis_title="Cantidad de reservas")
    return fig

def grafica_boxplot(data, titulo="", yaxis_title=""):
    """Devuelve un diagrama de caja para la distribución de 'data'."""
    fig = px.box(data, title=titulo)
    fig.update_layout(yaxis_title=yaxis_title)
    return fig
