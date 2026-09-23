import time

def evaluar_solucion(nombre, mensaje):
    print("\nAnalizando...")
    time.sleep(1.5)
    print(f"Diagnóstico para {nombre}: {mensaje}")
    
    funciono = input("\n¿Se solucionó el problema con esto? (s/n): ").lower().strip()
    
    if funciono == "s":
        print("Perfecto, el equipo ya está funcionando.")
    else:
        print("Te recomiendo llevar el equipo con un técnico para que lo revise físicamente.")

def iniciar_sistema():
    print("--- Bienvenido al Sistema de Diagnóstico ---")
    nombre = input("Ingresa tu nombre: ").strip()
    print("--- SISTEMA DE DIAGNÓSTICO BÁSICO ---\n")

    electricidad = input("1. ¿Hay electricidad en el enchufe? (s/n): ").lower().strip()
    if electricidad != "s":
        evaluar_solucion(nombre, "Conecta el equipo a otro enchufe o revisa que el regulador esté encendido.")
        return 

    enciende = input("2. ¿El equipo enciende (suenan ventiladores o prenden luces)? (s/n): ").lower().strip()
    if enciende != "s":
        print("\nDescartando problemas de energía...")
        
        cable = input("   -> ¿Revisaste que el cable de corriente esté bien conectado de ambos lados? (s/n): ").lower().strip()
        if cable != "s":
            evaluar_solucion(nombre, "Desconecta el cable de corriente, vuelve a conectarlo bien y prueba de nuevo.")
            return
            
        fuente = input("   -> ¿Ya intentaste desconectar los cables de la fuente a la tarjeta madre y volverlos a conectar? (s/n): ").lower().strip()
        if fuente != "s":
            evaluar_solucion(nombre, "Abre el gabinete, desconecta el cable de 24 pines y el del procesador, vuélvelos a poner y checa.")
            return
            
        evaluar_solucion(nombre, "Si los cables y conexiones están bien, seguro la fuente de poder se quemó o hay un corto en la placa.")
        return

    imagen = input("3. ¿Da video en el monitor? (s/n): ").lower().strip()
    if imagen != "s":
        print("\nDescartando problemas de video y RAM...")
        
        cables_video = input("   -> ¿Los cables de video (HDMI/VGA/DisplayPort) están bien puestos? (s/n): ").lower().strip()
        if cables_video != "s":
             evaluar_solucion(nombre, "Asegura bien los cables tanto en el monitor como en la PC.")
             return
             
        ram = input("   -> ¿Ya sacaste la memoria RAM para limpiarla y volverla a poner? (s/n): ").lower().strip()
        if ram != "s":
             evaluar_solucion(nombre, "Quita la RAM, limpia los contactos dorados con cuidado y ponla de nuevo hasta que haga clic.")
             return
             
        evaluar_solucion(nombre, "Si cables y RAM están bien, puede ser la tarjeta de video o de plano el monitor.")
        return

    carga_sistema = input("4. ¿Carga el sistema operativo (Windows/Mac/Linux)? (s/n): ").lower().strip()
    if carga_sistema != "s":
        bios = input("   -> ¿El equipo detecta el disco duro en la BIOS? (s/n): ").lower().strip()
        if bios != "s":
            evaluar_solucion(nombre, "Revisa los cables SATA o M.2. Si está bien conectado y no aparece, el disco ya murió.")
            return
        else:
            evaluar_solucion(nombre, "El disco funciona pero el sistema está dañado. Toca reparar el inicio o formatear.")
            return

    internet = input("5. ¿Se conecta a internet? (s/n): ").lower().strip()
    if internet != "s":
        evaluar_solucion(nombre, "Revisa si el cable Ethernet está bien conectado o si los drivers de red están actualizados.")
        return

    print("\nAnalizando...")
    time.sleep(1.5)
    print(f"Diagnóstico para {nombre}: El funcionamiento básico es correcto. Tu equipo no tiene fallas graves.")

if __name__ == "__main__":
    iniciar_sistema()