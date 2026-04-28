#Excepciones Personalizadas y Logging (La Base)
#Este módulo debe definirse primero para que los otros estudiantes puedan usar las excepciones y el registro de errores
import logging
from abc import ABC, abstractmethod
from datetime import datetime

# Configuración del archivo de LOGS
logging.basicConfig(
    filename="gestion_errores.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Excepciones Personalizadas
class SoftwareFJError(Exception): """Clase base para errores del sistema"""
class ClienteInvalidoError(SoftwareFJError): """Error en datos del cliente"""
class ServicioNoDisponibleError(SoftwareFJError): """Error en parámetros del servicio"""
class ReservaInvalidaError(SoftwareFJError): """Error en la lógica de reserva"""



#Clase Reserva y Orquestación de Errores _ Jairo Alexis Cmacho
#Integra todo y maneja el flujo de ejecución
class Reserva:
    def __init__(self, cliente, servicio, parametros):
        self.cliente = cliente
        self.servicio = servicio
        self.parametros = parametros
        self.estado = "Pendiente"

    def procesar(self):
        try:
            print(f"--- Procesando Reserva para {self.cliente.nombre} ---")
            costo = self.servicio.calcular_costo(**self.parametros)
        except TypeError as e:
            error_msg = f"Parámetros faltantes en servicio {self.servicio.nombre}: {e}"
            logging.error(error_msg)
            raise ReservaInvalidaError(error_msg) from e
        except Exception as e:
            logging.error(f"Error inesperado: {e}")
            raise
        else:
            self.estado = "Confirmada"
            print(f"Reserva Exitosa. Costo Total: ${costo}")
            logging.info(f"Reserva Exitosa para {self.cliente.nombre}")
        finally:
            print(f"Estado final de la operación: {self.estado}\n")

