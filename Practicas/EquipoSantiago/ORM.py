from sqlalchemy import Column, Integer, String, Date, ForeignKey, Boolean
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime

Base = declarative_base()

class Vuelo(Base):
    __tablename__ = 'vuelo'
    idvuelo = Column(Integer, primary_key=True)
    numero = Column(String(10), unique=True, nullable=False)
    origen = Column(String(50), nullable=False)
    destino = Column(String(50), nullable=False)
    fecha = Column(Date, nullable=False)
    capacidad = Column(Integer, nullable=False)

    asientos = relationship("Asiento", back_populates="vuelo", cascade="all, delete-orphan")
    reservas = relationship("Reserva", back_populates="vuelo", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Vuelo({self.numero}, {self.origen} -> {self.destino} el {self.fecha})>"

    @staticmethod
    def buscar_vuelos(session, destino, fecha_inicio, fecha_fin):
        vuelos = session.query(Vuelo).filter(
            Vuelo.destino == destino,
            Vuelo.fecha >= fecha_inicio,
            Vuelo.fecha <= fecha_fin
        ).all()
        return vuelos

    @staticmethod
    def mostrar_asientos(session, idvuelo):
        vuelo = session.query(Vuelo).filter_by(idvuelo=idvuelo).first()
        if vuelo:
            libres = [a.numero for a in vuelo.asientos if not a.ocupado]
            ocupados = [a.numero for a in vuelo.asientos if a.ocupado]
            print(f"Asientos libres: {libres}")
            print(f"Asientos ocupados: {ocupados}")
        else:
            print("Vuelo no encontrado")

class Pasajero(Base):
    __tablename__ = 'pasajero'
    idpasajero = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)

    reservas = relationship("Reserva", back_populates="pasajero", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Pasajero({self.nombre})>"

class Asiento(Base):
    __tablename__ = 'asiento'
    idasiento = Column(Integer, primary_key=True)
    numero = Column(Integer, nullable=False)
    ocupado = Column(Boolean, default=False)

    idvuelo = Column(Integer, ForeignKey('vuelo.idvuelo'))
    vuelo = relationship("Vuelo", back_populates="asientos")
    reserva = relationship("Reserva", back_populates="asiento", uselist=False)

    def __repr__(self):
        return f"<Asiento({self.numero}, ocupado={self.ocupado})>"

class Reserva(Base):
    __tablename__ = 'reserva'
    idreserva = Column(Integer, primary_key=True)
    
    idpasajero = Column(Integer, ForeignKey('pasajero.idpasajero'))
    pasajero = relationship("Pasajero", back_populates="reservas")
    
    idvuelo = Column(Integer, ForeignKey('vuelo.idvuelo'))
    vuelo = relationship("Vuelo", back_populates="reservas")

    idasiento = Column(Integer, ForeignKey('asiento.idasiento'))
    asiento = relationship("Asiento", back_populates="reserva")

    def __repr__(self):
        return f"<Reserva(Pasajero={self.pasajero.nombre}, Vuelo={self.vuelo.numero}, Asiento={self.asiento.numero})>"

    @staticmethod
    def crear_reserva(session, idpasajero, idvuelo):
        vuelo = session.query(Vuelo).filter_by(idvuelo=idvuelo).first()
        pasajero = session.query(Pasajero).filter_by(idpasajero=idpasajero).first()

        if not vuelo or not pasajero:
            print("Vuelo o pasajero no encontrado.")
            return

        asiento_libre = next((a for a in vuelo.asientos if not a.ocupado), None)

        if asiento_libre:
            asiento_libre.ocupado = True
            nueva_reserva = Reserva(pasajero=pasajero, vuelo=vuelo, asiento=asiento_libre)
            session.add(nueva_reserva)
            session.commit()
            print(f"Reserva realizada para {pasajero.nombre} en asiento {asiento_libre.numero}.")
        else:
            print("No hay asientos disponibles en este vuelo.")

    @staticmethod
    def cancelar_reserva(session, idreserva):
        reserva = session.query(Reserva).filter_by(idreserva=idreserva).first()
        if reserva:
            reserva.asiento.ocupado = False
            session.delete(reserva)
            session.commit()
            print("Reserva cancelada.")
        else:
            print("Reserva no encontrada.")