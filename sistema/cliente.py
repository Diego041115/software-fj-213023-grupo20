import re
from .entidad import Entidad
from .excepciones import NombreInvalidoError, DocumentoInvalidoError
from .logger import obtener_logger

logger = obtener_logger()


class Cliente(Entidad):
    """Clase que representa a un cliente del sistema."""
    
    def __init__(self, identificador: str, nombre: str, correo: str = "", telefono: str = ""):
        super().__init__(identificador)
        self.__nombre = nombre.strip()
        self.__correo = correo.strip()
        self.__telefono = telefono.strip()
        
        try:
            self.validar()
        except (NombreInvalidoError, DocumentoInvalidoError) as error:
            logger.error(f"No se pudo crear el cliente: {error}")
            raise
    
    @property
    def nombre(self) -> str:
        return self.__nombre
    
    @property
    def documento(self) -> str:
        return self._id
    
    @property
    def correo(self) -> str:
        return self.__correo
    
    @property
    def telefono(self) -> str:
        return self.__telefono
    
    def validar(self) -> bool:
        """Verifica que el nombre y el documento sean correctos."""
        if len(self.__nombre) < 2:
            raise NombreInvalidoError("El nombre debe tener al menos 2 caracteres.")
        
        if not re.match(r"^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$", self.__nombre):
            raise NombreInvalidoError("El nombre solo puede contener letras y espacios.")
        
        if len(self._id) < 5 or not self._id.isdigit():
            raise DocumentoInvalidoError("El documento debe tener al menos 5 dígitos y solo números.")
        
        logger.debug(f"Cliente validado: {self.__nombre}")
        return True
    
    def describir(self) -> str:
        return f"👤 Cliente: {self.__nombre} | Doc: {self._id} | Correo: {self.__correo or 'No registrado'}"
