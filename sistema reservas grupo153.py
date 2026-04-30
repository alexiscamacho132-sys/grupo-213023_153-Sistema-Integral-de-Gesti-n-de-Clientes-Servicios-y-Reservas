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




#Aporte de la estudiante ANGELA GABRIELA BECERRA ORTIZ 
#Servicios (Herencia y Polimorfismo)
#Define la estructura de los servicios y cómo varía el cálculo del costo




# Aporte estudiante ..... JESUS HERNANDO VILLAMIZAR ESPINOSA 
#Clase Reserva y Orquestación de Errores 
#Integra todo y maneja el flujo de ejecución

