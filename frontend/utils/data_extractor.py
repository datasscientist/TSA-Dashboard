import pandas as pd
from datetime import datetime

# Ruta a la carpeta de datos CSV
DATA_PATH = "C:/Users/vhgar/source/repos/TSA-Dashboard/frontend/data/"

# Función para cargar los DataFrame necesarios desde CSV
def load_data():
    """Carga los datos de reservas y catálogos desde archivos CSV."""
    # Leer archivo principal de reservaciones
    reservaciones = pd.read_csv(DATA_PATH + "reservaciones_tcabdfront2.csv",low_memory=False, parse_dates=["h_res_fec_ok", "h_fec_lld_ok"])
    # Leer catálogos (estatus, agencias, empresas, canales)
    estatus = pd.read_csv(DATA_PATH + "iar_estatus_reservaciones.csv")
    estatus.rename(columns={
        'estatus_reservaciones': 'descripcion'
    }, inplace=True)
    agencias = pd.read_csv(DATA_PATH + "iar_Agencias.csv")
    empresas = pd.read_csv(DATA_PATH + "iar_empresas.csv")
    canales = pd.read_csv(DATA_PATH + "iar_canales.csv")
    # Retornar todos los DataFrames en un diccionario para fácil acceso
    return {
        "reservaciones": reservaciones,
        "estatus": estatus,
        "agencias": agencias,
        "empresas": empresas,
        "canales": canales
    }

# Función para preparar datos filtrados según los filtros seleccionados
def filtrar_datos(df, start_date=None, end_date=None, empresas_sel=None, canales_sel=None, agencias_sel=None):
    """
    Aplica filtros de fecha, empresa, canal y agencia al DataFrame de reservaciones.
    - start_date, end_date: rango de fechas de check-in (inclusive).
    - empresas_sel, canales_sel, agencias_sel: listas de IDs seleccionados (o None/[] para no filtrar).
    """
    df_filtrado = df.copy()
    # Filtrar por rango de fechas (fecha de check-in)
    if start_date:
        start_ts = pd.to_datetime(start_date)
        df_filtrado = df_filtrado[df_filtrado["h_fec_lld_ok"] >= start_ts]
    if end_date:
        end_ts = pd.to_datetime(end_date)
        df_filtrado = df_filtrado[df_filtrado["h_fec_lld_ok"] <= end_ts]
    # Filtrar por empresa(s)
    if empresas_sel:
        df_filtrado = df_filtrado[df_filtrado["ID_empresa"].isin(empresas_sel)]
    if canales_sel:
        df_filtrado = df_filtrado[df_filtrado["ID_canal"].isin(canales_sel)]
    if agencias_sel:
        df_filtrado = df_filtrado[df_filtrado["ID_Agencia"].isin(agencias_sel)]
    return df_filtrado

# Función para obtener los KPI agregados por período de tiempo
def calcular_kpis(df, freq="D", total_habs=100):
    """
    Calcula los KPI agregados según un intervalo de frecuencia temporal.
    - freq: "D" diario, "W" semanal, "M" mensual.
    - total_habs: número total de habitaciones disponibles (para cálculo de ocupación y RevPAR).
    Devuelve un diccionario con series (pandas Series o DataFrames) para cada métrica temporal y valores agregados.
    """
    # Asegurar que la fecha de check-in es datetime (por seguridad ya parseado en read_csv)
    df = df.copy()
    df["fecha_checkin"] = pd.to_datetime(df["h_fec_lld_ok"]).dt.date  # convertir a date (sin hora)
    df.sort_values("fecha_checkin", inplace=True)
    # Agrupar por periodo según freq
    if freq == "D":
        # Agrupación diaria por fecha
        grupo = df.groupby("fecha_checkin")
        # Determinar días en cada grupo (si no todos los días aparecen, contarlos igualmente)
        # Para diario, días_en_periodo = 1 siempre para grupos diarios.
    elif freq == "W":
        # Agrupar por semana (año-semana)
        df["week"] = pd.to_datetime(df["fecha_checkin"]).dt.isocalendar().week  # semana del año
        df["year"] = pd.to_datetime(df["fecha_checkin"]).dt.year
        grupo = df.groupby(["year", "week"])
    elif freq == "M":
        # Agrupar por mes (año-mes)
        df["month"] = pd.to_datetime(df["fecha_checkin"]).dt.to_period("M")
        grupo = df.groupby("month")
    else:
        grupo = df.groupby("fecha_checkin")  # default diario
    
    # Volumen de reservas: conteo de reservas por período
    volumen = grupo.size()  # Series con índice = periodo, valor = count
    # Noches habitación vendidas: suma de h_num_noc * h_tot_hab por período
    df["room_nights"] = df["h_num_noc"] * df["h_tot_hab"]
    room_nights = grupo["room_nights"].sum()
    # Ingreso total (suma de h_tfa_total) por período para calcular ADR
    ingreso_total = grupo["h_tfa_total"].sum()
    # ADR por período = ingreso total / room_nights (donde room_nights > 0)
    adr = ingreso_total / room_nights
    # Ocupación por período = (room_nights / (total_habs * días_en_periodo)) * 100
    ocupacion = None
    if freq == "D":
        ocupacion = (room_nights / total_habs) * 100  # cada grupo es 1 día
    elif freq == "W":
        ocupacion = (room_nights / (total_habs * 7)) * 100  # aproximamos 7 días por semana
    elif freq == "M":
        # obtener días en cada mes
        ocupacion = (room_nights / (total_habs * room_nights.index.to_series().apply(lambda p: p.days_in_month))) * 100
    # RevPAR por período = ADR * (ocupacion/100)  (ó ingreso total / total_habs)
    revpar = (adr * ocupacion/100)
    
    # KPI globales (en el rango filtrado completo, no por período)
    total_reservas = len(df)
    total_room_nights = df["room_nights"].sum()
    ocupacion_global = None
    if df["fecha_checkin"].nunique() > 0:
        # calcular ocupación global considerando el rango de fechas filtrado
        rango_dias = (df["fecha_checkin"].max() - df["fecha_checkin"].min()).days + 1
        ocupacion_global = (total_room_nights / (total_habs * rango_dias)) * 100
    else:
        ocupacion_global = 0.0
    adr_global = df["h_tfa_total"].sum() / total_room_nights if total_room_nights > 0 else 0
    revpar_global = adr_global * (ocupacion_global/100)
    avg_stay = df["h_num_noc"].mean() if total_reservas > 0 else 0
    
    # Cálculo de tasa de cancelación y no-show (% sobre total reservas filtradas)
    # Identificar estatus de cancelación y no-show en el DataFrame (se espera que ya esté mergeado con descripción estatus)
    cancelados = df[df["estatus_desc"].str.contains("Cancel", case=False)]  # contiene "Cancel"
    noshows = df[df["estatus_desc"].str.contains("no show", case=False, regex=False)]
    tasa_cancel = (len(cancelados) / total_reservas * 100) if total_reservas > 0 else 0
    tasa_noshow = (len(noshows) / total_reservas * 100) if total_reservas > 0 else 0
    
    return {
        "volumen": volumen,
        "room_nights": room_nights,
        "ocupacion": ocupacion,
        "adr": adr,
        "revpar": revpar,
        "global": {
            "total_reservas": total_reservas,
            "room_nights": total_room_nights,
            "ocupacion": ocupacion_global,
            "adr": adr_global,
            "revpar": revpar_global,
            "avg_stay": avg_stay,
            "tasa_cancel": tasa_cancel,
            "tasa_noshow": tasa_noshow
        }
    }
