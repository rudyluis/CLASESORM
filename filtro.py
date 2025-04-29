from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, ForeignKey, Date, Numeric, Text, Sequence
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.orm  import sessionmaker, Session
from sqlalchemy.inspection import inspect
from ORM_1 import *



engine = create_engine('postgresql://postgres:123456@localhost:5432/jardineria')
Session = sessionmaker(bind=engine)
session = Session()

def consultar_tabla(session, modelo, filtros=None, solo_uno=False):
    """
    Consulta una tabla cualquiera definida con SQLAlchemy.

    :param session: sesión activa de SQLAlchemy.
    :param modelo: clase (modelo) de SQLAlchemy a consultar, e.g. Oficina, Empleado, etc.
    :param filtros: dict con pares clave=valor para filter_by (opcional).
    :param solo_uno: si True, devuelve/imprime solo el primer resultado (optional).
    :return: lista de instancias del modelo (o una sola instancia si solo_uno=True).
    """
    # Construir la consulta base
    q = session.query(modelo)
    
    # Aplicar filtros si los hay
    if filtros:
        q = q.filter_by(**filtros)
    
    # Ejecutar
    resultados = q.first() if solo_uno else q.all()
    
    # Función auxiliar para imprimir un objeto cualquiera
    def _print_obj(obj):
        mapper = inspect(obj.__class__)
        for col in mapper.columns:
            valor = getattr(obj, col.key)
            print(f"{col.key} = {valor}")
        print("-" * 40)
    
    # Imprimir y devolver
    if solo_uno:
        if resultados:
            _print_obj(resultados)
        else:
            print("No se encontró ningún registro.")
        return resultados
    else:
        if not resultados:
            print("No se encontraron registros.")
            return []
        for fila in resultados:
            _print_obj(fila)
        return resultados

# 1) Obtener todas las oficinas:
consultar_tabla(session, Oficina)

# 2) Obtener el empleado con id 5:
consultar_tabla(session, Empleado, filtros={"idempleado": 5}, solo_uno=True)

# 3) Filtrar productos de una gama concreta:
consultar_tabla(session, Producto, filtros={"idgamaproducto": 2})