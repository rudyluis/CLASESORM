from sqlalchemy import Column, Integer, String, ForeignKey, Date, Numeric, Text, Sequence, DateTime, SmallInteger,func

from sqlalchemy.orm import relationship, declarative_base

Base= declarative_base()

class Oficina(Base):
    __tablename__='oficina'
    idoficina= Column(Integer, primary_key=True)
    codigooficina=Column(String(10), unique=True, nullable=False)
    ciudad =Column(String(30), nullable=False)
    pais =Column(String(50), nullable=False)
    region =Column(String(50))
    codigopostal=Column(String(50), nullable=False)
    telefono=Column(String(20), nullable=False)
    lineadireccion1=Column(String(50), nullable=False)
    lineadireccion2=Column(String(50))
    empleado= relationship('Empleado', back_populates='oficina')
    def __repr__(self):
        return f"<Oficina(idoficina={self.idoficina}, codigooficina={self.codigooficina}, ciudad={self.ciudad}, pais={self.pais}, region={self.region}, codigopostal={self.codigopostal}, telefono={self.telefono}, lineadireccion1={self.lineadireccion1}, lineadireccion2={self.lineadireccion2})>"
    @staticmethod
    def mostrar_todas_las_oficinas(session):
        oficinas = session.query(Oficina).all()
        for oficina in oficinas:
            print("ID de Oficina:", oficina.idoficina)
            print("Código de Oficina:", oficina.codigooficina)
            print("Ciudad:", oficina.ciudad)
            print("País:", oficina.pais)
            print("Región:", oficina.region)
            print("Código Postal:", oficina.codigopostal)
            print("Teléfono:", oficina.telefono)
            print("Línea de Dirección 1:", oficina.lineadireccion1)
            print("Línea de Dirección 2:", oficina.lineadireccion2)
            print("-------------------------------------------")
    @staticmethod
    def mostrar_oficina_por_id(session, id_oficina):
        oficina= session.query(Oficina).filter(Oficina.idoficina== id_oficina).first()
        if oficina:
            print('OFICINA ENCONTRADA')
            print("ID de Oficina:", oficina.idoficina)
            print("Código de Oficina:", oficina.codigooficina)
            print("Ciudad:", oficina.ciudad)
            print("País:", oficina.pais)
            print("Región:", oficina.region)
            print("Código Postal:", oficina.codigopostal)
            print("Teléfono:", oficina.telefono)
            print("Línea de Dirección 1:", oficina.lineadireccion1)
            print("Línea de Dirección 2:", oficina.lineadireccion2)
            print("-------------------------------------------")
        else: 
            print('No existe la Oficina mencionada')
    @staticmethod
    def agregarOficina(session, codigooficina, ciudad, pais, codigopostal, telefono, lineadireccion1, lineadireccion2, region= None):
        nueva_oficina=Oficina(codigooficina=codigooficina, ciudad=ciudad, 
                              pais= pais, codigopostal= codigopostal, telefono= telefono, 
                              lineadireccion1=lineadireccion1, lineadireccion2=lineadireccion2, region=region)
        
        session.add(nueva_oficina)
        session.commit()
        print('Se agregado una nueva oficina')

    @staticmethod
    def modificarOficina(session, id_oficina, **kwargs):
        oficina= session.query(Oficina).filter_by(idoficina=id_oficina).first()
        if oficina:
            for key, value in kwargs.items():
                setattr(oficina, key,value)
            session.commit()
            print('Oficina Actualizada')
        else:
            print('oficina no encontrada')
    
    @staticmethod
    def eliminarOficina(session, id_oficina):
        oficina= session.query(Oficina).filter_by(idoficina=id_oficina).first()
        if oficina:
            session.delete(oficina)
            session.commit()
            print('Oficina Eliminada')
        else:
            print('Oficina no encontrada')

