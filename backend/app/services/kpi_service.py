import pandas as pd
from typing import List, Dict


def kpi_reservas(parquet_path: str = "data/reservations_clean.parquet") -> List[Dict]:
    """
    Genera un KPI de reservas totales por hotel a partir del archivo Parquet.

    Args:
        parquet_path (str): Ruta al archivo .parquet de reservas.

    Returns:
        List[Dict]: Lista de diccionarios con claves 'hotel' y 'total_reservations'.
    """
    # Leer el DataFrame desde Parquet
    df = pd.read_parquet(parquet_path)

    # Agrupar por hotel y sumar las reservas
    grouped = df.groupby("hotel")["reservations"].sum().reset_index()

    # Renombrar columna para claridad
    grouped = grouped.rename(columns={"reservations": "total_reservations"})

    # Convertir a lista de diccionarios para serializar a JSON
    return grouped.to_dict(orient="records")