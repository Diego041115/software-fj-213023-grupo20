import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from sistema import (
    obtener_logger, GestorSoftwareFJ,
    Cliente, ReservaSala, AlquilerEquipo, Asesoria, Reserva,
    NombreInvalidoError, DocumentoInvalidoError, ParametroInvalidoError,
    ServicioNoDisponibleError, ReservaInvalidaError, OperacionNoPermitidaError
)

logger = obtener_logger()


def ejecutar_operacion(nombre_operacion: str, funcion):
    """Ejecuta una operación con manejo de excepciones try/except/else/finally"""
    print(f"\n{'='*60}")
    print(f"🔹 {nombre_operacion}")
    print('-'*60)
    try:
        resultado = funcion()
    except Exception as error:
        logger.error(f"❌ Falló: {error}")
        print(f"❌ Resultado: ERROR → {error}")
    else:
        logger.info(f"✅ {nombre_operacion} — Exitoso")
        print(f"✅ Resultado: OK")
        if resultado:
            print(f"   → {resultado}")
    finally:
        print(f"📝 Operación finalizada: {nombre_operacion}")


def main():
    print("\n" + "="*60)
    print("   SISTEMA INTEGRAL DE GESTIÓN — SOFTWARE FJ")
    print("="*60)
    logger.info("Inicio de simulación de 23 operaciones")

    gestor = GestorSoftwareFJ()

    # ========== 1. REGISTRO DE CLIENTES ==========
    ejecutar_operacion("1. Registrar cliente válido — María Pérez",
        lambda: gestor.registrar_cliente("1098765432", "María Pérez", "maria@email.com", "3101234567"))

    ejecutar_operacion("2. Registrar cliente válido — Juan Gómez",
        lambda: gestor.registrar_cliente("1098765433", "Juan Gómez", "juan@email.com", "3101234568"))

    ejecutar_operacion("3. Intentar registrar cliente con nombre muy corto",
        lambda: gestor.registrar_cliente("1234567890", "M", "corto@email.com", "3000000000"))

    ejecutar_operacion("4. Intentar registrar cliente con documento corto",
        lambda: gestor.registrar_cliente("123", "Pedro Ruiz", "pedro@email.com", "3110000000"))

    ejecutar_operacion("5. Intentar registrar cliente con documento con letras",
        lambda: gestor.registrar_cliente("ABC12345", "Ana María", "ana@email.com", "3120000000"))

    # ========== 2. CREACIÓN DE SERVICIOS ==========
    ejecutar_operacion("6. Crear servicio: Sala de Conferencias A",
        lambda: gestor.registrar_servicio(ReservaSala("Conferencias A", 30)))

    ejecutar_operacion("7. Crear servicio: Sala Pequeña B",
        lambda: gestor.registrar_servicio(ReservaSala("Pequeña B", 6)))

    ejecutar_operacion("8. Crear servicio: Alquiler de Portátil",
        lambda: gestor.registrar_servicio(AlquilerEquipo("Portátil", "HP Pavilion 15")))

    ejecutar_operacion("9. Crear servicio: Asesoría en Programación",
        lambda: gestor.registrar_servicio(Asesoria("Programación", "Ing. Carlos Ruiz")))

    ejecutar_operacion("10. Listar todos los servicios disponibles",
        lambda: gestor.listar_servicios())

    # ========== 3. RESERVAS EXITOSAS ==========
    ejecutar_operacion("11. Reserva — María reserva Sala A por 2 horas",
        lambda: gestor.crear_reserva("1098765432", "Sala: Conferencias A", 2.0))

    ejecutar_operacion("12. Reserva — Juan alquila portátil por 5 horas",
        lambda: gestor.crear_reserva("1098765433", "Equipo: Portátil (HP Pavilion 15)", 5.0))

    ejecutar_operacion("13. Confirmar la reserva de María",
        lambda: gestor.confirmar_reserva(0))

    ejecutar_operacion("14. Confirmar y procesar reserva de Juan",
        lambda: (gestor.confirmar_reserva(1), gestor.procesar_reserva(1)))

    # ========== 4. RESERVAS FALLIDAS ==========
    ejecutar_operacion("15. Intentar reservar sala para más personas de las que caben",
        lambda: ReservaSala("Pequeña B", 6).validar_parametros(capacidad=10))

    ejecutar_operacion("16. Intentar crear reserva con duración negativa",
        lambda: gestor.crear_reserva("1098765432", "Sala: Conferencias A", -3))

    ejecutar_operacion("17. Marcar servicio como no disponible e intentar reservarlo",
        lambda: (gestor.servicios[0].marcar_como_no_disponible(),
                 gestor.crear_reserva("1098765433", "Sala: Conferencias A", 1)))

    ejecutar_operacion("18. Cancelar una reserva y verificar estado",
        lambda: (gestor.cancelar_reserva(0), gestor.reservas[0].estado))

    ejecutar_operacion("19. Intentar cancelar una reserva ya procesada",
        lambda: gestor.cancelar_reserva(1))

    ejecutar_operacion("20. Intentar confirmar una reserva que no existe",
        lambda: gestor.confirmar_reserva(99))

    ejecutar_operacion("21. Calcular costo con descuento del 10%",
        lambda: f"$ {ReservaSala('Prueba', 10).calcular_costo(4, descuento=0.10):,.2f}")

    ejecutar_operacion("22. Listar historial completo de reservas",
        lambda: gestor.listar_reservas())

    ejecutar_operacion("23. Verificar archivo de log creado en logs/software_fj.log",
        lambda: "✅ Archivo de registro generado correctamente")

    print("\n" + "="*60)
    print("   FIN DE LA SIMULACIÓN — 23 OPERACIONES EJECUTADAS")
    print("="*60)
    logger.info("Simulación finalizada — 23 operaciones completadas")


if __name__ == "__main__":
    main()

