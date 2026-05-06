import logging
import re
from abc import ABC, abstractmethod
from datetime import datetime

# =================================================================
# ESTUDIANTE 1: Jairo Alexis Camacho
# Excepciones Personalizadas y Logging
# =================================================================

# Configuración robusta de LOGS
logging.basicConfig(
    filename="gestion_errores.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

class SoftwareFJError(Exception): """Clase base"""
class ClienteInvalidoError(SoftwareFJError): """Error en cliente"""
class ServicioNoDisponibleError(SoftwareFJError): """Error en servicio"""
class ReservaInvalidaError(SoftwareFJError): """Error en reserva"""

# =================================================================
# ESTUDIANTE 2: ANA KARINA GARCIA RODRIGUEZ
# Clase Cliente (Encapsulación y Validaciones)
# =================================================================

class Cliente:
    def __init__(self, documento, nombre, correo, telefono):
        # Inicialización de atributos privados (Encapsulación)
        self.__documento = None
        self.__nombre = None
        self.__correo = None
        self.__telefono = None
        
        # El constructor delega a los setters para validar desde el inicio
        self.documento = documento
        self.nombre = nombre
        self.correo = correo
        self.telefono = telefono

    @property
    def documento(self): return self.__documento
    @documento.setter
    def documento(self, valor):
        if not str(valor).isdigit():
            raise ClienteInvalidoError("El documento debe ser numérico.")
        self.__documento = valor

    @property
    def nombre(self): return self.__nombre
    @nombre.setter
    def nombre(self, valor):
        if not valor or len(valor.strip()) < 3:
            raise ClienteInvalidoError("Nombre inválido (mínimo 3 caracteres).")
        self.__nombre = valor

    @property
    def correo(self): return self.__correo
    @correo.setter
    def correo(self, valor):
        patron = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(patron, valor):
            raise ClienteInvalidoError("Formato de correo electrónico inválido.")
        self.__correo = valor

    @property
    def telefono(self): return self.__telefono
    @telefono.setter
    def telefono(self, valor):
        if not str(valor).isdigit() or len(str(valor)) < 7:
            raise ClienteInvalidoError("Teléfono debe ser numérico y tener al menos 7 dígitos.")
        self.__telefono = valor

    def __str__(self):
        return f"Client: {self.nombre} (ID: {self.documento})"

# =================================================================
# ESTUDIANTE 3: ANGELA GABRIELA BECERRA ORTIZ
# Servicios (Herencia y Polimorfismo)
# =================================================================

class Servicio(ABC):
    def __init__(self, nombre, costo_base):
        self.nombre = nombre
        self.costo_base = costo_base

    @abstractmethod
    def calcular_costo(self, **kwargs): pass

    @abstractmethod
    def descripcion(self): pass

    def validar_base(self):
        if self.costo_base <= 0:
            raise ServicioNoDisponibleError(f"Costo base inválido para {self.nombre}")

class ServicioSala(Servicio):
    def calcular_costo(self, **kwargs):
        self.validar_base()
        horas = kwargs.get("horas", 0)
        if horas <= 0: raise ServicioNoDisponibleError("Las salas requieren horas > 0")
        # Sobrecarga lógica: Descuento si son más de 5 horas
        total = self.costo_base * horas
        return total * 0.9 if horas > 5 else total

    def descripcion(self):
        return f"Meeting Room: {self.nombre}"

class ServicioEquipo(Servicio):
    def calcular_costo(self, **kwargs):
        self.validar_base()
        dias = kwargs.get("dias", 0)
        if dias <= 0: raise ServicioNoDisponibleError("Alquiler requiere días > 0")
        return (self.costo_base * dias) + 15.0 # Seguro fijo de 15.0

    def descripcion(self):
        return f"Equipment Rental: {self.nombre}"

class ServicioAsesoria(Servicio):
    def calcular_costo(self, **kwargs):
        self.validar_base()
        horas = kwargs.get("horas", 0)
        if horas <= 0: raise ServicioNoDisponibleError("Asesoría requiere horas > 0")
        return self.costo_base * horas + 50.0 # Fee de consultoría fijo

    def descripcion(self):
        return f"Specialized Advisory: {self.nombre}"

# =================================================================
# ESTUDIANTE 4 (Integración): Clase Reserva y Simulación
# =================================================================

class Reserva:
    def __init__(self, cliente, servicio, parametros):
        self.cliente = cliente
        self.servicio = servicio
        self.parametros = parametros
        self.fecha = datetime.now()
        self.estado = "PENDING"

    def procesar(self):
        print(f"--- Processing Reservation for {self.cliente.nombre} ---")
        try:
            # Polimorfismo en acción
            costo = self.servicio.calcular_costo(**self.parametros)
            self.estado = "CONFIRMED"
            print(f"SUCCESS: {self.servicio.descripcion()} | Total: ${costo:.2f}")
            logging.info(f"Reserva Exitosa: {self.cliente.documento} - {self.servicio.nombre}")
        
        except ServicioNoDisponibleError as e:
            self.estado = "FAILED"
            logging.warning(f"Falla en Servicio: {e}")
            # Encadenamiento de excepciones
            raise ReservaInvalidaError("No se pudo completar la reserva por error en el servicio") from e
        
        except Exception as e:
            self.estado = "ERROR"
            logging.error(f"Error inesperado: {e}")
            raise
        
        finally:
            print(f"Status: {self.estado} | Date: {self.fecha.strftime('%Y-%m-%d %H:%M')}\n")

# --- SIMULACIÓN DE 10 OPERACIONES ---

def ejecutar_simulacion():
    # Catálogo de servicios disponibles
    s_sala = ServicioSala("Main Boardroom", 100)
    s_pc = ServicioEquipo("MacBook Pro", 50)
    s_adv = ServicioAsesoria("Legal Consult", 200)

    casos = [
        # 1. OK - Sala
        {"cl": ("123", "Juan Perez", "juan@mail.com", "3001234"), "srv": s_sala, "p": {"horas": 3}},
        # 2. ERROR - Cliente (Nombre corto)
        {"cl": ("456", "Al", "error@mail.com", "3001234"), "srv": s_adv, "p": {"horas": 2}},
        # 3. ERROR - Cliente (Documento no numérico)
        {"cl": ("ABC", "Luis Diaz", "luis@mail.com", "3001234"), "srv": s_pc, "p": {"dias": 1}},
        # 4. OK - Equipo
        {"cl": ("789", "Ana Rios", "ana@mail.com", "3159999"), "srv": s_pc, "p": {"dias": 5}},
        # 5. ERROR - Servicio (Horas 0)
        {"cl": ("101", "Pedro Solo", "ps@mail.com", "3201111"), "srv": s_sala, "p": {"horas": 0}},
        # 6. OK - Asesoría
        {"cl": ("202", "Marta Lopez", "marta@mail.com", "3008888"), "srv": s_adv, "p": {"horas": 4}},
        # 7. ERROR - Correo inválido
        {"cl": ("303", "Carlos Cas", "carlos@com", "3007777"), "srv": s_sala, "p": {"horas": 2}},
        # 8. OK - Sala con descuento (>5h)
        {"cl": ("404", "Sofia Re", "sofia@mail.com", "3006666"), "srv": s_sala, "p": {"horas": 10}},
        # 9. ERROR - Parámetros faltantes (No hay dias)
        {"cl": ("505", "Jose Mar", "jose@mail.com", "3005555"), "srv": s_pc, "p": {}},
        # 10. OK - Alquiler equipo corto
        {"cl": ("606", "Laura Vis", "laura@mail.com", "3004444"), "srv": s_pc, "p": {"dias": 2}},
    ]

    for i, data in enumerate(casos, 1):
        print(f"CASE #{i}")
        try:
            # Paso 1: Intentar crear cliente
            cliente_obj = Cliente(*data["cl"])
            
            # Paso 2: Intentar crear y procesar reserva
            reserva_obj = Reserva(cliente_obj, data["srv"], data["p"])
            reserva_obj.procesar()

        except ClienteInvalidoError as e:
            print(f"CLIENT ERROR: {e}")
            logging.error(f"Operación {i}: Cliente inválido - {e}")
        except ReservaInvalidaError as e:
            print(f"RESERVATION ERROR: {e}")
            # Aquí se ve el encadenamiento si se inspecciona el log
        except Exception as e:
            print(f"GENERAL ERROR: {e}")
        print("-" * 50)

if __name__ == "__main__":
    ejecutar_simulacion()