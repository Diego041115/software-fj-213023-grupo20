from abc import ABC, abstractmethod
from datetime import timedelta
from .excepciones import ParametroInvalidoError, ServicioNoDisponibleError
from .logger import obtener_logger

logger = obtener_logger()


class Servicio(ABC):
    """Clase abstracta base para todos los servicios."""

    def __init__(self, nombre: str, descripcion: str = ""):
        self._nombre = nombre
        self._descripcion = descripcion
        self._disponible = True

    @property
    def nombre(self) -> str:
        return self._nombre

    @property
    def disponible(self) -> bool:
        return self._disponible

    def marcar_como_no_disponible(self) -> None:
        self._disponible = False
        logger.info(f"Servicio no disponible: {self._nombre}")

    def marcar_como_disponible(self) -> None:
        self._disponible = True
        logger.info(f"Servicio disponible: {self._nombre}")

    @abstractmethod
    def _costo_base(self) -> float:
        pass

    @abstractmethod
    def validar_parametros(self, **kwargs) -> bool:
        pass

    @abstractmethod
    def describir(self) -> str:
        pass

    def calcular_costo(self, duracion: float | int | timedelta,
                       impuesto: float = 0.19, descuento: float = 0.0) -> float:
        """Calcula el precio final con impuestos y descuento."""
        if isinstance(duracion, timedelta):
            horas = duracion.total_seconds() / 3600
        else:
            horas = float(duracion)

        if horas <= 0:
            raise ParametroInvalidoError("La duración debe ser mayor a cero.", codigo="FJ-201")

        if not self.disponible:
            raise ServicioNoDisponibleError(f"El servicio '{self._nombre}' no está disponible.")

        costo_base = self._costo_base() * horas
        costo_con_descuento = costo_base * (1 - descuento)
        costo_final = costo_con_descuento * (1 + impuesto)
        return round(costo_final, 2)


class ReservaSala(Servicio):
    """Reserva de salas de reuniones."""
    def __init__(self, nombre_sala: str, capacidad_personas: int):
        super().__init__(f"Sala: {nombre_sala}", f"Sala para {capacidad_personas} personas")
        self._nombre_sala = nombre_sala
        self._capacidad = capacidad_personas
        self._costo_por_hora = 25000.0

    def _costo_base(self) -> float:
        return self._costo_por_hora

    def validar_parametros(self, **kwargs) -> bool:
        capacidad_solicitada = kwargs.get('capacidad', 1)
        if capacidad_solicitada > self._capacidad:
            raise ParametroInvalidoError(
                f"La sala '{self._nombre_sala}' solo admite {self._capacidad} personas.", codigo="FJ-202"
            )
        return True

    def describir(self) -> str:
        return (f"🏛️ {self.nombre} — Capacidad: {self._capacidad} personas — "
                f"$25.000/hora — {'✅ Disponible' if self.disponible else '❌ No disponible'}")


class AlquilerEquipo(Servicio):
    """Alquiler de equipos tecnológicos."""
    def __init__(self, tipo_equipo: str, modelo: str):
        super().__init__(f"Equipo: {tipo_equipo} ({modelo})", f"Alquiler de {tipo_equipo}")
        self._tipo_equipo = tipo_equipo
        self._modelo = modelo
        self._costo_por_hora = 15000.0

    def _costo_base(self) -> float:
        return self._costo_por_hora

    def validar_parametros(self, **kwargs) -> bool:
        return True

    def describir(self) -> str:
        return (f"💻 {self.nombre} — $15.000/hora — "
                f"{'✅ Disponible' if self.disponible else '❌ No disponible'}")


class Asesoria(Servicio):
    """Asesoría profesional."""
    def __init__(self, area_conocimiento: str, nombre_profesional: str):
        super().__init__(f"Asesoría en {area_conocimiento}", f"Con {nombre_profesional}")
        self._area = area_conocimiento
        self._profesional = nombre_profesional
        self._costo_por_hora = 80000.0

    def _costo_base(self) -> float:
        return self._costo_por_hora

    def validar_parametros(self, **kwargs) -> bool:
        return True

    def describir(self) -> str:
        return (f"🎓 {self.nombre} — Profesional: {self._profesional} — "
                f"$80.000/hora — {'✅ Disponible' if self.disponible else '❌ No disponible'}")
