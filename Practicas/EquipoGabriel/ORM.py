# INTEGRANTES:
# RENATA ANEYBA, GABRIEL VARGAS, JOAQUIN LARA
from sqlalchemy import (Column, Integer, String, ForeignKey, Date, Time,Numeric, Text, Boolean, DateTime, Sequence, func)
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('postgresql://postgres:123456@localhost:5432/gimnasio')
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()
 
class Sucursal(Base):
    __tablename__ = 'sucursal'
    id = Column(Integer, primary_key=True)
    codigo = Column(String(10), unique=True, nullable=False)
    nombre = Column(String(50), nullable=False)
    ciudad = Column(String(30), nullable=False)
    direccion = Column(String(100), nullable=False)
    telefono = Column(String(20))
    clientes = relationship('Cliente', back_populates='sucursal')
    entrenadores = relationship('Entrenador', back_populates='sucursal')
    def __repr__(self):
        return f"<Sucursal(id={self.id}, codigo={self.codigo}, nombre={self.nombre}, ciudad={self.ciudad}, direccion={self.direccion}, telefono={self.telefono})>"
 
    @staticmethod
    def mostrar_todas_las_sucursales(session):
        sucursales = session.query(Sucursal).all()
        for s in sucursales:
            print(s)
 
    @staticmethod
    def mostrar_sucursal_por_id(session, id_sucursal):
        s = session.query(Sucursal).filter(Sucursal.id == id_sucursal).first()
        if s:
            print('SUCURSAL ENCONTRADA:', s)
        else:
            print('No existe la sucursal mencionada')
 
    @staticmethod
    def agregar_sucursal(session, codigo, nombre, ciudad, direccion, telefono=None):
        nueva = Sucursal(codigo=codigo, nombre=nombre, ciudad=ciudad, direccion=direccion, telefono=telefono)
        session.add(nueva)
        session.commit()
        print('Se agregó una nueva sucursal')
 
    @staticmethod
    def modificar_sucursal(session, id_sucursal, **kwargs):
        s = session.query(Sucursal).filter_by(id=id_sucursal).first()
        if s:
            for k, v in kwargs.items(): setattr(s, k, v)
            session.commit()
            print('Sucursal actualizada')
        else:
            print('Sucursal no encontrada')
 
    @staticmethod
    def eliminar_sucursal(session, id_sucursal):
        s = session.query(Sucursal).filter_by(id=id_sucursal).first()
        if s:
            session.delete(s)
            session.commit()
            print('Sucursal eliminada')
        else:
            print('Sucursal no encontrada')
 
class Cliente(Base):
    __tablename__ = 'cliente'
    id = Column(Integer, primary_key=True)
    dni = Column(String(20), unique=True, nullable=False)
    nombre = Column(String(50), nullable=False)
    apellido = Column(String(50), nullable=False)
    fecha_nacimiento = Column(Date)
    telefono = Column(String(20))
    email = Column(String(100), unique=True)
    id_sucursal = Column(Integer, ForeignKey('sucursal.id'), nullable=False)
    id_membresia = Column(Integer, ForeignKey('tipo_membresia.id'))
    fecha_alta = Column(DateTime, default=func.now())
    fecha_baja = Column(DateTime)
    sucursal = relationship('Sucursal', back_populates='clientes')
    membresia = relationship('TipoMembresia', back_populates='clientes')
    reservas = relationship('ReservaClase', back_populates='cliente')
    pagos = relationship('Pago', back_populates='cliente')
    def __repr__(self):
        return f"<Cliente(id={self.id}, dni={self.dni}, nombre={self.nombre} {self.apellido}, email={self.email})>"
 
    @staticmethod
    def mostrar_todos_los_clientes(session):
        for c in session.query(Cliente).all(): print(c)
 
    @staticmethod
    def agregar_cliente(session, dni, nombre, apellido, id_sucursal, email=None, telefono=None, fecha_nacimiento=None):
        nuevo = Cliente(dni=dni, nombre=nombre, apellido=apellido,
                        id_sucursal=id_sucursal, email=email,
                        telefono=telefono, fecha_nacimiento=fecha_nacimiento)
        session.add(nuevo)
        session.commit()
        print('Cliente agregado correctamente')
 
    @staticmethod
    def modificar_cliente(session, id_cliente, **kwargs):
        c = session.query(Cliente).filter_by(id=id_cliente).first()
        if c:
            for k,v in kwargs.items(): setattr(c, k, v)
            session.commit()
            print('Cliente actualizado')
        else:
            print('Cliente no encontrado')
 
    @staticmethod
    def eliminar_cliente(session, id_cliente):
        c = session.query(Cliente).filter_by(id=id_cliente).first()
        if c:
            session.delete(c)
            session.commit()
            print('Cliente eliminado')
        else:
            print('Cliente no encontrado')
 
