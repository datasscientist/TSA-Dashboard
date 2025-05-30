from fastapi import APIRouter
from app.services import kpi_service  # funciones que procesan los parquet
from app.schemas.kpi import KPIResponse  # pydantic schema para la respuesta

router = APIRouter(prefix="/kpi")

@router.get("/reservas", response_model=KPIResponse)
def get_kpi_reservas():
    data = kpi_service.kpi_reservas()  # esta función lee parquet y procesa datos
    return {"kpi": "reservas_total", "values": data}
