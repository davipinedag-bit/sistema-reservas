from abc import ABC, abstractmethod
from datetime import datetime

# ===== EXCEPCIONES PERSONALIZADAS =====
class ErrorSistema(Exception):
    pass

class ErrorValidacion(ErrorSistema):
    pass

class ErrorReserva(ErrorSistema):
    pass

class ErrorServicioNoDisponible(ErrorSistema):
    pass


# ===== LOGS DETALLADOS =====
def registrar_log(tipo, mensaje, contexto=""):
    with open("logs.txt", "a", encoding="utf-8") as f:
        f.write(f"{datetime.now()} | {tipo} | {mensaje} | {contexto}\n")


# ===== CLASE ABSTRACTA GENERAL =====
class Entidad(ABC):
    @abstractmethod
    def mostrar_info(self):
        pass


# ===== CLIENTE =====
class Cliente(Entidad):
    def __init__(self, nombre):
        if not nombre or not nombre.strip():
            raise ErrorValidacion("Nombre de cliente inválido")
        self.nombre = nombre

    def mostrar_info(self):
        return f"Cliente: {self.nombre}"


# ===== SERVICIO ABSTRACTO =====
class Servicio(Entidad):
    def __init__(self, nombre, precio):
        if precio <= 0:
            raise ErrorValidacion("Precio inválido")
        self.nombre = nombre
        self.precio = precio

    @abstractmethod
    def calcular_costo(self, cantidad=1, impuesto=0, descuento=0):
        pass


# ===== SERVICIOS =====
class ServicioSala(Servicio):
    def calcular_costo(self, horas=1, impuesto=0, descuento=0):
        subtotal = self.precio * horas
        total = subtotal + (subtotal * impuesto) - descuento
        return total


class ServicioEquipo(Servicio):
    def calcular_costo(self, dias=1, impuesto=0, descuento=0):
        subtotal = self.precio * dias
        total = subtotal + (subtotal * impuesto) - descuento
        return total


class ServicioAsesoria(Servicio):
    def calcular_costo(self, horas=1, impuesto=0, descuento=0):
        subtotal = self.precio * horas
        total = subtotal + (subtotal * impuesto) - descuento
        return total


# ===== RESERVA =====
class Reserva:
    def __init__(self, cliente, servicio, duracion):
        if duracion <= 0:
            raise ErrorReserva("Duración inválida")
        self.cliente = cliente
        self.servicio = servicio
        self.duracion = duracion

    def procesar(self):
        try:
            if not self.servicio:
                raise ErrorServicioNoDisponible("Servicio no disponible")

            costo = self.servicio.calcular_costo(
                self.duracion,
                impuesto=0.19,
                descuento=10
            )

        except ErrorSistema as e:
            registrar_log("ERROR", str(e), "Reserva")
            print("Error controlado:", e)

        except Exception as e:
            registrar_log("ERROR_GENERAL", str(e), "Reserva")
            print("Error inesperado:", e)

        else:
            print(f"Reserva exitosa para {self.cliente.nombre} → Total: {costo}")

        finally:
            print("Proceso de reserva finalizado\n")


# ===== SISTEMA =====
class SistemaReservas:
    def __init__(self):
        self.clientes = []
        self.servicios = []
        self.reservas = []

    def agregar_cliente(self, nombre):
        try:
            cliente = Cliente(nombre)
            self.clientes.append(cliente)
        except ErrorSistema as e:
            registrar_log("ERROR", str(e), "Cliente")

    def agregar_servicio(self, servicio):
        self.servicios.append(servicio)

    def crear_reserva(self, cliente, servicio, duracion):
        try:
            reserva = Reserva(cliente, servicio, duracion)
            self.reservas.append(reserva)
            reserva.procesar()
        except ErrorSistema as e:
            registrar_log("ERROR", str(e), "Crear reserva")


# ===== SIMULACIÓN (10+ OPERACIONES) =====
def main():
    sistema = SistemaReservas()

    # Clientes
    sistema.agregar_cliente("Juan")
    sistema.agregar_cliente("Ana")
    sistema.agregar_cliente("")  # inválido
    sistema.agregar_cliente("Carlos")

    # Servicios
    sala = ServicioSala("Sala", 100)
    equipo = ServicioEquipo("Equipo", 50)
    asesoria = ServicioAsesoria("Asesoría", 80)

    sistema.agregar_servicio(sala)
    sistema.agregar_servicio(equipo)
    sistema.agregar_servicio(asesoria)

    # Reservas (válidas e inválidas)
    sistema.crear_reserva(sistema.clientes[0], sala, 2)
    sistema.crear_reserva(sistema.clientes[1], equipo, 3)
    sistema.crear_reserva(sistema.clientes[2] if len(sistema.clientes) > 2 else None, sala, 1)
    sistema.crear_reserva(sistema.clientes[0], None, 2)
    sistema.crear_reserva(sistema.clientes[1], asesoria, -1)
    sistema.crear_reserva(sistema.clientes[0], sala, 5)
    sistema.crear_reserva(sistema.clientes[1], equipo, 1)
    sistema.crear_reserva(sistema.clientes[0], asesoria, 2)
    sistema.crear_reserva(sistema.clientes[1], sala, 4)
    sistema.crear_reserva(sistema.clientes[0], equipo, 0)

    print("Sistema ejecutado correctamente")


if __name__ == "__main__":
    main()