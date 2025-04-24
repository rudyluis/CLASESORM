from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, ForeignKey, Date, Numeric, Text, Sequence
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.orm  import sessionmaker, Session
from ORM_1 import *
from sqlalchemy import or_, and_, func

engine = create_engine('postgresql://postgres:123456@localhost:5432/jardineria_clases')
Session = sessionmaker(bind=engine)
session = Session()

count_oficinas = session.query(func.count(Oficina.idoficina)).scalar()
##print(session.query(func.count(Oficina.idoficina)))
##quit()
print(f"Cantidad de Oficinas en Paris: {count_oficinas}")

## suma producto
suma_producto = session.query(func.sum(Producto.precioventa)).scalar()
print(f"Suma de Precio de Productos en la tienda: {suma_producto}")

## precio maximo
maximo_precio = session.query(func.max(Producto.precioventa)).scalar()
print(f"Precio Máximo de Productos en la tienda: {maximo_precio}")

## precio minimo
minimo_precio = session.query(func.min(Producto.precioventa)).scalar()
print(f"Precio Mínimo de Productos en la tienda: {minimo_precio}")

## inner join entre empleado y oficina
empleados_oficinas = session.query(Empleado, Oficina).join(Oficina, Empleado.idoficina==Oficina.idoficina).all()

for empleado_oficina in empleados_oficinas:
    print(f"ID de Empleado: {empleado_oficina[0].idempleado}")
    print(f"Nombre: {empleado_oficina[0].nombre}")
    print(f"Apellido: {empleado_oficina[0].apellido1}")
    print(f"ID de Oficina: {empleado_oficina[1].idoficina}")
    print(f"Código de Oficina: {empleado_oficina[1].codigooficina}")
    print(f"Ciudad: {empleado_oficina[1].ciudad}")
    print(f"País: {empleado_oficina[1].pais}")
    print("-------------------------------------------")

result = session.query(Oficina,Empleado).join(Empleado).all()

for oficina_empleado in result:
    print(f"ID de Oficina: {oficina_empleado[0].idoficina}")
    print(f"Nombre de Oficina: {oficina_empleado[0].idoficina}")
    print(f"Código de Oficina: {oficina_empleado[0].codigooficina}")
    print(f"Ciudad de Oficina: {oficina_empleado[0].ciudad}")

## query que filtro por pais españa y me muestro solo los campos region y empleado nomre
result = session.query(Oficina.region,Empleado.nombre).join(Empleado).filter(Oficina.pais=="España").all()

for oficina_empleado in result:
    print(f"Region: {oficina_empleado[0]}")
    print(f"Nombre de Empleado: {oficina_empleado[1]}")
    print("-------------------------------------------")

## having y group by con producto y conunt para productos
result = session.query(Producto.nombre,func.count(Producto.idproducto)).\
    group_by(Producto.nombre).\
    having(func.count(Producto.idproducto)>=2).all()

for producto in result:
    print(f"Nombre: {producto[0]}")
    print(f"Cantidad de Productos: {producto[1]}")
    print("-------------------------------------------")

print("LABEL EN LA FUNCION")
## suma de los productos  agrupados por nombre y precio de venta
result = session.query(Producto.nombre,func.sum(Producto.cantidadstock).label("TotalStock")).\
    group_by(Producto.nombre, Producto.precioventa).\
    having(func.sum(Producto.cantidadstock)>=100).all()

for producto in result:
    print(f"Nombre: {producto.nombre}")
    print(f"Precio de Venta: {producto.TotalStock}")
    print("-------------------------------------------")

## logs por nivel
logs = session.query(SystemLog.log_level, func.count(SystemLog.log_id).label('Total_logs')).\
    group_by(SystemLog.log_level).all()

for log in logs:
    print(f"Nivel de Log: {log.log_level}")
    print(f"Cantidad de Logs: {log.Total_logs}")
    print("-------------------------------------------")