class TipoMembresia(Base):
    __tablename__ = 'tipo_membresia'
    id = Column(Integer, primary_key=True)
    nombre = Column(String(30), nullable=False, unique=True)
    duracion_meses = Column(Integer, nullable=False)  # e.g. 1, 3, 12
    precio = Column(Numeric(10,2), nullable=False)
    descripcion = Column(Text)
    clientes = relationship('Cliente', back_populates='membresia')
    inscripciones = relationship('Inscripcion', back_populates='membresia')
    def __repr__(self):
        return f"<TipoMembresia(id={self.id}, nombre={self.nombre}, duracion_meses={self.duracion_meses}, precio={self.precio})>"
 
    @staticmethod
    def mostrar_todos_los_tipos(session):
        for t in session.query(TipoMembresia).all(): print(t)
 
    @staticmethod
    def mostrar_tipo_por_id(session, id_tipo):
        t = session.query(TipoMembresia).filter(TipoMembresia.id == id_tipo).first()
        if t:
            print('TIPO ENCONTRADO:', t)
        else:
            print('Tipo de membresía no encontrado')
 
    @staticmethod
    def agregar_tipo(session, nombre, duracion_meses, precio, descripcion=None):
        nuevo = TipoMembresia(nombre=nombre, duracion_meses=duracion_meses, precio=precio, descripcion=descripcion)
        session.add(nuevo)
        session.commit()
        print('Tipo de membresía agregado')
 
    @staticmethod
    def modificar_tipo(session, id_tipo, **kwargs):
        t = session.query(TipoMembresia).filter_by(id=id_tipo).first()
        if t:
            for k, v in kwargs.items(): setattr(t, k, v)
            session.commit()
            print('Tipo actualizado')
        else:
            print('Tipo no encontrado')
 
    @staticmethod
    def eliminar_tipo(session, id_tipo):
        t = session.query(TipoMembresia).filter_by(id=id_tipo).first()
        if t:
            session.delete(t)
            session.commit()
            print('Tipo eliminado')
        else:
            print('Tipo no encontrado')
 
 
class Inscripcion(Base):
    __tablename__ = 'inscripcion'
    id = Column(Integer, primary_key=True)
    id_cliente = Column(Integer, ForeignKey('cliente.id'), nullable=False)
    id_membresia = Column(Integer, ForeignKey('tipo_membresia.id'), nullable=False)
    fecha_inicio = Column(DateTime, default=func.now())
    fecha_fin = Column(DateTime)
    activa = Column(Boolean, default=True)
    cliente = relationship('Cliente')
    membresia = relationship('TipoMembresia', back_populates='inscripciones')
    pagos = relationship('Pago', back_populates='inscripcion')
    def __repr__(self):
        return f"<Inscripcion(id={self.id}, id_cliente={self.id_cliente}, id_membresia={self.id_membresia}, activa={self.activa})>"
 
    @staticmethod
    def mostrar_todas_inscripciones(session):
        for ins in session.query(Inscripcion).all(): print(ins)
 
    @staticmethod
    def mostrar_inscripcion_por_id(session, id_inscripcion):
        ins = session.query(Inscripcion).filter(Inscripcion.id == id_inscripcion).first()
        if ins:
            print('INSCRIPCIÓN ENCONTRADA:', ins)
        else:
            print('Inscripción no encontrada')
 
    @staticmethod
    def agregar_inscripcion(session, id_cliente, id_membresia, fecha_inicio=None, fecha_fin=None):
        nueva = Inscripcion(id_cliente=id_cliente, id_membresia=id_membresia,
                            fecha_inicio=fecha_inicio or func.now(), fecha_fin=fecha_fin)
        session.add(nueva)
        session.commit()
        print('Inscripción agregada')
 
    @staticmethod
    def modificar_inscripcion(session, id_inscripcion, **kwargs):
        ins = session.query(Inscripcion).filter_by(id=id_inscripcion).first()
        if ins:
            for k, v in kwargs.items(): setattr(ins, k, v)
            session.commit()
            print('Inscripción actualizada')
        else:
            print('Inscripción no encontrada')
 
    @staticmethod
    def eliminar_inscripcion(session, id_inscripcion):
        ins = session.query(Inscripcion).filter_by(id=id_inscripcion).first()
        if ins:
            session.delete(ins)
            session.commit()
            print('Inscripción eliminada')
        else:
            print('Inscripción no encontrada')
 
