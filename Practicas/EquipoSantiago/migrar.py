from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import ORM

engine = create_engine('postgresql+psycopg2://postgres:123456@localhost:5432/reserva_vuelos_bkp2025')

ORM.Base.metadata.create_all(engine)