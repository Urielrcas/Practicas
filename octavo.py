import tkinter as tk
from tkinter import messagebox
import random
from datetime import datetime, timedelta


# 1. GENERAR CITA Y NÚMERO ALEATORIO AL INICIO
num_cita_original = random.randint(10000, 99999)
dias = random.randint(1, 15)
hora = random.randint(8, 18)
mins = random.choice(["00", "15", "30", "45"])
fecha_cita = datetime.now() + timedelta(days=dias)
fecha_str = f"{fecha_cita.strftime('%d/%m/%Y')} a las {hora}:{mins} hrs"
doc_asignado = random.choice(["Dr. Monroy", "Dra. Salcedo", "Dr. Octaviano", "Dra. Ramírez"])

# 2. FUNCIÓN PRINCIPAL DE EVALUACIÓN
def procesar_datos():
    nombre = entry_nombre.get().strip()
    if not nombre:
        messagebox.showerror("Error", "El nombre no puede estar vacío.")
        return

    try:
        edad = int(entry_edad.get())
        if not (0 <= edad <= 120):
            messagebox.showerror("Error", f"La edad {edad} es irreal. Debe estar entre 0 y 120.")
            return
    except ValueError:
        messagebox.showerror("Error", "La edad debe ser un número entero.")
        return

    try:
        oxigeno = int(entry_oxigeno.get())
        if not (0 <= oxigeno <= 100):
            messagebox.showerror("Error", f"El oxígeno {oxigeno} es irreal. Debe estar entre 0 y 100.")
            return
    except ValueError:
        messagebox.showerror("Error", "El oxígeno debe ser un número entero.")
        return

    try:
        fc = int(entry_fc.get())
        if not (0 <= fc <= 250):
            messagebox.showerror("Error", f"La frecuencia cardíaca {fc} es irreal.")
            return
    except ValueError:
        messagebox.showerror("Error", "La frecuencia cardíaca debe ser un número.")
        return

    try:
        sis_str, dia_str = entry_presion.get().split('/')
        sis = int(sis_str)
        dia = int(dia_str)
        if not (50 <= sis <= 250 and 30 <= dia <= 150):
            messagebox.showerror("Error", "Valores de presión irreales. Revisa los datos.")
            return
    except ValueError:
        messagebox.showerror("Error", "Formato de presión incorrecto. Usa el formato 120/80.")
        return

    try:
        peso = float(entry_peso.get())
        if not (2.0 <= peso <= 300.0):
            messagebox.showerror("Error", "El peso debe estar entre 2.0 y 300.0 kg.")
            return
    except ValueError:
        messagebox.showerror("Error", "El peso debe ser un número.")
        return

    try:
        talla = float(entry_talla.get())
        if not (0.4 <= talla <= 2.5):
            messagebox.showerror("Error", "La estatura debe estar entre 0.4 y 2.5 m.")
            return
    except ValueError:
        messagebox.showerror("Error", "La estatura debe ser un número (ej. 1.70).")
        return

    # EVALUACIÓN LÓGICA
    imc = peso / (talla ** 2)
    diagnostico = []
    derivacion = None

    if imc < 18.5:
        estado_imc = "Bajo peso"
        diagnostico.append("Requiere plan de alimentación para subir de peso.")
        derivacion = "Nutrición"
    elif imc <= 24.9:
        estado_imc = "Peso normal"
    elif imc <= 29.9:
        estado_imc = "Sobrepeso"
        diagnostico.append("Alerta por sobrepeso. Se sugiere revisión de dieta.")
        derivacion = "Nutrición"
    else:
        estado_imc = "Obesidad"
        diagnostico.append("Riesgo por obesidad. Requiere intervención nutricional.")
        derivacion = "Nutrición"

    if sis > 130 or dia > 85 or fc > 100:
        diagnostico.append("Alteración en presión arterial o ritmo cardíaco.")
        derivacion = "Cardiología"

    if oxigeno < 90:
        diagnostico.append("Hipoxia detectada (Nivel de oxígeno bajo).")
        derivacion = "Neumología"

    if not diagnostico:
        diagnostico.append("Signos vitales dentro de los parámetros normales.")

    # MOSTRAR RESULTADOS EN LA INTERFAZ
    caja_resultados.delete(1.0, tk.END)
    caja_resultados.insert(tk.END, "REPORTE MÉDICO FINAL\n")
    caja_resultados.insert(tk.END, f"Paciente: {nombre}\n")
    caja_resultados.insert(tk.END, f"Edad: {edad} años\n")
    caja_resultados.insert(tk.END, f"IMC: {round(imc, 1)} ({estado_imc})\n")
    caja_resultados.insert(tk.END, f"Oxígeno: {oxigeno}%\n")
    caja_resultados.insert(tk.END, f"Presión: {sis}/{dia}\n")
    caja_resultados.insert(tk.END, f"FC: {fc} lpm\n\n")

    caja_resultados.insert(tk.END, "DIAGNÓSTICO:\n")
    for d in diagnostico:
        caja_resultados.insert(tk.END, f"- {d}\n")

    caja_resultados.insert(tk.END, "\nESTADO DE LA CITA:\n")
    
    if derivacion:
        # Generamos nuevos datos para la cita de especialidad
        num_cita_nueva = random.randint(10000, 99999)
        dias_nueva = random.randint(1, 15)
        hora_nueva = random.randint(8, 18)
        mins_nueva = random.choice(["00", "15", "30", "45"])
        fecha_nueva = datetime.now() + timedelta(days=dias_nueva)
        fecha_nueva_str = f"{fecha_nueva.strftime('%d/%m/%Y')} a las {hora_nueva}:{mins_nueva} hrs"

        caja_resultados.insert(tk.END, f"--> La cita original #{num_cita_original} se CANCELA.\n")
        caja_resultados.insert(tk.END, f"--> Nueva cita generada para el área de: {derivacion}\n")
        caja_resultados.insert(tk.END, f"--> Nuevo Folio: #{num_cita_nueva}\n")
        caja_resultados.insert(tk.END, f"--> Nueva Fecha: {fecha_nueva_str}\n")
    else:
        caja_resultados.insert(tk.END, "--> No se requieren derivaciones especiales.\n")
        caja_resultados.insert(tk.END, f"--> Se MANTIENE la cita #{num_cita_original}\n")
        caja_resultados.insert(tk.END, f"--> Médico: {doc_asignado}\n")
        caja_resultados.insert(tk.END, f"--> Fecha: {fecha_str}\n")
        