class Empleado(Base):
    __tablename__ = 'empleado'
    idempleado = Column(Integer, primary_key=True)
    codigo_empleado = Column(Integer, unique=True, nullable=False)
    nombre = Column(String(50), nullable=False)
    apellido1 = Column(String(50), nullable=False)
    apellido2 = Column(String(50))
    extension = Column(String(10), nullable=False)
    email = Column(String(100), nullable=False)
    idoficina= Column(Integer, ForeignKey('oficina.idoficina'), nullable=False)
    idempleadojefe= Column(Integer, ForeignKey('empleado.idempleado'))
    puesto = Column(String(50))
    
    oficina= relationship('Oficina', back_populates='empleado')
    jefe = relationship('Empleado', remote_side=[idempleado])

    @staticmethod
    def empleadoInfo(session):
        empleados = session.query(Empleado).all()
        for empleado in empleados:
            print("ID de Empleado:", empleado.idempleado)
            print("Código de Empleado:", empleado.codigo_empleado)
            print("Nombre:", empleado.nombre)
            print("Apellido 1:", empleado.apellido1)
            print("Apellido 2:", empleado.apellido2)
            print("Extensión:", empleado.extension)
            print("Email:", empleado.email)
            print("ID de Oficina:", empleado.idoficina)
            print("Puesto:", empleado.puesto)
            if empleado.jefe:
                print("ID del Jefe:", empleado.jefe.idempleado)
                print("Nombre del Jefe:", empleado.jefe.nombre)
            else:
                print("JEFE")
            print("--------------------------")
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

class GamaProducto(Base):
    __tablename__ = 'gamaproducto'
    idgamaproducto = Column(Integer, primary_key=True)
    gama = Column(String(50), nullable=True)
    descripciontexto = Column(String)  #
    descripcionhtml = Column(String)    #
    imagen = Column(String(256))   #
    @staticmethod
    def agregarGamaProducto(session, gama,descripciontexto, descripcionhtml=None,imagen=None):
        nuevaGama=GamaProducto(gama=gama,
                               descripciontexto=descripciontexto,
                                descripcionhtml=descripcionhtml,
                                imagen=imagen)
        session.add(nuevaGama)
        session.commit()
        print("Nueva Gama agregada exitosamente")

    @staticmethod
    def modificarGamaProducto(session,id_gamaproducto,**kwargs):
        gamaproducto=session.query(GamaProducto).filter_by(idgamaproducto=id_gamaproducto).first()
        if gamaproducto:
            for key, value in kwargs.items():
                setattr(gamaproducto,key,value)
            session.commit()
            print("Gama Actualizada")
        else:
            print("Gama no encontrada")

    @staticmethod
    def mostrar_todas_las_gamaProductos(session):
        gamaproductos = session.query(GamaProducto).all()
        for gamaproducto in gamaproductos:
            print("ID de gamaProducto:", gamaproducto.idgamaproducto)
            print("Nombres de la Gama Producto:", gamaproducto.gama)
            print("Descripcion en texto de la Gama Producto:", gamaproducto.descripciontexto)
            print("Descripcion en html de la Gama Producto:", gamaproducto.descripcionhtml)
            print("Imagen la Gama Producto:", gamaproducto.imagen)
            print("-------------------------------------------")

