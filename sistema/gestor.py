from typing import List

from .cliente import Cliente
from .servicios import Servicio
from .reserva import Reserva
from .excepciones import (
    ParametroInvalidoError,
    ServicioNoDisponibleError,
    ReservaInvalidaError,
)
from .logger import obtener_logger


logger = obtener_logger()


class GestorSoftwareFJ:
    """Administra clientes, servicios y reservas del sistema."""

    def __init__(self):
        self.clientes: List[Cliente] = []
        self.servicios: List[Servicio] = []
        self.reservas: List[Reserva] = []

    def registrar_cliente(
        self,
        documento: str,
        nombre: str,
        correo: str = "",
        telefono: str = "",
    ) -> Cliente:
        if any(cliente.documento == documento for cliente in self.clientes):
            raise ParametroInvalidoError(
                f"Ya existe un cliente con el documento {documento}.",
                codigo="FJ-203",
            )

        cliente = Cliente(documento, nombre, correo, telefono)
        self.clientes.append(cliente)
        logger.info(f"Cliente registrado: {cliente.nombre}")
        return cliente

    def registrar_servicio(self, servicio: Servicio) -> Servicio:
        if not isinstance(servicio, Servicio):
            raise ParametroInvalidoError(
                "El objeto registrado no corresponde a un servicio.",
                codigo="FJ-204",
            )
        self.servicios.append(servicio)
        logger.info(f"Servicio registrado: {servicio.nombre}")
        return servicio

    def listar_servicios(self) -> str:
        if not self.servicios:
            return "No hay servicios registrados"

        resultado = "\n".join(
            f"{indice}. {servicio.describir()}"
            for indice, servicio in enumerate(self.servicios)
        )
        logger.info("Servicios disponibles consultados")
        return resultado

    def listar_reservas(self) -> str:
        if not self.reservas:
            return "No hay reservas registradas"

        resultado = "\n".join(
            f"{indice}. {reserva.describir()}"
            for indice, reserva in enumerate(self.reservas)
        )
        logger.info("Historial de reservas consultado")
        return resultado

    def buscar_cliente(self, documento: str) -> Cliente:
        for cliente in self.clientes:
            if cliente.documento == documento:
                return cliente
        raise ReservaInvalidaError(
            f"No existe un cliente registrado con el documento {documento}."
        )

    def buscar_servicio(self, nombre: str) -> Servicio:
        for servicio in self.servicios:
            if servicio.nombre == nombre:
                return servicio
        raise ReservaInvalidaError(
            f"No existe un servicio registrado con el nombre '{nombre}'."
        )

    def crear_reserva(
        self,
        documento_cliente: str,
        nombre_servicio: str,
        duracion_horas: float,
    ) -> Reserva:
        if duracion_horas <= 0:
            raise ParametroInvalidoError(
                "La duración debe ser mayor a cero.",
                codigo="FJ-201",
            )

        cliente = self.buscar_cliente(documento_cliente)
        servicio = self.buscar_servicio(nombre_servicio)

        if not servicio.disponible:
            raise ServicioNoDisponibleError(
                f"El servicio '{servicio.nombre}' no está disponible."
            )

        reserva = Reserva(cliente, servicio, float(duracion_horas))
        self.reservas.append(reserva)
        logger.info(f"Reserva creada en el índice {len(self.reservas) - 1}")
        return reserva

    def confirmar_reserva(self, indice: int) -> Reserva:
        reserva = self._obtener_reserva(indice)
        reserva.confirmar()
        return reserva

    def procesar_reserva(self, indice: int) -> Reserva:
        reserva = self._obtener_reserva(indice)
        reserva.procesar()
        return reserva

    def cancelar_reserva(self, indice: int) -> Reserva:
        reserva = self._obtener_reserva(indice)
        reserva.cancelar()
        return reserva

    def _obtener_reserva(self, indice: int) -> Reserva:
        if indice < 0 or indice >= len(self.reservas):
            raise ReservaInvalidaError(
                f"No existe una reserva en el índice {indice}.",
            )
        return self.reservas[indice]
