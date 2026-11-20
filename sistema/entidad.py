from abc import ABC, abstractmethod


class Entidad(ABC):
    """Clase abstracta que representa cualquier elemento del sistema."""
    
    def __init__(self, identificador: str):
        self._id = identificador
    
    @property
    def id(self) -> str:
        return self._id
    
    @abstractmethod
    def validar(self) -> bool:
        """Valida que los datos sean correctos."""
        pass
    
    @abstractmethod
    def describir(self) -> str:
        """Devuelve una descripción con los datos del elemento."""
        pass
