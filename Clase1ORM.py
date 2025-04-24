
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from ORM import Oficina, Empleado,Cliente

engine = create_engine('postgresql://postgres:123456@localhost:5432/jardineria_clases')
Session = sessionmaker(bind=engine)
session = Session()
Oficina.eliminarOficina(session, 10)
quit()
Oficina.modificarOficina(session, 10, ciudad="Nueva Ciudad bolivia", pais="BOLIVIA", codigopostal="591")

quit()


## crear nueva oficina
Oficina.agregarOficina(session, "123456", "Ciudad", "PAIS", "REGION", "12345", "12345678", "L1", "L2")


empleados = session.query(Empleado).all()

print(empleados)

for empleado in empleados:
    print(empleado.codigo_empleado)
    print(empleado.nombre)
    print(empleado.apellido1)
    print(empleado.apellido2)
    print(empleado.extension)
    print(empleado.oficina.codigooficina)
    print(empleado.oficina.ciudad)
    print(empleado.oficina.pais)


oficinas = session.query(Oficina).all()

print(oficinas)

print("===================")

for oficina in oficinas:
    print(oficina.codigooficina)
    print(oficina.ciudad)
    print(oficina.pais)
    print(oficina.region)
    print(oficina.codigopostal)
    print(oficina.telefono)
    print(oficina.lineadireccion1)
    print(oficina.lineadireccion2)  
    ##print(oficina.empleado.codigo_empleado)
    print(oficina.empleado)
    print("===================")

    empleadosoficina=oficina.empleado
    for empleado in empleadosoficina:
        print(empleado.codigo_empleado)
        print(empleado.nombre)


