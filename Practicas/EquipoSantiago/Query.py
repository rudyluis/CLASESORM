from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from datetime import date
from ORM import Vuelo, Asiento, Pasajero, Reserva

# Configura la conexión
engine = create_engine('postgresql://postgres:123456@localhost:5432/reserva_vuelos_bkp2025')
Session = sessionmaker(bind=engine)
session = Session()

# -------------------------------
# 1. Crear y cancelar reservas
# -------------------------------

print("🛬 1. Crear y cancelar reservas")

# Crear reserva
Reserva.crear_reserva(session, 1, 1)
print("✅ Reserva creada")

# Cancelar reserva
reserva_cancelar = session.query(Reserva).filter_by(idreserva=1).first()
if reserva_cancelar:
    session.delete(reserva_cancelar)
    session.commit()
    print("❌ Reserva cancelada")
else:
    print("⚠️ No se encontró la reserva para cancelar")

# -------------------------------
# 2. Mostrar vuelos por destino y rango de fechas
# -------------------------------

print("\n📍 2. Mostrar vuelos por destino y rango de fechas")

inicio = date(2025, 5, 19)
fin = date(2025, 5, 21)
destino = "La Paz"

vuelos = session.query(Vuelo).filter(
    Vuelo.destino == destino,
    Vuelo.fecha.between(inicio, fin)
).all()

print(f"Vuelos a {destino} entre {inicio} y {fin}:")
for vuelo in vuelos:
    print(f"- Vuelo {vuelo.numero} desde {vuelo.origen} el {vuelo.fecha}")

# -------------------------------
# 3. Consultar asientos libres y ocupados para un vuelo
# -------------------------------

print("\n💺 3. Consultar asientos libres y ocupados")

vuelo_consulta = "V001"

asientos = session.query(
    Asiento.numero,
    func.coalesce(Pasajero.nombre, "Libre").label("estado")
).join(Vuelo).outerjoin(Reserva).outerjoin(Pasajero).filter(
    Vuelo.numero == vuelo_consulta
).order_by(Asiento.numero).all()

print(f"Estado de los asientos del vuelo {vuelo_consulta}:")
for num, estado in asientos:
    print(f"Asiento {num}: {'Ocupado por ' + estado if estado != 'Libre' else 'Libre'}")

session.close()