class Entrenador(Base):
    __tablename__ = 'entrenador'
    id = Column(Integer, primary_key=True)
    dni = Column(String(20), unique=True, nullable=False)
    nombre = Column(String(50), nullable=False)
    apellido = Column(String(50), nullable=False)
    especialidad = Column(String(50))  # ej. yoga, crossfit
    id_sucursal = Column(Integer, ForeignKey('sucursal.id'), nullable=False)
    sucursal = relationship('Sucursal', back_populates='entrenadores')
    horarios = relationship('Horario', back_populates='entrenador')
   
    def __repr__(self):
        return f"<Entrenador(id={self.id}, dni={self.dni}, nombre={self.nombre} {self.apellido}, especialidad={self.especialidad})>"
 
    @staticmethod
    def mostrar_todos_los_entrenadores(session):
        for e in session.query(Entrenador).all(): print(e)
 
    @staticmethod
    def mostrar_entrenador_por_id(session, id_entrenador):
        e = session.query(Entrenador).filter(Entrenador.id == id_entrenador).first()
        if e:
            print('ENTRENADOR ENCONTRADO:', e)
        else:
            print('Entrenador no encontrado')
 
    @staticmethod
    def agregar_entrenador(session, dni, nombre, apellido, id_sucursal, especialidad=None):
        nuevo = Entrenador(dni=dni, nombre=nombre, apellido=apellido, id_sucursal=id_sucursal, especialidad=especialidad)
        session.add(nuevo)
        session.commit()
        print('Entrenador agregado correctamente')
 
    @staticmethod
    def modificar_entrenador(session, id_entrenador, **kwargs):
        e = session.query(Entrenador).filter_by(id=id_entrenador).first()
        if e:
            for k, v in kwargs.items(): setattr(e, k, v)
            session.commit()
            print('Entrenador actualizado')
        else:
            print('Entrenador no encontrado')
 
    @staticmethod
    def eliminar_entrenador(session, id_entrenador):
        e = session.query(Entrenador).filter_by(id=id_entrenador).first()
        if e:
            session.delete(e)
            session.commit()
            print('Entrenador eliminado')
        else:
            print('Entrenador no encontrado')
 
 
