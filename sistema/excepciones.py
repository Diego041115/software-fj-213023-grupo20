class SoftwareFJError(Exception):
    """Excepción base del sistema Software FJ."""
    def __init__(self, mensaje: str, codigo: str = "FJ-000"):
        self.mensaje = mensaje
        self.codigo = codigo
        super().__init__(f"[{codigo}] {mensaje}")


class DocumentoInvalidoError(SoftwareFJError):
    """El documento de identidad no es válido."""
    def __init__(self, mensaje: str):
        super().__init__(mensaje, codigo="FJ-101")


class NombreInvalidoError(SoftwareFJError):
    """El nombre no cumple con los requisitos."""
    def __init__(self, mensaje: str):
        super().__init__(mensaje, codigo="FJ-102")


class ParametroInvalidoError(SoftwareFJError):
    """Un parámetro proporcionado no es válido."""
    def __init__(self, mensaje: str, codigo: str = "FJ-200"):
        super().__init__(mensaje, codigo=codigo)


class ServicioNoDisponibleError(SoftwareFJError):
    """El servicio solicitado no está disponible."""
    def __init__(self, mensaje: str):
        super().__init__(mensaje, codigo="FJ-301")


class ReservaInvalidaError(SoftwareFJError):
    """La reserva no se puede realizar."""
    def __init__(self, mensaje: str):
        super().__init__(mensaje, codigo="FJ-401")


class OperacionNoPermitidaError(SoftwareFJError):
    """No se permite cambiar el estado de la reserva."""
    def __init__(self, mensaje: str):
        super().__init__(mensaje, codigo="FJ-501")
