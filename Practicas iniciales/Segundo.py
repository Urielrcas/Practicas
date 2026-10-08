
dual = input("¿El alumno es DUAL? (s/n): ").strip().lower()

if dual == "s":
    print("Aprobado directamente")
else:
    P = float(input("Ingrese el porcentaje de asistencia (P): "))
    Q = float(input("Ingrese el promedio obtenido (Q): "))
    R = input("¿Entrego el proyecto? (s/n): ").strip().lower()

    asistencia = P >= 80
    promedio = Q >= 8
    proyecto = R == "s"

    if asistencia and promedio and proyecto:
        resultado = "APROBADO"
    else:
        resultado = "REPROBADO"

    print("\n--- Resultado de la evaluacion ---")
    print(f"Asistencia: {P}%  -> {'Aprobatorio' if asistencia else 'No aprobatorio'}")
    print(f"Promedio:   {Q}   -> {'Aprobatorio' if promedio else 'No aprobatorio'}")
    print(f"Proyecto:   {'Si' if proyecto else 'No'}   -> {'Aprobatorio' if proyecto else 'No aprobatorio'}")
    print(f"\nLa materia queda: {resultado}")