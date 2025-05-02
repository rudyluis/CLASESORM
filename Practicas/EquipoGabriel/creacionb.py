# INTEGRANTES:
# RENATA ANEYBA, GABRIEL VARGAS, JOAQUIN LARA
# 
from sqlalchemy import create_engine, text
from sqlalchemy.exc import ProgrammingError, OperationalError

# Conexión a la base 'postgres', que siempre existe
engine = create_engine('postgresql+psycopg2://postgres:123456@localhost:5432/postgres')

conn = engine.connect()
dbname = "gimnasio"  # mejor usar minúsculas por convención en PostgreSQL

try:
    # Autocommit es necesario para CREATE DATABASE
    conn.execution_options(isolation_level="AUTOCOMMIT").execute(
        text(f'CREATE DATABASE "{dbname}"')  # usa comillas dobles por si hay mayúsculas
    )
    print(f"Base de datos '{dbname}' creada con éxito.")
except (ProgrammingError, OperationalError) as e:
    print(f"No se pudo crear la base de datos '{dbname}': {e}")
finally:
    conn.close()