ventana = tk.Tk()
ventana.title("Hospital Médica MIA")
ventana.geometry("480x750")
ventana.config(padx=20, pady=20)

tk.Label(ventana, text=" Cita previa generada en el sistema", fg="red", font=("Arial", 10, "bold")).pack()
tk.Label(ventana, text=f"Folio: #{num_cita_original}").pack()
tk.Label(ventana, text=f"Fecha: {fecha_str}").pack()
tk.Label(ventana, text=f"Médico Inicial: {doc_asignado} (Medicina General)").pack()

tk.Label(ventana, text="-"*50).pack(pady=10)

# Formulario de entrada
tk.Label(ventana, text="Nombre del paciente:").pack()
entry_nombre = tk.Entry(ventana, width=30)
entry_nombre.pack()

tk.Label(ventana, text="Edad:").pack()
entry_edad = tk.Entry(ventana, width=10)
entry_edad.pack()

tk.Label(ventana, text="Oxígeno (%):").pack()
entry_oxigeno = tk.Entry(ventana, width=10)
entry_oxigeno.pack()

tk.Label(ventana, text="Frecuencia Cardíaca (lpm):").pack()
entry_fc = tk.Entry(ventana, width=10)
entry_fc.pack()

tk.Label(ventana, text="Presión Arterial (ej. 120/80):").pack()
entry_presion = tk.Entry(ventana, width=15)
entry_presion.pack()

tk.Label(ventana, text="Peso (kg):").pack()
entry_peso = tk.Entry(ventana, width=10)
entry_peso.pack()

tk.Label(ventana, text="Estatura (m):").pack()
entry_talla = tk.Entry(ventana, width=10)
entry_talla.pack()

# Botón para procesar
tk.Button(ventana, text="Diagnosticar y Asignar", command=procesar_datos, bg="lightgray", font=("Arial", 10, "bold")).pack(pady=15)

# Cuadro de texto para mostrar el resultado final
caja_resultados = tk.Text(ventana, height=20, width=55)
caja_resultados.pack()

ventana.mainloop()