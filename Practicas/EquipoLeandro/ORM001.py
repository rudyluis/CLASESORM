from sqlalchemy import Column, Integer, String, ForeignKey, Numeric, Text, DateTime, func
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()


class Marca(Base):
    __tablename__ = 'marcas'
    id_marca = Column(Integer, primary_key=True)
    nombre_marca = Column(String(100), unique=True, nullable=False)
    productos = relationship('Producto', back_populates='marca')

    def __repr__(self):
        return f"<Marca(id_marca={self.id_marca}, nombre_marca={self.nombre_marca})>"

    @staticmethod
    def agregar_marca(session, nombre_marca):
        nueva_marca = Marca(nombre_marca=nombre_marca)
        session.add(nueva_marca)
        session.commit()
        print('Nueva marca agregada')

    @staticmethod
    def mostrar_todas_marcas(session):
        marcas = session.query(Marca).all()
        for marca in marcas:
            print("ID Marca:", marca.id_marca)
            print("Nombre Marca:", marca.nombre_marca)
            print("-------------------")

    @staticmethod
    def actualizar_marca(session, id_marca, nombre_marca):
        marca = session.query(Marca).filter_by(id_marca=id_marca).first()
        if marca:
            marca.nombre_marca = nombre_marca
            session.commit()
            print('Marca actualizada')
        else:
            print('Marca no encontrada')

    @staticmethod
    def eliminar_marca(session, id_marca):
        marca = session.query(Marca).filter_by(id_marca=id_marca).first()
        if marca:
            session.delete(marca)
            session.commit()
            print('Marca eliminada')
        else:
            print('Marca no encontrada')


class Categoria(Base):
    __tablename__ = 'categorias'
    id_categoria = Column(Integer, primary_key=True)
    nombre_categoria = Column(String(50), unique=True, nullable=False)
    productos = relationship('Producto', back_populates='categoria')

    def __repr__(self):
        return f"<Categoria(id_categoria={self.id_categoria}, nombre_categoria={self.nombre_categoria})>"

    @staticmethod
    def agregar_categoria(session, nombre_categoria):
        nueva_categoria = Categoria(nombre_categoria=nombre_categoria)
        session.add(nueva_categoria)
        session.commit()
        print('Nueva categoría agregada')

    @staticmethod
    def mostrar_todas_categorias(session):
        categorias = session.query(Categoria).all()
        for categoria in categorias:
            print("ID Categoría:", categoria.id_categoria)
            print("Nombre Categoría:", categoria.nombre_categoria)
            print("-------------------")

    @staticmethod
    def actualizar_categoria(session, id_categoria, nombre_categoria):
        categoria = session.query(Categoria).filter_by(
            id_categoria=id_categoria).first()
        if categoria:
            categoria.nombre_categoria = nombre_categoria
            session.commit()
            print('Categoría actualizada')
        else:
            print('Categoría no encontrada')

    @staticmethod
    def eliminar_categoria(session, id_categoria):
        categoria = session.query(Categoria).filter_by(
            id_categoria=id_categoria).first()
        if categoria:
            session.delete(categoria)
            session.commit()
            print('Categoría eliminada')
        else:
            print('Categoría no encontrada')


class Producto(Base):
    __tablename__ = 'productos'
    id_producto = Column(Integer, primary_key=True)
    id_categoria = Column(Integer, ForeignKey(
        'categorias.id_categoria'), nullable=False)
    id_marca = Column(Integer, ForeignKey('marcas.id_marca'), nullable=False)
    modelo = Column(String(100), nullable=False)
    precio = Column(Numeric(10, 2), nullable=False)
    descripcion = Column(Text)
    fecha_creacion = Column(DateTime, server_default=func.current_timestamp())
    categoria = relationship('Categoria', back_populates='productos')
    marca = relationship('Marca', back_populates='productos')
    inventario = relationship(
        'Inventario', uselist=False, back_populates='producto')
    ventas = relationship('Venta', back_populates='producto')

    def __repr__(self):
        return f"<Producto(id_producto={self.id_producto}, modelo={self.modelo}, precio={self.precio})>"

    @staticmethod
    def agregar_producto(session, id_categoria, id_marca, modelo, precio, descripcion=None):
        nuevo_producto = Producto(id_categoria=id_categoria, id_marca=id_marca, modelo=modelo,
                                  precio=precio, descripcion=descripcion)
        session.add(nuevo_producto)
        session.commit()
        print('Nuevo producto agregado')
        return nuevo_producto.id_producto

    @staticmethod
    def mostrar_todos_productos(session):
        productos = session.query(Producto).all()
        for producto in productos:
            print("ID Producto:", producto.id_producto)
            print("Categoría:", producto.categoria.nombre_categoria)
            print("Marca:", producto.marca.nombre_marca)
            print("Modelo:", producto.modelo)
            print("Precio:", producto.precio)
            print("Descripción:", producto.descripcion)
            print("Fecha Creación:", producto.fecha_creacion)
            print("-------------------")

    @staticmethod
    def actualizar_producto(session, id_producto, **kwargs):
        producto = session.query(Producto).filter_by(
            id_producto=id_producto).first()
        if producto:
            for key, value in kwargs.items():
                setattr(producto, key, value)
            session.commit()
            print('Producto actualizado')
        else:
            print('Producto no encontrado')

    @staticmethod
    def eliminar_producto(session, id_producto):
        producto = session.query(Producto).filter_by(
            id_producto=id_producto).first()
        if producto:
            session.delete(producto)
            session.commit()
            print('Producto eliminado')
        else:
            print('Producto no encontrado')