class Clase(Base):
    __tablename__ = 'clase'
    id = Column(Integer, primary_key=True)
    nombre = Column(String(30), nullable=False, unique=True)  # yoga, spinning, etc.
    descripcion = Column(Text)
    duracion_min = Column(Integer, nullable=False)  # duración en minutos
    horarios = relationship('Horario', back_populates='clase')
    def __repr__(self):
        return f"<Clase(id={self.id}, nombre={self.nombre}, duracion_min={self.duracion_min})>"
 
    @staticmethod
    def mostrar_todas_las_clases(session):
        for c in session.query(Clase).all(): print(c)
 
    @staticmethod
    def mostrar_clase_por_id(session, id_clase):
        c = session.query(Clase).filter(Clase.id == id_clase).first()
        if c:
            print('CLASE ENCONTRADA:', c)
        else:
            print('Clase no encontrada')
 
    @staticmethod
    def agregar_clase(session, nombre, duracion_min, descripcion=None):
        nueva = Clase(nombre=nombre, duracion_min=duracion_min, descripcion=descripcion)
        session.add(nueva)
        session.commit()
        print('Clase agregada correctamente')
 
    @staticmethod
    def modificar_clase(session, id_clase, **kwargs):
        c = session.query(Clase).filter_by(id=id_clase).first()
        if c:
            for k, v in kwargs.items(): setattr(c, k, v)
            session.commit()
            print('Clase actualizada')
        else:
            print('Clase no encontrada')
 
    @staticmethod
    def eliminar_clase(session, id_clase):
        c = session.query(Clase).filter_by(id=id_clase).first()
        if c:
            session.delete(c)
            session.commit()
            print('Clase eliminada')
        else:
            print('Clase no encontrada')
 
class Horario(Base):
    __tablename__ = 'horario'
    id = Column(Integer, primary_key=True)
    id_clase = Column(Integer, ForeignKey('clase.id'), nullable=False)
    id_entrenador = Column(Integer, ForeignKey('entrenador.id'), nullable=False)
    dia_semana = Column(String(9), nullable=False)  # lunes–domingo
    hora_inicio = Column(Time, nullable=False)
    sala = Column(String(20))  # e.g. Sala A, Sala B
    clase = relationship('Clase', back_populates='horarios')
    entrenador = relationship('Entrenador', back_populates='horarios')
    reservas = relationship('ReservaClase', back_populates='horario')
    def __repr__(self):
        return f"<Horario(id={self.id}, clase={self.id_clase}, entrenador={self.id_entrenador}, dia_semana={self.dia_semana}, hora_inicio={self.hora_inicio}, sala={self.sala})>"
 
    @staticmethod
    def mostrar_todos_los_horarios(session):
        for h in session.query(Horario).all(): print(h)
 
    @staticmethod
    def mostrar_horario_por_id(session, id_horario):
        h = session.query(Horario).filter(Horario.id == id_horario).first()
        if h:
            print('HORARIO ENCONTRADO:', h)
        else:
            print('Horario no encontrado')
 
    @staticmethod
    def agregar_horario(session, id_clase, id_entrenador, dia_semana, hora_inicio, sala=None):
        nuevo = Horario(id_clase=id_clase, id_entrenador=id_entrenador, dia_semana=dia_semana, hora_inicio=hora_inicio, sala=sala)
        session.add(nuevo)
        session.commit()
        print('Horario agregado correctamente')
 
    @staticmethod
    def modificar_horario(session, id_horario, **kwargs):
        h = session.query(Horario).filter_by(id=id_horario).first()
        if h:
            for k, v in kwargs.items(): setattr(h, k, v)
            session.commit()
            print('Horario actualizado')
        else:
            print('Horario no encontrado')
 
    @staticmethod
    def eliminar_horario(session, id_horario):
        h = session.query(Horario).filter_by(id=id_horario).first()
        if h:
            session.delete(h)
            session.commit()
            print('Horario eliminado')
        else:
            print('Horario no encontrado')
 
