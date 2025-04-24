from sqlalchemy import Column, Integer, String, ForeignKey, create_engine, func,Date, Text, Sequence, Numeric, SmallInteger, DateTime

from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class Oficina(Base):
    __tablename__ = 'oficina'
    idoficina = Column(Integer, primary_key=True)
    codigooficina = Column(String(10),unique=True, nullable=False)
    ciudad = Column(String(30), nullable=False)
    pais = Column(String(50), nullable=False)
    region = Column(String(50))
    codigopostal = Column(String(50), nullable=False)
    telefono = Column(String(20), nullable=False)
    lineadireccion1= Column(String(50), nullable=False)
    lineadireccion2= Column(String(50))
    empleado =relationship("Empleado", back_populates="oficina")
    def __repr__(self):
        return f"<oficina id={self.codigooficina}, ciudad={self.ciudad}, pais={self.pais}, region={self.region}, codigopostal={self.codigopostal}, telefono={self.telefono}, lineadireccion1={self.lineadireccion1}, lineadireccion2={self.lineadireccion2}>"
    @staticmethod
    def agregarOficina(session, codigooficina, ciudad, pais, region, codigopostal, telefono, lineadireccion1, lineadireccion2):
        nueva_oficina = Oficina(codigooficina=codigooficina, ciudad=ciudad, pais=pais, region=region, codigopostal=codigopostal, telefono=telefono, lineadireccion1=lineadireccion1, lineadireccion2=lineadireccion2)
        session.add(nueva_oficina)
        session.commit()
        print("Nueva Oficina agregada")
    @staticmethod
    def modificarOficina(session, idoficina, **kwargs):
        oficina = session.query(Oficina).filter_by(idoficina=idoficina).first()
        if oficina:
            for key, value in kwargs.items():
                setattr(oficina, key, value)
            session.commit()
            print("Oficina modificada")
        else:
            print("No existe la Oficina")
    @staticmethod
    def eliminarOficina(session, idoficina):
        oficina = session.query(Oficina).filter_by(idoficina=idoficina).first()
        if oficina:
            session.delete(oficina)
            session.commit()
            print("Oficina eliminada")
        else:
            print("No existe la Oficina")
class Empleado(Base):
    __tablename__ = 'empleado'
    idempleado = Column(Integer, primary_key=True)
    codigo_empleado = Column(Integer,unique=True, nullable=False)
    nombre = Column(String(50), nullable=False)
    apellido1 = Column(String(50), nullable=False)
    apellido2 = Column(String(50))
    extension = Column(String(10),nullable=False)
    email = Column(String(50), nullable=False)
    puesto = Column(String(50), nullable=False)
    idoficina = Column(Integer, ForeignKey('oficina.idoficina'), nullable=False)
    idempleadojefe =Column(Integer, ForeignKey('empleado.idempleado'))
    oficina = relationship("Oficina", back_populates="empleado")
    empleadojefe = relationship("Empleado", remote_side=[idempleado])
    def __repr__(self):
        return f"<empleado id={self.codigo_empleado}, nombre={self.nombre}, apellido1={self.apellido1}, apellido2={self.apellido2}, extension={self.extension}, email={self.email}, puesto={self.puesto}, idoficina={self.idoficina}>"

    @staticmethod
    def agregarEmpleado(session, codigo_empleado, nombre, apellido1, apellido2, extension, email, id_oficina, id_empleado_jefe, puesto= None):
        nuevoEmpleado= Empleado( codigo_empleado= codigo_empleado, nombre= nombre, apellido1= apellido1,
                                    apellido2=apellido2, extension=extension, email= email, 
                                     idoficina = id_oficina, idempleadojefe= id_empleado_jefe, puesto=puesto                   
                                )
        session.add(nuevoEmpleado)
        session.commit()
        print("Empleado agregado correctamente")
    
    @staticmethod
    def modificarEmpleado(session, id_empleado, **kwargs):
        empleado= session.query(Empleado).filter_by(idempleado=id_empleado).first()
        if empleado:
            for key, value in kwargs.items():
                setattr(empleado, key,value)
            session.commit()
            print('Empleado Actualizado')
        else:
            print('Empleado no encontrado')

    @staticmethod
    def eliminarEmpleado(session, id_empleado):
        empleado= session.query(Empleado).filter_by(idempleado=id_empleado).first()
        if empleado:
            session.delete(empleado)
            session.commit()
            print('Empleado eliminado')
        else:
            print('No existe el empleado')