class Inventario(Base):
    __tablename__ = 'inventario'
    id_inventario = Column(Integer, primary_key=True)
    id_producto = Column(Integer, ForeignKey(
        'productos.id_producto'), nullable=False)
    stock = Column(Integer, nullable=False)
    ultima_actualizacion = Column(
        DateTime, server_default=func.current_timestamp())
    producto = relationship('Producto', back_populates='inventario')

    def __repr__(self):
        return f"<Inventario(id_inventario={self.id_inventario}, id_producto={self.id_producto}, stock={self.stock})>"

    @staticmethod
    def agregar_inventario(session, id_producto, stock):
        nuevo_inventario = Inventario(id_producto=id_producto, stock=stock)
        session.add(nuevo_inventario)
        session.commit()
        print('Nueva entrada de inventario agregada')

    @staticmethod
    def mostrar_inventario(session, id_producto=None):
        query = session.query(Inventario)
        if id_producto:
            query = query.filter_by(id_producto=id_producto)
        inventarios = query.all()
        for inventario in inventarios:
            print("ID Inventario:", inventario.id_inventario)
            print("Producto:", inventario.producto.modelo)
            print("Stock:", inventario.stock)
            print("Última Actualización:", inventario.ultima_actualizacion)
            print("-------------------")

    @staticmethod
    def actualizar_inventario(session, id_inventario, stock):
        inventario = session.query(Inventario).filter_by(
            id_inventario=id_inventario).first()
        if inventario:
            inventario.stock = stock
            inventario.ultima_actualizacion = func.current_timestamp()
            session.commit()
            print('Inventario actualizado')
        else:
            print('Inventario no encontrado')

    @staticmethod
    def eliminar_inventario(session, id_inventario):
        inventario = session.query(Inventario).filter_by(
            id_inventario=id_inventario).first()
        if inventario:
            session.delete(inventario)
            session.commit()
            print('Inventario eliminado')
        else:
            print('Inventario no encontrado')


class Venta(Base):
    __tablename__ = 'ventas'
    id_venta = Column(Integer, primary_key=True)
    id_producto = Column(Integer, ForeignKey(
        'productos.id_producto'), nullable=False)
    cantidad = Column(Integer, nullable=False)
    precio_venta = Column(Numeric(10, 2), nullable=False)
    fecha_venta = Column(DateTime, server_default=func.current_timestamp())
    producto = relationship('Producto', back_populates='ventas')

    def __repr__(self):
        return f"<Venta(id_venta={self.id_venta}, id_producto={self.id_producto}, cantidad={self.cantidad})>"

    @staticmethod
    def agregar_venta(session, id_producto, cantidad, precio_venta):
        inventario = session.query(Inventario).filter_by(
            id_producto=id_producto).first()
        if inventario and inventario.stock >= cantidad:
            nueva_venta = Venta(id_producto=id_producto,
                                cantidad=cantidad, precio_venta=precio_venta)
            inventario.stock -= cantidad
            inventario.ultima_actualizacion = func.current_timestamp()
            session.add(nueva_venta)
            session.commit()
            print('Nueva venta agregada y inventario actualizado')
        else:
            print('Stock insuficiente o producto no encontrado')

    @staticmethod
    def mostrar_todas_ventas(session):
        ventas = session.query(Venta).all()
        for venta in ventas:
            print("ID Venta:", venta.id_venta)
            print("Producto:", venta.producto.modelo)
            print("Cantidad:", venta.cantidad)
            print("Precio Venta:", venta.precio_venta)
            print("Fecha Venta:", venta.fecha_venta)
            print("-------------------")

    @staticmethod
    def mostrar_ventas_por_producto(session, id_producto):
        ventas = session.query(Venta).filter_by(id_producto=id_producto).all()
        if ventas:
            for venta in ventas:
                print("ID Venta:", venta.id_venta)
                print("Producto:", venta.producto.modelo)
                print("Cantidad:", venta.cantidad)
                print("Precio Venta:", venta.precio_venta)
                print("Fecha Venta:", venta.fecha_venta)
                print("-------------------")
        else:
            print('No se encontraron ventas para este producto')