class Producto(Base):
    __tablename__ = 'producto'
    idproducto = Column(Integer, primary_key=True)
    codigo_producto = Column(String(15), nullable=False, unique=True)
    nombre = Column(String(70), nullable=False)
    idgamaproducto = Column(Integer, ForeignKey('gamaproducto.idgamaproducto'), nullable=False)  ###
    dimensiones = Column(String(25))
    proveedor = Column(String(50))
    descripcion = Column(String)  ####
    cantidadstock = Column(Integer, nullable=False)
    precioventa = Column(Numeric(15, 2), nullable=False)
    precioproveedor = Column(Numeric(15, 2))
    gama_producto = relationship('GamaProducto')
    @staticmethod
    def agregarProducto(session, codigo_producto, nombre, idgamaproducto, dimensiones, proveedor, descripcion, cantidad_stock, precio_proveedor, precio_venta):
        nuevoProducto = Producto(codigo_producto=codigo_producto, nombre=nombre, idgamaproducto=idgamaproducto, dimensiones=dimensiones, proveedor=proveedor, descripcion=descripcion, cantidadstock=cantidad_stock, precioproveedor=precio_proveedor, precioventa=precio_venta)
        session.add(nuevoProducto)
        session.commit()
        print('Producto agregado correctamente')

    # Añadir el método modificarProducto para modificar un producto existente
    @staticmethod
    def modificarProducto(session, id_producto, **kwargs):
        producto = session.query(Producto).filter_by(idproducto=id_producto).first()
        if producto:
            for key, value in kwargs.items():
                setattr(producto, key, value)
            session.commit()
            print('Producto actualizado')
        else:
            print('Producto no encontrado')

    # Método para eliminar un producto
    @staticmethod
    def eliminarProducto(session, id_producto):
        producto = session.query(Producto).filter_by(idproducto=id_producto).first()
        if producto:
            session.delete(producto)
            session.commit()
            print('Producto eliminado')
        else:
            print('Producto no encontrado')


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

    ###empleadoventas= relationship('Empleado', backref="cliente")
    empleadoventas= relationship('Empleado')
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
    codigopedido = Column(String(10),  nullable=False)
    fechapedido = Column(Date, nullable=False)  ##
    fechaesperada = Column(Date, nullable=False)  ##
    fechaentrega = Column(Date)   ##
    estado = Column(String(15), nullable=False)
    comentarios = Column(String)
    idcliente = Column(Integer, ForeignKey('cliente.idcliente'), nullable=False)
    cliente = relationship("Cliente")   ###
    @staticmethod
    def mostrar_todos_los_pedidos(session):
        pedidos = session.query(Pedido).all()
        for pedido in pedidos:
            print("ID de Pedido:", pedido.idpedido)
            print("Código de Pedido:", pedido.codigopedido)
            print("Fecha de Pedido:", pedido.fecha_pedido)
            print("Fecha Esperada:", pedido.fecha_esperada)
            print("Fecha de Entrega:", pedido.fecha_entrega)
            print("Estado:", pedido.estado)
            print("Comentarios:", pedido.comentarios)
            print("ID de Cliente:", pedido.idcliente)
            print("------------------------------------------")
    @staticmethod
    def agregar_pedido(session, codigopedido, fechapedido, fechaesperada, estado, idcliente, fechaentrega=None, comentarios=None):
        nuevo_pedido = Pedido(codigopedido=codigopedido, fechapedido=fechapedido, fechaesperada=fechaesperada, estado=estado, idcliente=idcliente, fechaentrega=fechaentrega, comentarios=comentarios)
        session.add(nuevo_pedido)
        session.commit()
        print("Pedido agregado correctamente")
    @staticmethod
    def modificar_pedido(session, idpedido, **kwargs):
        pedido = session.query(Pedido).filter_by(idpedido=idpedido).first()
        if pedido:
           for key, value in kwargs.items():
              setattr(pedido, key, value)
              session.commit()
              print("Pedido actualizado")
        else:
            print("Pedido no encontrado")
    @staticmethod
    def eliminar_pedido(session, idpedido):
        pedido = session.query(Pedido).filter_by(idpedido=idpedido).first()
        if pedido:
            session.delete(pedido)
            session.commit()
            print("Pedido eliminado correctamente")
        else:
            print("Pedido no encontrado")

class DetallePedido(Base):
    __tablename__ = 'detallepedido'
    iddetallepedido = Column(Integer, primary_key=True, nullable=False)
    idproducto = Column(Integer, ForeignKey('producto.idproducto'),nullable=False)
    idpedido = Column(Integer, ForeignKey('pedido.idpedido'),nullable=False)
    cantidad = Column(Integer,nullable=False)
    preciounidad = Column(Numeric(15,2),nullable=False)
    numerolinea = Column(Integer,nullable=False)
    pedido = relationship("Pedido")
    producto = relationship("Producto")
    
    @staticmethod
    def agregarDetallePedido(session,  id_pedido, id_producto, cantidad, precio_unidad, numero_linea):
        nuevoDetallePedido = DetallePedido(idpedido = id_pedido, idproducto = id_producto, cantidad= cantidad, preciounidad = precio_unidad, numerolinea= numero_linea)
        session.add(nuevoDetallePedido)
        session.commit()
        print('Detalle de pedido agregado correctamente')

    @staticmethod
    def modificarDetallePedido(session, id_detalle_pedido, **kwargs):
        detallepedido = session.query(DetallePedido).filter_by(iddetallepedido= id_detalle_pedido).first()
        if detallepedido :
            for key, value in kwargs.items():
                setattr(detallepedido, key, value)
            session.commit()
            print('Detalle de pedido actualizado')
        else:
            print('Detalle de pedido no encontrado')

    @staticmethod
    def eliminarDetallePedido(session, id_detalle_pedido):
        detallepedido = session.query(DetallePedido).filter_by(iddetallepedido = id_detalle_pedido).first()
        if detallepedido:
            session.delete(detallepedido)
            session.commit()
            print('Detalle de pedido eliminado correctamente')
        else:
            print('No existe ese Detalle de pedido')