class ReservaClase(Base):
    __tablename__ = 'reserva_clase'
    id = Column(Integer, primary_key=True)
    id_cliente = Column(Integer, ForeignKey('cliente.id'), nullable=False)
    id_horario = Column(Integer, ForeignKey('horario.id'), nullable=False)
    fecha_reserva = Column(DateTime, default=func.now())
    asistio = Column(Boolean)
    cliente = relationship('Cliente', back_populates='reservas')
    horario = relationship('Horario', back_populates='reservas')
    def __repr__(self):
        return f"<ReservaClase(id={self.id}, id_cliente={self.id_cliente}, id_horario={self.id_horario}, fecha_reserva={self.fecha_reserva}, asistio={self.asistio})>"
 
    @staticmethod
    def mostrar_todas_las_reservas(session):
        for r in session.query(ReservaClase).all(): print(r)
 
    @staticmethod
    def mostrar_reserva_por_id(session, id_reserva):
        r = session.query(ReservaClase).filter(ReservaClase.id == id_reserva).first()
        if r:
            print('RESERVA ENCONTRADA:', r)
        else:
            print('Reserva no encontrada')
 
    @staticmethod
    def agregar_reserva(session, id_cliente, id_horario, fecha_reserva=None, asistio=None):
        nueva = ReservaClase(id_cliente=id_cliente, id_horario=id_horario, fecha_reserva=fecha_reserva or func.now(), asistio=asistio)
        session.add(nueva)
        session.commit()
        print('Reserva agregada correctamente')
 
    @staticmethod
    def modificar_reserva(session, id_reserva, **kwargs):
        r = session.query(ReservaClase).filter_by(id=id_reserva).first()
        if r:
            for k, v in kwargs.items(): setattr(r, k, v)
            session.commit()
            print('Reserva actualizada')
        else:
            print('Reserva no encontrada')
 
    @staticmethod
    def eliminar_reserva(session, id_reserva):
        r = session.query(ReservaClase).filter_by(id=id_reserva).first()
        if r:
            session.delete(r)
            session.commit()
            print('Reserva eliminada')
        else:
            print('Reserva no encontrada')
class Pago(Base):
    __tablename__ = 'pago'
    id = Column(Integer, primary_key=True)
    id_cliente = Column(Integer, ForeignKey('cliente.id'), nullable=False)
    id_inscripcion = Column(Integer, ForeignKey('inscripcion.id'), nullable=True)
    fecha_pago = Column(DateTime, default=func.now(), nullable=False)
    monto = Column(Numeric(10,2), nullable=False)
    metodo = Column(String(30))       # ej. 'tarjeta', 'efectivo', 'transferencia'
    referencia = Column(String(50))   # número de transacción o comprobante
    cliente = relationship('Cliente', back_populates='pagos')
    inscripcion = relationship('Inscripcion', back_populates='pagos')
 
 
    def __repr__(self):
        return (f"<Pago(id={self.id}, id_cliente={self.id_cliente}, "
                f"id_inscripcion={self.id_inscripcion}, fecha_pago={self.fecha_pago}, "
                f"monto={self.monto}, metodo={self.metodo})>")
 
    @staticmethod
    def mostrar_todos_los_pagos(session):
        for p in session.query(Pago).all():
            print(p)
 
    @staticmethod
    def mostrar_pago_por_id(session, id_pago):
        p = session.query(Pago).filter(Pago.id == id_pago).first()
        if p:
            print('PAGO ENCONTRADO:', p)
        else:
            print('Pago no encontrado')
 
    @staticmethod
    def agregar_pago(session, id_cliente, monto, metodo=None, referencia=None, id_inscripcion=None, fecha_pago=None):
        nuevo = Pago(
            id_cliente=id_cliente,
            id_inscripcion=id_inscripcion,
            monto=monto,
            metodo=metodo,
            referencia=referencia,
            fecha_pago=fecha_pago or func.now()
        )
        session.add(nuevo)
        session.commit()
        print('Pago registrado correctamente')
 
    @staticmethod
    def modificar_pago(session, id_pago, **kwargs):
        p = session.query(Pago).filter_by(id=id_pago).first()
        if p:
            for k, v in kwargs.items(): setattr(p, k, v)
            session.commit()
            print('Pago actualizado')
        else:
            print('Pago no encontrado')
 
    @staticmethod
    def eliminar_pago(session, id_pago):
        p = session.query(Pago).filter_by(id=id_pago).first()
        if p:
            session.delete(p)
            session.commit()
            print('Pago eliminado')
        else:
            print('Pago no encontrado')
           
 
# Conectamos al engine apuntando a la base ya creada
engine = create_engine('postgresql+psycopg2://postgres:241210@localhost:5432/gimnasio')

# Crear todas las tablas definidas en el modelo
Base.metadata.create_all(engine)
print("Tablas creadas con éxito.")