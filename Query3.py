from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, ForeignKey, Date, Numeric, Text, Sequence
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.orm  import sessionmaker, Session
from ORM_1 import *
from sqlalchemy import or_, and_, func

engine = create_engine('postgresql://postgres:123456@localhost:5432/jardineria_clases')
Session = sessionmaker(bind=engine)
session = Session()


Oficinas = session.query(Oficina).filter(
    and_(Oficina.ciudad == 'Madrid', Oficina.pais == 'España')).all()

mostrar_datos(session, Oficinas, campos=['ciudad', 'pais', 'telefono'])

quit()
## funcion de promedio avg
result = session.query(func.avg(Producto.precioventa)).all()
print(result)
for precio in result:
    print(f"Precio Promedio de Productos: {precio}")

promedio = session.query(func.avg(EmpleadoSueldo.sueldo).label('Promedio_sueldo')).scalar()

print(f"Promedio de Sueldo de Empleados: {promedio}")

print(f"Precio Promedio de Productos: {result[0][0]}")

##fechas

comision = session.query(ComisionVendedor).all()

comisiones = session.query(
    func.extract('month', ComisionVendedor.fecharegistro).label('Mes'),
    func.extract('year', ComisionVendedor.fecharegistro).label('Año'),
    func.sum(ComisionVendedor.comisioncalculada).label('total_mes')
).group_by('Año','Mes').order_by('Año','Mes').all()

print(comisiones)

for mes, anio, total in comisiones:
    print(f"Mes: {mes}")
    print(f"Año: {anio}")
    print(f"Total de Comisiones: {total}")
    print("-------------------------------------------")

from sqlalchemy import text

#codigo_cliente =115
resultado = session.execute(text("select calcular_ventas_totales_temp()"))

res = resultado.fetchall()

for row in res:
    print(row)   

#resultado = session.execute(text("select obtener_suma_pagos("+str(codigo_cliente)+")")).scalar()



producto=filtro_generico(session, Producto)

print(producto)

