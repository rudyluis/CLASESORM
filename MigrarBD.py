from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import ORM

engine = create_engine('postgresql://postgres:123456@localhost:5432/jardineria_bkp2025')

ORM.Base.metadata.create_all(engine)

print("Base de datos creada con éxito")