#Santiago Rojas, Dayra Monegro, Mirko Coca
from sqlalchemy import create_engine, MetaData, text
from sqlalchemy.exc import ProgrammingError
from sqlalchemy.engine import Engine
import ORM 

def create_database(admin_url: str, dbname: str) -> None:
    """Crea la base de datos si no existe."""
    engine = create_engine(admin_url)
    with engine.connect() as conn:
        try:
            conn.execution_options(isolation_level="AUTOCOMMIT") \
                .execute(text(f"CREATE DATABASE {dbname}"))
            print(f"✅ Base de datos '{dbname}' creada.")
        except ProgrammingError:
            print(f"⚠️ Base de datos '{dbname}' ya existe o no se pudo crear.")
    engine.dispose()


def get_engine(db_url: str) -> Engine:
    """Devuelve un engine SQLAlchemy desde una URL."""
    return create_engine(db_url)


def create_schema(engine: Engine) -> None:
    """Crea el esquema (tablas) en la base de datos destino."""
    ORM.Base.metadata.create_all(engine)
    print("✅ Esquema (tablas) creado en la base de datos destino.")


def migrate_data(src_url: str, dst_url: str, batch_size: int = None) -> None:
    """Copia todos los datos de la base de datos origen a la destino."""
    engine_src = get_engine(src_url)
    engine_dst = get_engine(dst_url)

    # Reflejar el esquema de la BD origen
    meta_src = MetaData()
    meta_src.reflect(bind=engine_src)

    # Crear las tablas destino si no existen
    create_schema(engine_dst)

    with engine_src.connect() as conn_src, engine_dst.begin() as conn_dst:
        for table in ORM.Base.metadata.sorted_tables:
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
    # 1) Crear la base de datos destino
    ADMIN_URL = "postgresql+psycopg2://postgres:123456@localhost:5432/postgres"
    TARGET_DB = "reserva_vuelos_bkp2025"
    create_database(ADMIN_URL, TARGET_DB)