class Pago(Base):
    __tablename__ = 'pago'
    idpago =Column(Integer,primary_key=True)
    idcliente = Column(Integer,ForeignKey('cliente.idcliente'), nullable=False)  ###
    formapago = Column(String(40),nullable=False)
    nrotransaccion = Column(String(50),nullable=False)
    fechapago = Column(Date,nullable=False)
    total = Column(Numeric(15,2),nullable=False)
    cliente=relationship("Cliente")

    @staticmethod 
    def agregarPago(session, idcliente,formapago,nrotransaccion,fechapago,total): 
        nuevoPago=Pago(idcliente=idcliente, formapago = formapago, nrotransaccion = nrotransaccion, fechapago = fechapago, 
                           total = total) 
        session.add(nuevoPago) 
        session.commit() 
        print("Pago agregado correctamente") 
    @staticmethod 
    def modificarPago(session,id_pago,**kwargs):# kwargs para n funciones 
        pago=session.query(Pago).filter_by(idpago=id_pago).first() 
        if pago: 
            for key,value in kwargs.items(): 
                setattr(pago,key,value) 
                session.commit() 
            print('Pago actualizado ') 
        else: 
            print('Pago no encontrado')  
    @staticmethod 
    def eliminarPago(session,id_pago): 
        pago=session.query(Pago).filter_by(idpago=id_pago).first() 
        if pago: 
            session.delete(pago) 
            session.commit() 
            print('El pago fue eliminado') 
        else: 
            print('No se encontro el pago') 
    

class EmpleadoPlanilla(Base):
    __tablename__ = 'empleado_planilla'
    id_planilla_empleado = Column(Integer, primary_key=True)
    id_planilla = Column(Integer,  nullable=False)
    id_empleado = Column(Integer, ForeignKey('empleado.idempleado'), nullable=False)
    sueldo_basico = Column(Numeric(18,2), nullable=False)
    bono_ventas = Column(Numeric(18,2), nullable=False)
    bono_antiguedad = Column(Numeric(18,2), nullable=False)
    gestora_publica= Column(Numeric(18,2), nullable=False)
    mes = Column(String(50), nullable=False)
    gestion = Column(String(50), nullable=False)
    sueldo_total = Column(Numeric(18,2), nullable=False)
    sueldo_neto = Column(Numeric(18,2), nullable=False)
    Empleado = relationship("Empleado")
    def _repr_(self): 
        return f"<empleado_planilla id={self.id_planilla_empleado}, id_planilla={self.id_planilla},id_empleado={self.id_empleado}, sueldo_basico={self.sueldo_basico}, bono_ventas={self.bono_ventas}, bono_antiguedad={self.bono_antiguedad}, gestora_publica={self.gestora_publica}, mes={self.mes}, gestion={self.gestion}, sueldo_total={self.sueldo_total}, sueldo_neto={self.sueldo_neto}>"
    
    @staticmethod
    def agregarplanilla(session, id_planilla, id_empleado, sueldo_basico, bono_ventas, bono_antiguedad, gestora_publica, mes, gestion, sueldo_total, sueldo_neto):
        nueva_planilla = empleado_planilla(id_planilla, id_empleado, sueldo_basico, bono_ventas, bono_antiguedad, gestora_publica, mes, gestion, sueldo_total, sueldo_neto)
        session.add(nueva_planilla)
        session.commit()
        print("Nueva Planilla agregada")
    
    @staticmethod
    def modificar_planilla(session, id_planilla_empleado, **kwargs):
        planilla_modificada = session.query(empleado_planilla).filter_by(id_planilla_empleado=id_planilla_empleado).first()
        if planilla_modificada:
            for key, value in kwargs.items():
                setattr(planilla_modificada, key, value)
            session.commit()
            print("Planilla modificada")
        else:
            print("No existe la Planilla")
    
    @staticmethod
    def eliminar_planilla(session, id_planilla_empleado):
        planilla_eliminada = session.query(empleado_planilla).filter_by(id_planilla_empleado=id_planilla_empleado).first()
        if planilla_eliminada:
            session.delete(planilla_eliminada)
            session.commit()
            print("Planilla eliminada")
        else:
            print("No existe la Planilla")

