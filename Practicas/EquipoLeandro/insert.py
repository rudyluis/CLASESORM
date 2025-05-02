from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ORM001 import Base, Marca, Categoria, Producto, Inventario, Venta

# Conexión a la base de datos
engine = create_engine(
    'postgresql+psycopg2://postgres:123456@localhost:5432/electronica01')
Session = sessionmaker(bind=engine)

# Crear las tablas si no existen
Base.metadata.create_all(engine)


def insert_sample_data():
    session = Session()
    try:
        # Insertar marcas
        Marca.agregar_marca(session, "Samsung")
        Marca.agregar_marca(session, "Apple")
        Marca.agregar_marca(session, "Sony")
        Marca.agregar_marca(session, "LG")

        # Insertar categorías
        Categoria.agregar_categoria(session, "Teléfono")
        Categoria.agregar_categoria(session, "Laptop")
        Categoria.agregar_categoria(session, "Televisor")
        Categoria.agregar_categoria(session, "Accesorio")

        # Insertar productos
        id_producto1 = Producto.agregar_producto(
            session,
            id_categoria=1,  # Teléfono
            id_marca=1,      # Samsung
            modelo="Galaxy S23",
            precio=799.99,
            descripcion="Smartphone 5G con 128GB"
        )

        id_producto2 = Producto.agregar_producto(
            session,
            id_categoria=2,  # Laptop
            id_marca=2,      # Apple
            modelo="MacBook Air M2",
            precio=1199.99,
            descripcion="Laptop con chip M2 y 256GB SSD"
        )

        id_producto3 = Producto.agregar_producto(
            session,
            id_categoria=3,  # Televisor
            id_marca=3,      # Sony
            modelo="Bravia 55X90J",
            precio=1299.99,
            descripcion="TV 4K LED de 55 pulgadas"
        )

        id_producto4 = Producto.agregar_producto(
            session,
            id_categoria=4,  # Accesorio
            id_marca=4,      # LG
            modelo="Auriculares TONE Free",
            precio=129.99,
            descripcion="Auriculares inalámbricos con cancelación de ruido"
        )

        # Insertar inventario
        Inventario.agregar_inventario(session, id_producto1, 50)
        Inventario.agregar_inventario(session, id_producto2, 30)
        Inventario.agregar_inventario(session, id_producto3, 20)
        Inventario.agregar_inventario(session, id_producto4, 100)

        # Insertar ventas
        Venta.agregar_venta(session, id_producto1, 5, 799.99)
        Venta.agregar_venta(session, id_producto2, 2, 1199.99)
        Venta.agregar_venta(session, id_producto4, 10, 129.99)

        session.commit()
        print("Datos de ejemplo insertados con éxito")

    except Exception as e:
        session.rollback()
        print(f"Error al insertar datos: {str(e)}")
    finally:
        session.close()


if __name__ == "__main__":
    insert_sample_data()
