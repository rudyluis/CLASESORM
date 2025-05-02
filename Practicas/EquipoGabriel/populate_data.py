# INTEGRANTES:
# RENATA ANEYBA, GABRIEL VARGAS, JOAQUIN LARA
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta

# --- URI solo para conectarse a la BD ya existente ---
DB_URI = 'postgresql+psycopg2://postgres:123456@localhost:5432/gimnasio'

# --- Importa tu ORM (sin tocar la creación de Base) ---
from ORM import Base, Sucursal, TipoMembresia, Cliente, Entrenador, Clase, Horario, Inscripcion, ReservaClase, Pago

def main():
    # 1) Conexión y sesión
    engine = create_engine(DB_URI)
    Session = sessionmaker(bind=engine)
    session = Session()

    # 2) Datos estáticos: listas de 15 diccionarios por entidad
    sucursales = [
        {'codigo':'SUC001','nombre':'Gimnasio Central','ciudad':'La Paz','direccion':'Av. Mariscal Santa Cruz 123','telefono':'72123456'},
        {'codigo':'SUC002','nombre':'Gimnasio Norte','ciudad':'El Alto','direccion':'Calle 20 de Octubre 456','telefono':'72123457'},
        {'codigo':'SUC003','nombre':'Gimnasio Sur','ciudad':'Cochabamba','direccion':'Calle Sucre 789','telefono':'72123458'},
        {'codigo':'SUC004','nombre':'Gimnasio Este','ciudad':'Santa Cruz','direccion':'Av. Grigotá 101','telefono':'72123459'},
        {'codigo':'SUC005','nombre':'Gimnasio Oeste','ciudad':'Sucre','direccion':'Calle España 202','telefono':'72123460'},
        {'codigo':'SUC006','nombre':'Gimnasio Miraflores','ciudad':'La Paz','direccion':'Av. Arce 303','telefono':'72123461'},
        {'codigo':'SUC007','nombre':'Gimnasio Achumani','ciudad':'La Paz','direccion':'Calle Agosto 404','telefono':'72123462'},
        {'codigo':'SUC008','nombre':'Gimnasio Sopocachi','ciudad':'La Paz','direccion':'Av. 16 de Julio 505','telefono':'72123463'},
        {'codigo':'SUC009','nombre':'Gimnasio Cala Cala','ciudad':'Cochabamba','direccion':'Av. América 606','telefono':'72123464'},
        {'codigo':'SUC010','nombre':'Gimnasio Equipetrol','ciudad':'Santa Cruz','direccion':'Av. El Trompillo 707','telefono':'72123465'},
        {'codigo':'SUC011','nombre':'Gimnasio San Miguel','ciudad':'El Alto','direccion':'Av. 6 de Marzo 808','telefono':'72123466'},
        {'codigo':'SUC012','nombre':'Gimnasio Potosí','ciudad':'Potosí','direccion':'Calle Sucre 909','telefono':'72123467'},
        {'codigo':'SUC013','nombre':'Gimnasio Tarija','ciudad':'Tarija','direccion':'Av. Gral. Trigo 111','telefono':'72123468'},
        {'codigo':'SUC014','nombre':'Gimnasio Oruro','ciudad':'Oruro','direccion':'Calle Bolívar 222','telefono':'72123469'},
        {'codigo':'SUC015','nombre':'Gimnasio Trinidad','ciudad':'Santa Cruz','direccion':'Av. Bush 333','telefono':'72123470'},
    ]

    tipos = [
        {'nombre':'Básica Mensual','duracion_meses':1,'precio':150.00,'descripcion':'Acceso básico durante un mes'},
        {'nombre':'Estándar Trimestral','duracion_meses':3,'precio':400.00,'descripcion':'Acceso estándar durante tres meses'},
        {'nombre':'Premium Anual','duracion_meses':12,'precio':1200.00,'descripcion':'Acceso completo durante un año'},
        {'nombre':'Día Suelto','duracion_meses':0,'precio':30.00,'descripcion':'Entrada de un solo día'},
        {'nombre':'Semanal','duracion_meses':0,'precio':70.00,'descripcion':'Acceso durante una semana'},
        {'nombre':'Semestral','duracion_meses':6,'precio':700.00,'descripcion':'Acceso durante seis meses'},
        {'nombre':'Nocturna','duracion_meses':1,'precio':100.00,'descripcion':'Acceso nocturno durante un mes'},
        {'nombre':'Fin de Semana','duracion_meses':0,'precio':50.00,'descripcion':'Acceso sábados y domingos'},
        {'nombre':'Parejas Mensual','duracion_meses':1,'precio':250.00,'descripcion':'Dos personas, un mes'},
        {'nombre':'Estudiantil','duracion_meses':3,'precio':300.00,'descripcion':'Precio reducido para estudiantes, 3 meses'},
        {'nombre':'Corporativo','duracion_meses':12,'precio':1000.00,'descripcion':'Acceso anual para empresas'},
        {'nombre':'Golden','duracion_meses':12,'precio':1500.00,'descripcion':'Beneficios VIP durante un año'},
        {'nombre':'Trimestral Plus','duracion_meses':3,'precio':450.00,'descripcion':'Trimestre con clases incluidas'},
        {'nombre':'Mensual Plus','duracion_meses':1,'precio':200.00,'descripcion':'Mes con 4 clases semanales'},
        {'nombre':'Prueba 1 Día','duracion_meses':0,'precio':0.00,'descripcion':'Prueba gratuita de un día'},
    ]

    clientes = [
        {'dni':'12345678','nombre':'Juan','apellido':'Perez','fecha_nacimiento':'1995-05-10','telefono':'79123456','email':'juan.perez@example.com','id_sucursal':1,'id_membresia':1},
        {'dni':'23456789','nombre':'María','apellido':'González','fecha_nacimiento':'1990-11-20','telefono':'79123457','email':'maria.gonzalez@example.com','id_sucursal':2,'id_membresia':2},
        {'dni':'34567890','nombre':'Carlos','apellido':'Lopez','fecha_nacimiento':'1985-07-15','telefono':'79123458','email':'carlos.lopez@example.com','id_sucursal':3,'id_membresia':3},
        {'dni':'45678901','nombre':'Ana','apellido':'Martinez','fecha_nacimiento':'1998-03-05','telefono':'79123459','email':'ana.martinez@example.com','id_sucursal':4,'id_membresia':4},
        {'dni':'56789012','nombre':'Luis','apellido':'Ramirez','fecha_nacimiento':'2000-12-01','telefono':'79123460','email':'luis.ramirez@example.com','id_sucursal':5,'id_membresia':5},
        {'dni':'67890123','nombre':'Sofia','apellido':'Diaz','fecha_nacimiento':'1997-09-17','telefono':'79123461','email':'sofia.diaz@example.com','id_sucursal':6,'id_membresia':6},
        {'dni':'78901234','nombre':'Miguel','apellido':'Torres','fecha_nacimiento':'1988-02-28','telefono':'79123462','email':'miguel.torres@example.com','id_sucursal':7,'id_membresia':7},
        {'dni':'89012345','nombre':'Laura','apellido':'Vargas','fecha_nacimiento':'1992-06-30','telefono':'79123463','email':'laura.vargas@example.com','id_sucursal':8,'id_membresia':8},
        {'dni':'90123456','nombre':'Diego','apellido':'Fernandez','fecha_nacimiento':'1993-01-22','telefono':'79123464','email':'diego.fernandez@example.com','id_sucursal':9,'id_membresia':9},
        {'dni':'01234567','nombre':'Elena','apellido':'Castro','fecha_nacimiento':'1989-08-11','telefono':'79123465','email':'elena.castro@example.com','id_sucursal':10,'id_membresia':10},
        {'dni':'11223344','nombre':'Pedro','apellido':'Rojas','fecha_nacimiento':'1996-04-19','telefono':'79123466','email':'pedro.rojas@example.com','id_sucursal':11,'id_membresia':11},
        {'dni':'22334455','nombre':'Marta','apellido':'Sanchez','fecha_nacimiento':'1994-10-05','telefono':'79123467','email':'marta.sanchez@example.com','id_sucursal':12,'id_membresia':12},
        {'dni':'33445566','nombre':'Ricardo','apellido':'Alvarez','fecha_nacimiento':'1991-12-23','telefono':'79123468','email':'ricardo.alvarez@example.com','id_sucursal':13,'id_membresia':13},
        {'dni':'44556677','nombre':'Patricia','apellido':'Mendoza','fecha_nacimiento':'2001-05-02','telefono':'79123469','email':'patricia.mendoza@example.com','id_sucursal':14,'id_membresia':14},
        {'dni':'55667788','nombre':'Fernando','apellido':'Gutierrez','fecha_nacimiento':'1987-11-29','telefono':'79123470','email':'fernando.gutierrez@example.com','id_sucursal':15,'id_membresia':15},
    ]

    entrenadores = [
        {'dni':'99887766','nombre':'Diego','apellido':'Soto','especialidad':'Yoga','id_sucursal':1},
        {'dni':'88776655','nombre':'Paula','apellido':'Rincon','especialidad':'Crossfit','id_sucursal':2},
        {'dni':'77665544','nombre':'Jorge','apellido':'Blanco','especialidad':'Spinning','id_sucursal':3},
        {'dni':'66554433','nombre':'Carla','apellido':'Mora','especialidad':'Pilates','id_sucursal':4},
        {'dni':'55443322','nombre':'Andrés','apellido':'Quispe','especialidad':'Boxeo','id_sucursal':5},
        {'dni':'44332211','nombre':'Natalia','apellido':'Peña','especialidad':'Zumba','id_sucursal':6},
        {'dni':'33221100','nombre':'Sergio','apellido':'Vega','especialidad':'Musculación','id_sucursal':7},
        {'dni':'22110099','nombre':'Valeria','apellido':'Navarro','especialidad':'HIIT','id_sucursal':8},
        {'dni':'11009988','nombre':'Hugo','apellido':'Cruz','especialidad':'Natación','id_sucursal':9},
        {'dni':'00998877','nombre':'Elsa','apellido':'Ortega','especialidad':'Yoga','id_sucursal':10},
        {'dni':'99880011','nombre':'Rafael','apellido':'Pérez','especialidad':'Cycling','id_sucursal':11},
        {'dni':'88770022','nombre':'Claudia','apellido':'Salazar','especialidad':'TRX','id_sucursal':12},
        {'dni':'77660033','nombre':'Martin','apellido':'Flores','especialidad':'Boxeo','id_sucursal':13},
        {'dni':'66550044','nombre':'Ana','apellido':'Rojas','especialidad':'Zumba','id_sucursal':14},
        {'dni':'55440055','nombre':'Luis','apellido':'Huanca','especialidad':'Crossfit','id_sucursal':15},
    ]

    clases = [
        {'nombre':'Yoga','descripcion':'Clase de yoga para flexibilidad y relajación','duracion_min':60},
        {'nombre':'Pilates','descripcion':'Pilates para fortalecimiento del core','duracion_min':50},
        {'nombre':'Spinning','descripcion':'Clase de ciclismo indoor','duracion_min':45},
        {'nombre':'Boxeo','descripcion':'Entrenamiento de boxeo','duracion_min':60},
        {'nombre':'Zumba','descripcion':'Baile fitness','duracion_min':55},
        {'nombre':'Crossfit','descripcion':'Entrenamiento funcional intenso','duracion_min':50},
        {'nombre':'HIIT','descripcion':'Intervalos de alta intensidad','duracion_min':30},
        {'nombre':'TRX','descripcion':'Entrenamiento en suspensión','duracion_min':40},
        {'nombre':'Natación','descripcion':'Nado libre en piscina','duracion_min':60},
        {'nombre':'Cycling','descripcion':'Ciclismo de interior guiado','duracion_min':45},
        {'nombre':'BodyPump','descripcion':'Entrenamiento de resistencia con pesas','duracion_min':50},
        {'nombre':'Cardio','descripcion':'Cardio mixto','duracion_min':40},
        {'nombre':'Stretching','descripcion':'Estiramientos guiados','duracion_min':30},
        {'nombre':'Step','descripcion':'Aeróbicos con step','duracion_min':45},
        {'nombre':'Kickboxing','descripcion':'Kickboxing fitness','duracion_min':60},
    ]

    horarios = [
        {'id_clase':1,'id_entrenador':1,'dia_semana':'Lunes','hora_inicio':'08:00:00','sala':'Sala A'},
        {'id_clase':2,'id_entrenador':4,'dia_semana':'Martes','hora_inicio':'09:00:00','sala':'Sala B'},
        {'id_clase':3,'id_entrenador':3,'dia_semana':'Miércoles','hora_inicio':'18:00:00','sala':'Sala C'},
        {'id_clase':4,'id_entrenador':5,'dia_semana':'Jueves','hora_inicio':'19:00:00','sala':'Sala A'},
        {'id_clase':5,'id_entrenador':6,'dia_semana':'Viernes','hora_inicio':'17:00:00','sala':'Sala B'},
        {'id_clase':6,'id_entrenador':2,'dia_semana':'Sábado','hora_inicio':'10:00:00','sala':'Sala C'},
        {'id_clase':7,'id_entrenador':8,'dia_semana':'Domingo','hora_inicio':'11:00:00','sala':'Sala A'},
        {'id_clase':8,'id_entrenador':12,'dia_semana':'Lunes','hora_inicio':'12:00:00','sala':'Sala B'},
        {'id_clase':9,'id_entrenador':9,'dia_semana':'Martes','hora_inicio':'07:00:00','sala':'Piscina'},
        {'id_clase':10,'id_entrenador':11,'dia_semana':'Miércoles','hora_inicio':'20:00:00','sala':'Sala C'},
        {'id_clase':11,'id_entrenador':11,'dia_semana':'Jueves','hora_inicio':'08:00:00','sala':'Sala A'},
        {'id_clase':12,'id_entrenador':14,'dia_semana':'Viernes','hora_inicio':'09:00:00','sala':'Sala B'},
        {'id_clase':13,'id_entrenador':7,'dia_semana':'sábado','hora_inicio':'16:00:00','sala':'Sala C'},
        {'id_clase':14,'id_entrenador':10,'dia_semana':'Domingo','hora_inicio':'10:00:00','sala':'Sala A'},
        {'id_clase':15,'id_entrenador':13,'dia_semana':'Lunes','hora_inicio':'18:00:00','sala':'Sala B'},
    ]

    # 3) Commit preliminar para poder referenciar IDs auto
    for d in sucursales:     session.add(Sucursal(**d))
    for d in tipos:          session.add(TipoMembresia(**d))
    for d in clientes:       session.add(Cliente(**d))
    for d in entrenadores:   session.add(Entrenador(**d))
    for d in clases:         session.add(Clase(**d))
    for d in horarios:       session.add(Horario(**d))
    session.commit()

    # 4) Generar dinámicamente inscripciones, reservas y pagos
    now = datetime.now()
    inscripciones, reservas, pagos = [], [], []
    for i in range(1,16):
        start = now - timedelta(days=7*i)
        tipo = session.get(TipoMembresia, i)
        end = start + timedelta(days=(30 * tipo.duracion_meses if tipo.duracion_meses>0 else 1))
        inscripciones.append({'id_cliente':i,'id_membresia':i,'fecha_inicio':start,'fecha_fin':end,'activa':True})
        reservas.append({'id_cliente':i,'id_horario':i,'fecha_reserva':start + timedelta(days=10),'asistio': bool(i%2)})
        pagos.append({'id_cliente':i,'id_inscripcion':i,'fecha_pago':start + timedelta(days=1),'monto': float(tipo.precio),'metodo':'tarjeta' if i%2 else 'efectivo','referencia':f'TXN{1000+i}'})

    for d in inscripciones:  session.add(Inscripcion(**d))
    for d in reservas:       session.add(ReservaClase(**d))
    for d in pagos:          session.add(Pago(**d))
    session.commit()

    print("¡Datos poblados con éxito (15 filas por tabla)!")

    session.close()
    engine.dispose()

if __name__== '__main__':
    main()