class EmpleadoSueldo(Base):
    __tablename__ = "empleado_sueldo"

    idempleadosueldo = Column(Integer, primary_key=True, autoincrement=True)
    idempleado = Column(Integer, ForeignKey("empleado.idempleado", ondelete="CASCADE"), nullable=False)
    sueldo = Column(Numeric(18, 2), nullable=False)

    empleado = relationship("Empleado")

    def __repr__(self):
        return f"<EmpleadoSueldo(idempleado={self.idempleado}, sueldo={self.sueldo})>"

    @staticmethod
    def agregar_sueldo(session, idempleado, sueldo):
        nuevo_sueldo = EmpleadoSueldo(idempleado=idempleado, sueldo=sueldo)
        session.add(nuevo_sueldo)
        session.commit()
        print("Nuevo sueldo agregado")

    @staticmethod
    def modificar_sueldo(session, idempleadosueldo, **kwargs):
        sueldo = session.query(EmpleadoSueldo).filter_by(idempleadosueldo=idempleadosueldo).first()
        if sueldo:
            for key, value in kwargs.items():
                setattr(sueldo, key, value)
            session.commit()
            print("Sueldo modificado")
        else:
            print("No existe el sueldo")
            
    @staticmethod
    def eliminar_sueldo(session, idempleadosueldo):
        sueldo = session.query(EmpleadoSueldo).filter_by(idempleadosueldo=idempleadosueldo).first()
        if sueldo:
            session.delete(sueldo)
            session.commit()
            print("Sueldo eliminado")
        else:
            print("No existe el sueldo")

class ComisionVendedor(Base):
    __tablename__ = "comision_vendedor"

    idcomision = Column(Integer, primary_key=True, autoincrement=True)
    idpedido = Column(Integer, ForeignKey("pedido.idpedido"), nullable=False)
    idcodigoempleadoventas = Column(Integer, ForeignKey("empleado.idempleado"), nullable=False)
    totalventa = Column(Numeric(15, 2), nullable=False)
    porcentajecomision = Column(Numeric(5, 2), nullable=False)
    comisioncalculada = Column(Numeric(15, 2), nullable=False)
    fecharegistro = Column(DateTime, default=func.now())

    pedido = relationship("Pedido")
    empleado = relationship("Empleado")

    def __repr__(self):
        return f"<ComisionVendedor(idcomision={self.idcomision}, idpedido={self.idpedido}, idcodigoempleadoventas={self.idcodigoempleadoventas}, totalventa={self.totalventa}, porcentajecomision={self.porcentajecomision}, comisioncalculada={self.comisioncalculada}, fecharegistro={self.fecharegistro})>"

    @staticmethod
    def agregar_comision(session, idpedido, idcodigoempleadoventas, totalventa, porcentajecomision):
        nueva_comision = ComisionVendedor(idpedido=idpedido, idcodigoempleadoventas=idcodigoempleadoventas, totalventa=totalventa, porcentajecomision=porcentajecomision)
        session.add(nueva_comision)
        session.commit()
        print("Nueva comisión agregada")
        
    @staticmethod
    def modificar_comision(session, idcomision, **kwargs):
        comision = session.query(ComisionVendedor).filter_by(idcomision=idcomision).first()
        if comision:
            for key, value in kwargs.items():
                setattr(comision, key, value)
            session.commit()
            print("Comisión modificada")
        else:
            print("No existe la comisión")

    @staticmethod
    def eliminar_comision(session, idcomision):
        comision = session.query(ComisionVendedor).filter_by(idcomision=idcomision).first()
        if comision:
            session.delete(comision)
            session.commit()
            print("Comisión eliminada")
        else:
            print("No existe la comisión")


class SystemLog(Base):
    __tablename__ = "system_log"

    log_id = Column(Integer, primary_key=True, autoincrement=True)
    log_timestamp = Column(DateTime, default=func.now())
    log_usuario = Column(String, default=func.current_user())
    log_level = Column(String(10), nullable=False)
    log_message = Column(Text, nullable=False)
    
    def __repr__(self):
        return f"<SystemLog(log_id={self.log_id}, log_timestamp={self.log_timestamp}, log_usuario={self.log_usuario}, log_level={self.log_level}, log_message={self.log_message})>"

    @staticmethod
    def agregar_log(session, log_level, log_message):
        nuevo_log = SystemLog(log_level=log_level, log_message=log_message)
        session.add(nuevo_log)
        session.commit()
        print("Nuevo log agregado")

    @staticmethod
    def eliminar_log(session, log_id):
        log = session.query(SystemLog).filter_by(log_id=log_id).first()
        if log:
            session.delete(log)
            session.commit()
            print("Log eliminado")
        else:
            print("No existe el log")       

