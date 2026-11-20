from datetime import datetime
from .cliente import Cliente
from .servicios import Servicio
from .excepciones import ReservaInvalidaError, OperacionNoPermitidaError
from .logger import obtener_logger

logger = obtener_logger()


class Reserva:
    """Clase que representa una reserva de un servicio."""
    
    PENDIENTE = "PENDIENTE"
    CONFIRMADA = "CONFIRMADA"
    PROCESADA = "PROCESADA"
    CANCELADA = "CANCELADA"
    RECHAZADA = "RECHAZADA"
    
    def __init__(self, cliente: Cliente, servicio: Servicio, duracion_horas: float, fecha=None):
        self.cliente = cliente
        self.servicio = servicio
        self.duracion_horas = duracion_horas
        self.fecha = fecha or datetime.now()
        self.estado = self.PENDIENTE
        self.costo_final = 0.0
        logger.info(f"Nueva reserva creada — Cliente: {cliente.nombre} — Servicio: {servicio.nombre}")
    
    def confirmar(self):
        """Confirma la reserva si está pendiente y el servicio está disponible."""
        if self.estado != self.PENDIENTE:
            raise OperacionNoPermitidaError(f"No se puede confirmar una reserva en estado {self.estado}")
        
        try:
            if not self.servicio.disponible:
                raise ReservaInvalidaError(f"El servicio {self.servicio.nombre} no está disponible")
        except Exception as error:
            self.estado = self.RECHAZADA
            logger.error(f"Reserva rechazada: {error}")
            raise ReservaInvalidaError(f"No se pudo confirmar: {error}") from error
        else:
            self.estado = self.CONFIRMADA
            self.costo_final = self.servicio.calcular_costo(self.duracion_horas)
            logger.info(f"Reserva CONFIRMADA — Costo: ${self.costo_final:,}")
        finally:
            logger.debug("Proceso de confirmación finalizado")
    
    def cancelar(self):
        """Cancela la reserva si aún no ha sido procesada."""
        if self.estado in [self.PROCESADA, self.CANCELADA, self.RECHAZADA]:
            raise OperacionNoPermitidaError(f"No se puede cancelar una reserva {self.estado}")
        
        self.estado = self.CANCELADA
        logger.info(f"Reserva CANCELADA — Cliente: {self.cliente.nombre}")
    
    def procesar(self):
        """Marca la reserva como procesada (servicio realizado)."""
        if self.estado != self.CONFIRMADA:
            raise OperacionNoPermitidaError("Solo se pueden procesar reservas confirmadas")
        
        self.estado = self.PROCESADA
        logger.info(f"Reserva PROCESADA — Servicio: {self.servicio.nombre}")
    
    def describir(self) -> str:
        return (f"📅 Reserva: {self.servicio.nombre} | Cliente: {self.cliente.nombre} | "
                f"Duración: {self.duracion_horas}h | Estado: {self.estado} | "
                f"Costo: ${self.costo_final:,.2f}")