class Cliente(Base):
    __tablename__='cliente'
    idcliente= Column(Integer, primary_key=True)
    codigocliente=Column(Integer,unique=True, nullable=False)
    nombrecliente=Column(String(50), nullable=False)
    nombrecontacto=Column(String(50), nullable=False)
    apellidocontacto=Column(String(50), nullable=False)
    telefono=Column(String(15), nullable=False)
    fax=Column(String(15))
    lineadireccion1= Column(String(50), nullable=False)
    lineadireccion2= Column(String(50))
    ciudad= Column(String(30), nullable=False)
    region= Column(String(50))
    pais= Column(String(50), nullable=False)
    codigopostal=Column(String(30), nullable=False)
    idcodigoempleadoventas=Column(Integer, ForeignKey('empleado.idempleado'),nullable=False)
    limite_credito=Column(Numeric (15,2))   ###

    empleadoventas= relationship('Empleado')
    @staticmethod
    def __repr__(self):
        return f"<Cliente {self.nombrecliente} ({self.codigocliente}) - {self.ciudad}, {self.pais}>"
    @staticmethod
    def agregarCliente(session,codigocliente,nombrecliente,nombrecontacto,apellidocontacto,telefono,fax,lineadireccion1,lineadireccion2,ciudad,region,pais,codigopostal,idcodigoempleadoventas,limite_credito):
        nuevoCliente=Cliente(codigocliente=codigocliente,nombrecliente=nombrecliente,nombrecontacto=nombrecontacto,apellidocontacto=apellidocontacto,telefono=telefono,fax=fax,
                              lineadireccion1=lineadireccion1,lineadireccion2=lineadireccion2,ciudad=ciudad,
                       region=region,pais=pais,codigopostal=codigopostal,idcodigoempleadoventas=idcodigoempleadoventas,limite_credito=limite_credito)
        session.add(nuevoCliente)
        session.commit()
        print("Cliente agregado correctamente")
        
    @staticmethod
    def modificarCliente(session,id_cliente,**kwargs):
        cliente=session.query(Cliente).filter_by(idcliente=id_cliente).first()
        if cliente:
            for key, value in kwargs.items():
                setattr(cliente,key,value)
            session.commit()
            print("Cliente actualizado")
        else:
            print("Cliente no encontrada")
            
    @staticmethod
    def eliminarCliente (session,id_cliente):
        cliente=session.query(Cliente).filter_by(idcliente=id_cliente).first()
        if cliente:
            session.delete(cliente)
            session.commit()
            print("Cliente eliminado")
        else:
            print("Cliente no encontrado")



class Pedido(Base):
    __tablename__ = 'pedido'
    idpedido = Column(Integer, primary_key=True)
    codigopedido = Column(Integer, unique=True, nullable=False)
    fechapedido = Column(Date, nullable=False)
    fechaesperada = Column(Date, nullable=False)
    fechaentrega = Column(Date)
    estado = Column(String(20), nullable=False)
    comentarios = Column(Text)
    idcliente = Column(Integer, ForeignKey('cliente.idcliente'), nullable=False)
    totalpedido = Column(Numeric(15,2), nullable=False)
    idempleado = Column(Integer, ForeignKey('empleado.idempleado'), nullable=False)


    
    empleado = relationship("Empleado", backref="pedido")
    cliente = relationship("Cliente")  # Relación con la tabla cliente

    def _repr_(self):
        return (f"<pedido id={self.idpedido}, codigopedido={self.codigopedido}, fechapedido={self.fechapedido}, "
                f"fechaesperada={self.fechaesperada}, fechaentrega={self.fechaentrega}, estado={self.estado}, "
                f"totalpedido={self.totalpedido}>")

    @staticmethod
    def agregarPedido(session, codigopedido, fechapedido, fechaesperada, estado, idempleado, idcliente, totalpedido, fechaentrega=None, comentarios=None):
        nuevo_pedido = Pedido(
            codigopedido=codigopedido,
            fechapedido=fechapedido,
            fechaesperada=fechaesperada,
            fechaentrega=fechaentrega,
            estado=estado,
            comentarios=comentarios,
            idempleado=idempleado,
            idcliente=idcliente,
            totalpedido=totalpedido
        )
        session.add(nuevo_pedido)
        session.commit()
        print("Nuevo Pedido agregado")

    @staticmethod
    def modificarPedido(session, idpedido, **kwargs):
        pedido = session.query(Pedido).filter_by(idpedido=idpedido).first()
        if pedido:
            for key, value in kwargs.items():
                setattr(pedido, key, value)
            session.commit()
            print("Pedido modificado")
        else:
            print("No existe el Pedido")

    @staticmethod
    def eliminarPedido(session, idpedido):
        pedido = session.query(Pedido).filter_by(idpedido=idpedido).first()
        if pedido:
            session.delete(pedido)
            session.commit()
            print("Pedido eliminado")
        else:
            print("No existe el Pedido")



class DetallePedido(Base):
    __tablename__ = 'detallepedido'
    iddetallepedido = Column(Integer, primary_key=True)
    idpedido = Column(Integer, ForeignKey('pedido.idpedido'), nullable=False)
    idproducto = Column(Integer, ForeignKey('producto.idproducto'), nullable=False)
    cantidad = Column(Integer, nullable=False)
    preciounidad = Column(Numeric(15,2), nullable=False)
    numerolinea = Column(Integer, nullable=False)
    def __repr__(self):
        return f"<DetallePedido(id={self.iddetallepedido}, pedido={self.idpedido}, producto={self.idproducto})>"


    @staticmethod
    def agregar_detallepedido(session, idpedido, idproducto, cantidad, preciounidad, numerolinea):
        nuevo_detallepedido = DetallePedido(idpedido=idpedido, idproducto=idproducto, cantidad=cantidad, preciounidad=preciounidad, numerolinea=numerolinea)
        session.add(nuevo_detallepedido)
        session.commit()
        print("Detalle pedido agregado con exito")
    @staticmethod
    def modificar_detallepedido(session, iddetallepedido, **kwargs):
        detallepedido = session.query(DetallePedido).filter_by(iddetallepedido=iddetallepedido).first()
        if detallepedido:
            for key, value in kwargs.items():
                setattr(detallepedido, key, value)
            session.commit()
            print("Detalle pedido modificado con exito")
        else:
            print("No existe el detalle pedido")
    @staticmethod
    def eliminar_detallepedido(session, iddetallepedido):
        detallepedido = session.query(DetallePedido).filter_by(iddetallepedido=iddetallepedido).first()
        if detallepedido:
            session.delete(detallepedido)
            session.commit()
            print("Detalle pedido eliminado con exito")
        else:
            print("No existe el detalle pedido")