class Inventario(Base):
    __tablename__ = "inventario"

    idinventario = Column(Integer, primary_key=True, autoincrement=True)
    idproducto = Column(Integer, ForeignKey("producto.idproducto"), nullable=False)
    fechamovimiento = Column(Date, nullable=False)
    tipomovimiento = Column(String(20), nullable=False)
    cantidad = Column(Integer, nullable=False)
    comentario = Column(Text, nullable=True)
    Producto= relationship("Producto")
    def __repr__(self):
        return f"<Inventario(idinventario={self.idinventario}, idproducto={self.idproducto}, fechamovimiento={self.fechamovimiento}, tipomovimiento={self.tipomovimiento}, cantidad={self.cantidad}, comentario={self.comentario})>"

    @staticmethod
    def agregar_inventario(session, idproducto, fechamovimiento, tipomovimiento, cantidad, comentario=None):
        nuevo_inventario = Inventario(idproducto=idproducto, fechamovimiento=fechamovimiento, tipomovimiento=tipomovimiento, cantidad=cantidad, comentario=comentario)
        session.add(nuevo_inventario)
        session.commit()
        print("Nuevo inventario agregado")

    @staticmethod
    def modificar_inventario(session, idinventario, **kwargs):
        inventario = session.query(Inventario).filter_by(idinventario=idinventario).first()
        if inventario:
            for key, value in kwargs.items():
                setattr(inventario, key, value)
            session.commit()
            print("Inventario modificado")
        else:
            print("No existe el inventario")

    @staticmethod
    def eliminar_inventario(session, idinventario):
        inventario = session.query(Inventario).filter_by(idinventario=idinventario).first()
        if inventario:
            session.delete(inventario)
            session.commit()
            print("Inventario eliminado")
        else:
            print("No existe el inventario")


def filtro_generico(session, tabla):
    registro = session.query(tabla).all()

    #Devolver registro en diccionario
    registro_diccionario = [{columna: getattr(registro, columna) for columna in registro.__table__.columns.keys()} for registro in registro]

    return registro_diccionario
    

def mostrar_datos(session, modelo_o_resultados, campos=None):
    from sqlalchemy.inspection import inspect

    if isinstance(modelo_o_resultados, list):
        resultados = modelo_o_resultados
        modelo = resultados[0].__class__ if resultados else None
    else:
        modelo = modelo_o_resultados
        
        resultados = session.query(modelo).all()

    
    if campos is None and modelo:
        campos = [c.key for c in inspect(modelo).mapper.column_attrs]
    elif campos is None:
        raise ValueError(
            "No se proporcionaron campos y no se pudo inferir el modelo")

    
    for item in resultados:
        datos = [f"{campo}: {getattr(item, campo)}" for campo in campos]
        print(", ".join(datos))


def filtro_busqueda_generico(session, nombre_tabla, nombre_id, valor_buscar):
    # Consultar la tabla y filtrar por el nombre_id y valor_buscar
    registros = session.query(nombre_tabla).filter_by(**{nombre_id: valor_buscar}).all()
    
    # Verificar si se encontraron registros
    if registros:
        # Devolver los registros como una lista de diccionarios
        registros_dict = [{columna: getattr(registro, columna) for columna in registro.__table__.columns.keys()} for registro in registros]
        return registros_dict
    else:
        print("No se encontraron registros.")
        return None


def filtro_multiple(session, nombre_tabla, filtros):
    """
    Filtra registros usando múltiples condiciones dinámicas.

    filtros: diccionario de columna: valor
    """
    query = session.query(nombre_tabla)
    for campo, valor in filtros.items():
        query = query.filter(getattr(nombre_tabla, campo) == valor)
    registros = query.all()
    registros_dict = [{columna: getattr(registro, columna) for columna in registro.__table__.columns.keys()} for registro in registros]
    return registros_dict