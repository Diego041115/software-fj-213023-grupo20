import logging
import os
from datetime import datetime


def obtener_logger(nombre_logger: str = "software_fj") -> logging.Logger:
    """Configura y devuelve un objeto para registrar eventos y errores en un archivo."""
    carpeta_logs = "logs"
    try:
        if not os.path.exists(carpeta_logs):
            os.makedirs(carpeta_logs)
    except OSError as error_carpeta:
        print(f"⚠️ No se pudo crear la carpeta de registros: {error_carpeta}")
    else:
        ruta_archivo = os.path.join(carpeta_logs, "software_fj.log")
        logger = logging.getLogger(nombre_logger)
        
        if logger.handlers:
            return logger
        
        logger.setLevel(logging.DEBUG)
        formato = logging.Formatter('%(asctime)s | %(levelname)-8s | %(message)s',
                                     datefmt='%Y-%m-%d %H:%M:%S')
        
        manejador_archivo = logging.FileHandler(ruta_archivo, encoding='utf-8')
        manejador_archivo.setFormatter(formato)
        manejador_archivo.setLevel(logging.DEBUG)
        
        manejador_consola = logging.StreamHandler()
        manejador_consola.setFormatter(formato)
        manejador_consola.setLevel(logging.INFO)
        
        logger.addHandler(manejador_archivo)
        logger.addHandler(manejador_consola)
        logger.info("=" * 50)
        logger.info("Inicio de sesión del sistema Software FJ")
        
        return logger
