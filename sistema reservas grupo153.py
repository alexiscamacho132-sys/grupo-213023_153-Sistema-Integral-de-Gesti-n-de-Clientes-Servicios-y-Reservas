#Sistema Integral de Gestión de Clientes, Servicios y Reservas

#Aporte estudiante Jairo Alexis Camacho
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




#Aporte de la Estudiante: ANA KARINA GARCIA RODRIGUEZ 
# Clase Cliente (Validación y Encapsulación)
#Se enfoca en proteger los datos y asegurar que ningún cliente se cree con información corrupta.

import re

class Cliente:
    def __init__(self, nombre, documento, correo, telefono):
        try:
            # Encapsulación de atributos
            self.__nombre = None
            self.__documento = None
            self.__correo = None
            self.__telefono = None

            # Validaciones mediante setters
            self.set_nombre(nombre)
            self.set_documento(documento)
            self.set_correo(correo)
            self.set_telefono(telefono)

        except Exception as e:
            logging.error(f"Error al crear cliente: {e}")
            raise ClienteInvalidoError(f"Datos inválidos del cliente: {e}")

    # ---------------- VALIDACIONES ---------------- #

    def set_nombre(self, nombre):
        if not nombre or not nombre.strip():
            raise ValueError("El nombre no puede estar vacío")
        self.__nombre = nombre

    def set_documento(self, documento):
        if not str(documento).isdigit():
            raise ValueError("El documento debe ser numérico")
        self.__documento = documento

    def set_correo(self, correo):
        patron = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(patron, correo):
            raise ValueError("Correo electrónico inválido")
        self.__correo = correo

    def set_telefono(self, telefono):
        if not str(telefono).isdigit() or len(str(telefono)) < 7:
            raise ValueError("Teléfono inválido")
        self.__telefono = telefono

    # ---------------- GETTERS (PROPIEDADES) ---------------- #

    @property
    def nombre(self):
        return self.__nombre

    @property
    def documento(self):
        return self.__documento

    @property
    def correo(self):
        return self.__correo

    @property
    def telefono(self):
        return self.__telefono

    # ---------------- MÉTODOS ---------------- #

    def mostrar_info(self):
        return f"Cliente: {self.__nombre} - Documento: {self.__documento}"



#Aporte de la estudiante ANGELA GABRIELA BECERRA ORTIZ 
#Servicios (Herencia y Polimorfismo)
#Define la estructura de los servicios y cómo varía el cálculo del costo


class Servicio(ABC):
    def __init__(self, nombre, costo_base):
        self.nombre = nombre
        self.costo_base = costo_base

    @abstractmethod
    def calcular_costo(self, **kwargs):
        pass

    @abstractmethod
    def descripcion(self):
        pass

    def validar(self):
        if self.costo_base < 0:
            raise ServicioNoDisponibleError("El costo no puede ser negativo")
        if not self.nombre:
            raise ServicioNoDisponibleError("El servicio debe tener nombre")


class ServicioSala(Servicio):
    def calcular_costo(self, **kwargs):
        try:
            self.validar()
            horas = kwargs.get("horas")
            if horas is None or horas <= 0:
                raise ServicioNoDisponibleError("Horas inválidas")
        except Exception as e:
            logging.error(f"Error en ServicioSala: {e}")
            raise
        else:
            return self.costo_base * horas

    def descripcion(self):
        return f"Reserva de sala: {self.nombre}"


class ServicioEquipo(Servicio):
    def calcular_costo(self, **kwargs):
        try:
            self.validar()
            dias = kwargs.get("dias")
            if dias is None or dias <= 0:
                raise ServicioNoDisponibleError("Días inválidos")
        except Exception as e:
            logging.error(f"Error en ServicioEquipo: {e}")
            raise
        else:
            return self.costo_base * dias * 1.1

    def descripcion(self):
        return f"Alquiler de equipo: {self.nombre}"


class ServicioAsesoria(Servicio):
    def calcular_costo(self, **kwargs):
        try:
            self.validar()
            horas = kwargs.get("horas")
            if horas is None or horas <= 0:
                raise ServicioNoDisponibleError("Horas inválidas")
        except Exception as e:
            logging.error(f"Error en ServicioAsesoria: {e}")
            raise
        else:
            return self.costo_base * horas + 50

    def descripcion(self):
        return f"Asesoría especializada: {self.nombre}"




# Aporte estudiante ..... JESUS HERNANDO VILLAMIZAR ESPINOSA 
#Clase Reserva y Orquestación de Errores 
#Integra todo y maneja el flujo de ejecución

@abstractmethod
class Reserva:
    def __init__ (self, cliente, servicio, **kwargs):
        self.cliente = cliente
        self.servicio = servicio
        self.parametros = kwargs
    
    def procesar (self):
        try:
            costo = self.servicio.calcular_costo(**self.parametros)
        except Exception as e:
            logging.error(f"error al procesar la reserva: {e}")
            raise ReservaInvalidaError(f"No se pudo procesar la reserva")
        else:
            self.estado = "confirmada"
            return costo
    
    def confirmar (self):
        if self.estado != "confirmada":
            raise ReservaInvalidaError("No se puede confirmar ")
        return "Reserva confirmada"
    
    def cancelar (self):
        self.estado == ""
        return "Reserva cancelada con éxito"

    def mostrar(self):
        return f"{self.cliente.mostrar_info()} | {self.servicio.descripcion()} | Estado: {self.estado}"