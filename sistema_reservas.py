from abc import ABC, abstractmethod

# ===== LOGS =====
def registrar_log(mensaje):
    with open("logs.txt", "a") as archivo:
        archivo.write(mensaje + "\n")

# ===== CLASE ABSTRACTA GENERAL =====
class Entidad(ABC):
    @abstractmethod
    def mostrar_info(self):
        pass

# ===== CLIENTE =====
class Cliente(Entidad):
    def __init__(self, nombre):
        if not nombre:
            raise ValueError("El nombre no puede estar vacío")
        self.nombre = nombre

    def mostrar_info(self):
        return f"Cliente: {self.nombre}"

# ===== SERVICIO ABSTRACTO =====
class Servicio(Entidad):
    def __init__(self, nombre, precio):
        if precio <= 0:
            raise ValueError("El precio debe ser mayor a 0")
        self.nombre = nombre
        self.precio = precio

    @abstractmethod
    def calcular_costo(self, extra=0):
        pass

# ===== SERVICIOS =====
class ServicioSala(Servicio):
    def calcular_costo(self, horas=1):
        return self.precio * horas

class ServicioEquipo(Servicio):
    def calcular_costo(self, dias=1):
        return self.precio * dias

class ServicioAsesoria(Servicio):
    def calcular_costo(self, horas=1):
        return self.precio * horas

# ===== RESERVA =====
class Reserva:
    def __init__(self, cliente, servicio, duracion):
        if duracion <= 0:
            raise ValueError("Duración inválida")
        self.cliente = cliente
        self.servicio = servicio
        self.duracion = duracion

    def procesar_reserva(self):
        try:
            costo = self.servicio.calcular_costo(self.duracion)
        except TypeError:
            raise Exception("Error en cálculo de costo") from None
        else:
            return costo
        finally:
            print("Proceso de reserva finalizado")

# ===== SIMULACIÓN =====
def main():
    try:
        cliente1 = Cliente("Juan")
        cliente2 = Cliente("")  # error

        servicio1 = ServicioSala("Sala", 100)
        servicio2 = ServicioEquipo("Equipo", -50)  # error

        reserva1 = Reserva(cliente1, servicio1, 2)
        print("Costo:", reserva1.procesar_reserva())

        reserva2 = Reserva(cliente1, servicio1, -1)  # error

    except Exception as e:
        print("Error:", e)
        registrar_log(str(e))

    finally:
        print("Sistema finalizado")

if __name__ == "__main__":
    main()