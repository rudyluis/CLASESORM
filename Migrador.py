# migrator.py

from sqlalchemy import create_engine, MetaData, text
from sqlalchemy.exc import ProgrammingError
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker
import ORM_1  # Tu módulo donde defines Base = declarative_base() y los modelos

def create_database(admin_url: str, dbname: str) -> None:
    """
    Conecta al servidor (a la base 'postgres' u otra de sistema)
    y lanza CREATE DATABASE si no existe.
    """
    engine = create_engine(admin_url)
    with engine.connect() as conn:
        try:
            conn.execution_options(isolation_level="AUTOCOMMIT") \
                .execute(text(f"CREATE DATABASE {dbname}"))
            print(f"✅ Base de datos '{dbname}' creada.")
        except ProgrammingError:
            print(f"⚠️ Base de datos '{dbname}' ya existe o error.")
    engine.dispose()


def get_engine(db_url: str) -> Engine:
    """Crea un Engine de SQLAlchemy a partir de una URL."""
    return create_engine(db_url)


def create_schema(engine: Engine) -> None:
    """
    Crea todas las tablas definidas en Base.metadata
    en la base apuntada por 'engine'.
    """
    ORM_1.Base.metadata.create_all(engine)
    ##Base.metadata.create_all(engine)
    print("✅ Esquema (tablas) creado en destino.")


def migrate_data(src_url: str, dst_url: str, batch_size: int = None) -> None:
    """
    Copia todo el contenido de cada tabla de src_url → dst_url,
    respetando el orden de dependencias de claves foráneas.
    """
    engine_src = get_engine(src_url)
    engine_dst = get_engine(dst_url)

    # Reflejar esquema de la BD origen
    meta_src = MetaData()
    meta_src.reflect(bind=engine_src)

    # Asegurarnos de que el esquema destino existe
    create_schema(engine_dst)

    with engine_src.connect() as conn_src, engine_dst.begin() as conn_dst:  # OJO: usamos .begin()
        for table in ORM_1.Base.metadata.sorted_tables:
            src_table = meta_src.tables.get(table.name)
            if src_table is None:
                print(f"⚠️ Tabla '{table.name}' no existe en origen, se omite.")
                continue

            sel = src_table.select()

            if batch_size:
                offset = 0
                while True:
                    chunk = conn_src.execute(sel.limit(batch_size).offset(offset)).mappings().all()
                    if not chunk:
                        break
                    # Insertamos en destino
                    conn_dst.execute(table.insert(), chunk)
                    print(f"[{table.name}] Migrados {len(chunk)} registros (offset {offset}).")
                    offset += batch_size
            else:
                rows = conn_src.execute(sel).mappings().all()
                if rows:
                    conn_dst.execute(table.insert(), rows)
                    print(f"[{table.name}] Migrados {len(rows)} registros.")
                else:
                    print(f"[{table.name}] — sin datos.")

    print("✅ Migración de datos completada.")

if __name__ == "__main__":
    # 1) Crear la BD destino si no existe
    ADMIN_URL = "postgresql+psycopg2://postgres:123456@localhost:5432/postgres"
    TARGET_DB  = "jardineria_bkp2025_y"
    create_database(ADMIN_URL, TARGET_DB)

    # 2) URL de origen (tu BD actual) y destino
    SRC_URL = "postgresql+psycopg2://postgres:123456@localhost:5432/jardineria_clases"
    DST_URL = f"postgresql+psycopg2://postgres:123456@localhost:5432/{TARGET_DB}"

    # 3) Ejecutar migración
    migrate_data(SRC_URL, DST_URL, batch_size=1000)
