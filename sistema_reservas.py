# Sistema de Gestión de Clientes, Servicios y Reservas

from abc import ABC, abstractmethod
import datetime

# ---------------- LOG ----------------
def registrar_log(mensaje):
    with open("logs.txt", "a") as archivo:
        archivo.write(f"{datetime.datetime.now()} - {mensaje}\n")

# ---------------- EXCEPCIONES ----------------
class ErrorSistema(Exception):
    pass

class ErrorValidacion(ErrorSistema):
    pass

class ErrorReserva(ErrorSistema):
    pass

# ---------------- CLIENTE ----------------
class Cliente:
    def __init__(self, nombre, documento):
        if not nombre or not documento:
            raise ErrorValidacion("Datos del cliente inválidos")
        self.__nombre = nombre
        self.__documento = documento

    def get_nombre(self):
        return self.__nombre

    def __str__(self):
        return f"Cliente: {self.__nombre}"

# ---------------- SERVICIO ABSTRACTO ----------------
class Servicio(ABC):
    def __init__(self, nombre):
        self.nombre = nombre

    @abstractmethod
    def calcular_costo(self):
        pass

    @abstractmethod
    def descripcion(self):
        pass

# ---------------- SERVICIOS ----------------
class ReservaSala(Servicio):
    def __init__(self, horas):
        super().__init__("Reserva de Sala")
        self.horas = horas

    def calcular_costo(self):
        if self.horas <= 0:
            raise ErrorValidacion("Horas inválidas")
        return self.horas * 50

    def descripcion(self):
        return f"{self.nombre} por {self.horas} horas"

class AlquilerEquipo(Servicio):
    def __init__(self, dias):
        super().__init__("Alquiler de Equipo")
        self.dias = dias

    def calcular_costo(self):
        if self.dias <= 0:
            raise ErrorValidacion("Días inválidos")
        return self.dias * 30

    def descripcion(self):
        return f"{self.nombre} por {self.dias} días"

class Asesoria(Servicio):
    def __init__(self, horas):
        super().__init__("Asesoría")
        self.horas = horas

    def calcular_costo(self):
        if self.horas <= 0:
            raise ErrorValidacion("Horas inválidas")
        return self.horas * 80

    def descripcion(self):
        return f"{self.nombre} por {self.horas} horas"

# ---------------- RESERVA ----------------
class Reserva:
    def __init__(self, cliente, servicio):
        self.cliente = cliente
        self.servicio = servicio
        self.estado = "Pendiente"

    def confirmar(self):
        try:
            costo = self.servicio.calcular_costo()
            self.estado = "Confirmada"
            return costo
        except Exception as e:
            registrar_log(f"Error al confirmar reserva: {e}")
            raise ErrorReserva("No se pudo confirmar la reserva")

    def cancelar(self):
        self.estado = "Cancelada"

    def __str__(self):
        return f"{self.cliente} - {self.servicio.descripcion()} - Estado: {self.estado}"

# ---------------- SIMULACIÓN ----------------
def simulacion():
    clientes = []
    reservas = []

    # 10 operaciones (válidas e inválidas)
    operaciones = [
        ("Juan", "123"),
        ("", "456"),
        ("Maria", "789"),
        ("Pedro", ""),
        ("Ana", "111"),
        ("Luis", "222"),
        ("", ""),
        ("Sofia", "333"),
        ("Carlos", "444"),
        ("Laura", "")
    ]        
    

    for nombre, doc in operaciones:
        try:
            cliente = Cliente(nombre, doc)
            clientes.append(cliente)
            print("Cliente creado:", cliente)
        except Exception as e:
            registrar_log(e)
            print("Error cliente:", e)

    servicios = [
        ReservaSala(2),
        AlquilerEquipo(3),
        Asesoria(1),
        ReservaSala(-1),  # error
        AlquilerEquipo(0)  # error
    ]

    for i in range(len(clientes)):
        try:
            servicio = servicios[i % len(servicios)]
            reserva = Reserva(clientes[i], servicio)
            costo = reserva.confirmar()
            reservas.append(reserva)
            print(reserva, "Costo:", costo)
        except Exception as e:
            registrar_log(e)
            print("Error reserva:", e)

    print("\n--- RESUMEN ---")
    for r in reservas:
        print(r)

# ---------------- MAIN ----------------
if __name__ == "__main__":
    simulacion()