from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, ForeignKey, Date, Numeric, Text, Sequence
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.orm  import sessionmaker, Session
from ORM_1 import *

engine = create_engine('postgresql://postgres:123456@localhost:5432/jardineria_clases')
Session = sessionmaker(bind=engine)
session = Session()

Oficinas = session.query(Oficina).filter(Oficina.ciudad=="Paris").all()


Oficinas = session.query(Oficina).filter(Oficina.pais.like("%E%")).all()

## or
from sqlalchemy import or_, and_
Oficinas = session.query(Oficina).filter(or_(Oficina.ciudad=="Paris", Oficina.pais=="Francia")).all()

## and
Oficinas = session.query(Oficina).filter(and_(Oficina.ciudad=="Londres", Oficina.pais=="Inglaterra")).all()


## order by

Oficinas = session.query(Oficina).order_by(Oficina.ciudad.desc()).all()



for oficina in Oficinas:
    print(f"ID de Oficina: {oficina.idoficina}")
    print(f"Código de Oficina: {oficina.codigooficina}")
    print(f"Ciudad: {oficina.ciudad}")
    print(f"País: {oficina.pais}")
    print(f"Región: {oficina.region}")
    print(f"Código Postal: {oficina.codigopostal}")
    print(f"Teléfono: {oficina.telefono}")
    print(f"Línea de Dirección 1: {oficina.lineadireccion1}")
    print(f"Línea de Dirección 2: {oficina.lineadireccion2}")
    print("-------------------------------------------")


Productos = session.query(Producto).filter(Producto.cantidadstock.between(10,20)).all()

nombres_producto= ['Jardin','Higuera','Peral']

Productos = session.query(Producto).filter(Producto.nombre.in_(nombres_producto)).all()

for producto in Productos:
    print(f"ID de Producto: {producto.idproducto}")
    print(f"Código de Producto: {producto.codigo_producto}")
    print(f"Nombre: {producto.nombre}")
    print(f"ID de Gama Producto: {producto.idgamaproducto}")
    print(f"Dimensiones: {producto.dimensiones}")
    print(f"Proveedor: {producto.proveedor}")
    print(f"Descripción: {producto.descripcion}")
    print(f"Cantidad Stock: {producto.cantidadstock}")
    print(f"Precio Vendido: {producto.precioventa}")
    print(f"Precio Proveedor: {producto.precioproveedor}")
    print("-------------------------------------------")
