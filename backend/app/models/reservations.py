# app/models/reservations.py
from sqlalchemy import Column, Integer, DateTime, String
from db.base import Base

class ReservationClean(Base):
    __tablename__ = "reservations_clean"

    id_reserva = Column("ID_Reserva", Integer, primary_key=True)
    fecha_hoy = Column("Fecha_hoy", DateTime, nullable=True)
    h_res_fec = Column("h_res_fec", DateTime, nullable=False)
    h_num_per = Column("h_num_per", Integer, nullable=False)
    h_num_adu = Column("h_num_adu", Integer, nullable=False)
    h_num_men = Column("h_num_men", Integer, nullable=False)
    h_num_noc = Column("h_num_noc", Integer, nullable=False)
    h_tot_hab = Column("h_tot_hab", Integer, nullable=False)
    id_programa = Column("ID_Programa", Integer, nullable=False)
    id_paquete = Column("ID_Paquete", Integer, nullable=False)
    id_segmento_comp = Column("ID_Segmento_Comp", Integer, nullable=False)
    id_agencia = Column("ID_Agencia", Integer, nullable=False)
    id_empresa = Column("ID_empresa", Integer, nullable=False)
    id_tipo_habitacion = Column("ID_Tipo_Habitacion", Integer, nullable=False)
    id_canal = Column("ID_canal", Integer, nullable=False)
    id_pais_origen = Column("ID_Pais_Origen", Integer, nullable=False)
    id_estatus_reservaciones = Column("ID_estatus_reservaciones", Integer, nullable=False)
    h_fec_lld = Column("h_fec_lld", DateTime, nullable=True)
    h_fec_reg = Column("h_fec_reg", DateTime, nullable=True)
    h_fec_sda = Column("h_fec_sda", DateTime, nullable=True)
    canal_nombre = Column("Canal_nombre", String, nullable=False)
    empresa_nombre = Column("Empresa_nombre", String, nullable=False)
    habitaciones_tot = Column("Habitaciones_tot", Integer, nullable=False)
    agencia_nombre = Column("Agencia_nombre", String, nullable=False)
    ciudad_nombre = Column("Ciudad_Nombre", String, nullable=False)
    estatus_reservaciones = Column("estatus_reservaciones", String, nullable=False)
    ciudad_normalizada = Column("Ciudad_Normalizada", String, nullable=False)
