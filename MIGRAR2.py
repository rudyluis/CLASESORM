from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session, relationship

engine = create_engine('postgresql://postgres:123456@localhost:5432/jardineria_clases')

Base = automap_base()

Base.prepare(engine, reflect=True)

Oficina = Base.classes.oficina
Empleado = Base.classes.empleado
Pedido = Base.classes.pedido
DetallePedido = Base.classes.detallepedido
Pago = Base.classes.pago
Cliente = Base.classes.cliente
Producto = Base.classes.producto
GamaProducto = Base.classes.gamaproducto
Inventario = Base.classes.inventario
ComisionVendedor = Base.classes.comision_vendedor
SystemLog = Base.classes.system_log
EmpleadoSueldo = Base.classes.empleado_sueldo
EmpleadoPlanilla = Base.classes.empleado_planilla

session = Session(engine)

print("Conexión a la base de datos establecida correctamente")

Oficinas = session.query(Oficina).all()
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

Empleados = session.query(Empleado).all()
for empleado in Empleados:
    print(f"ID de Empleado: {empleado.idempleado}")
    print(f"Código de Empleado: {empleado.codigo_empleado}")
    print(f"Nombre: {empleado.nombre}")
    print(f"Apellido 1: {empleado.apellido1}")
    print(f"Apellido 2: {empleado.apellido2}")
    print(f"Extensión: {empleado.extension}")
    print(f"Email: {empleado.email}")
    print(f"ID de Oficina: {empleado.idoficina}")
    print(f"Puesto: {empleado.puesto}")
