import os
import random
from datetime import datetime, timedelta
import tkinter as tk
from tkinter import ttk, messagebox
from dotenv import load_dotenv
from pymongo import MongoClient
import dns.resolver



load_dotenv()

mongo_user = os.getenv("Mongo_User")
mongo_pass = os.getenv("Mongo_Password")
mongo_cluster = os.getenv("Mongo_Cluster")
mongo_db_name = os.getenv("Mongo_db")
mongo_collection = os.getenv("Mongo_Colleccion")

if not all([mongo_user, mongo_pass, mongo_cluster, mongo_db_name, mongo_collection]):
    raise ValueError("Faltan variables en el archivo .env")

mongo_uri = f"mongodb+srv://{mongo_user}:{mongo_pass}@{mongo_cluster}/?retryWrites=true&w=majority"

try:
    client = MongoClient(mongo_uri)
    db = client[mongo_db_name]
    coleccion = db[mongo_collection]
except Exception as e:
    messagebox.showerror("Error de conexión", f"No se pudo conectar a MongoDB: {e}")


def generar_cita_aleatoria():
    global num_cita_original, fecha_str, doc_asignado
    num_cita_original = random.randint(10000, 99999)
    dias = random.randint(1, 15)
    hora = random.randint(8, 18)
    mins = random.choice(["00", "15", "30", "45"])
    fecha_cita = datetime.now() + timedelta(days=dias)
    fecha_str = f"{fecha_cita.strftime('%d/%m/%Y')} {hora}:{mins} hrs"
    doc_asignado = random.choice(["Dr. Monroy", "Dra. Salcedo", "Dr. Octaviano", "Dra. Ramírez"])

generar_cita_aleatoria()


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
        messagebox.showerror("Error", "La frecuencia cardíaca debe ser un número entero.")
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

    imc = peso / (talla ** 2)
    diagnostico_lista = []
    derivacion = None

    if imc < 18.5:
        estado_imc = "Bajo peso"
        diagnostico_lista.append("Plan para subir de peso.")
        derivacion = "Nutrición"
    elif imc <= 24.9:
        estado_imc = "Normal"
    elif imc <= 29.9:
        estado_imc = "Sobrepeso"
        diagnostico_lista.append("Revisión de dieta.")
        derivacion = "Nutrición"
    else:
        estado_imc = "Obesidad"
        diagnostico_lista.append("Intervención nutricional.")
        derivacion = "Nutrición"

    if sis > 130 or dia > 85 or fc > 100:
        diagnostico_lista.append("Alteración de presión/ritmo.")
        derivacion = "Cardiología"

    if oxigeno < 90:
        diagnostico_lista.append("Hipoxia detectada.")
        derivacion = "Neumología"

    if not diagnostico_lista:
        diagnostico_lista.append("Signos vitales normales.")

    if derivacion:
        folio_final = random.randint(10000, 99999)
        dias_nueva = random.randint(1, 15)
        hora_nueva = random.randint(8, 18)
        mins_nueva = random.choice(["00", "15", "30", "45"])
        fecha_final = (datetime.now() + timedelta(days=dias_nueva)).strftime('%d/%m/%Y') + f" {hora_nueva}:{mins_nueva} hrs"
        medico_final = f"Esp. {derivacion}"
        estado_cita = f"Derivado a {derivacion} (Cancelada #{num_cita_original})"
    else:
        folio_final = num_cita_original
        fecha_final = fecha_str
        medico_final = doc_asignado
        estado_cita = "Mantiene general"

    diag_texto = "; ".join(diagnostico_lista)

    caja_resultados.delete(1.0, tk.END)
    caja_resultados.insert(tk.END, "=== REPORTE MÉDICO ===\n")
    caja_resultados.insert(tk.END, f"Paciente: {nombre} ({edad} años)\n")
    caja_resultados.insert(tk.END, f"IMC: {round(imc, 1)} ({estado_imc}) | O2: {oxigeno}% | PA: {sis}/{dia} | FC: {fc} lpm\n\n")
    caja_resultados.insert(tk.END, f"Diagnóstico: {diag_texto}\n\n")
    caja_resultados.insert(tk.END, f"Folio: #{folio_final}\n")
    caja_resultados.insert(tk.END, f"Cita: {fecha_final} con {medico_final}\n")
    caja_resultados.insert(tk.END, f"Estado: {estado_cita}\n")

    doc_paciente = {
        "folio": folio_final,
        "nombre": nombre,
        "edad": edad,
        "oxigeno": oxigeno,
        "fc": fc,
        "presion": f"{sis}/{dia}",
        "peso": peso,
        "talla": talla,
        "imc": round(imc, 1),
        "estado_imc": estado_imc,
        "diagnostico": diag_texto,
        "derivacion": derivacion if derivacion else "General",
        "fecha_cita": fecha_final,
        "medico": medico_final,
        "creado_el": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    try:
        coleccion.insert_one(doc_paciente)
        messagebox.showinfo("MongoDB Atlas", f"Cita #{folio_final} registrada exitosamente en la base de datos.")
    except Exception as err:
        messagebox.showerror("Error al guardar", f"No se pudo guardar en MongoDB: {err}")
        return

    limpiar_formulario()
    generar_cita_aleatoria()
    actualizar_encabezado_cita()
    refrescar_tabla()

def limpiar_formulario():
    entry_nombre.delete(0, tk.END)
    entry_edad.delete(0, tk.END)
    entry_oxigeno.delete(0, tk.END)
    entry_fc.delete(0, tk.END)
    entry_presion.delete(0, tk.END)
    entry_peso.delete(0, tk.END)
    entry_talla.delete(0, tk.END)
    caja_resultados.delete(1.0, tk.END)

def actualizar_encabezado_cita():
    lbl_cita_info.config(text=f"Folio: #{num_cita_original} | Fecha: {fecha_str}\nMédico General: {doc_asignado}")

def refrescar_tabla():
    for fila in tabla.get_children():
        tabla.delete(fila)

    try:
        registros = list(coleccion.find({"folio": {"$exists": True}}).sort("creado_el", -1))
        for item in registros:
            tabla.insert("", tk.END, values=(
                item.get("folio", ""),
                item.get("nombre", ""),
                item.get("edad", ""),
                item.get("presion", ""),
                item.get("imc", ""),
                item.get("derivacion", "General"),
                item.get("diagnostico", ""),
                item.get("fecha_cita", ""),
                item.get("medico", "")
            ))
    except Exception as e:
        messagebox.showerror("Error de lectura", f"No se pudieron consultar los datos: {e}")

def al_seleccionar_fila(event):
    seleccion = tabla.selection()
    if not seleccion:
        return
    item = tabla.item(seleccion[0])
    folio_sel = item["values"][0]

    try:
        paciente = coleccion.find_one({"folio": int(folio_sel)})
        if paciente:
            edit_folio.config(state="normal")
            edit_folio.delete(0, tk.END)
            edit_folio.insert(0, str(paciente.get("folio", "")))
            edit_folio.config(state="readonly")

            edit_nombre.delete(0, tk.END)
            edit_nombre.insert(0, paciente.get("nombre", ""))

            edit_diagnostico.delete(0, tk.END)
            edit_diagnostico.insert(0, paciente.get("diagnostico", ""))

            edit_area.delete(0, tk.END)
            edit_area.insert(0, paciente.get("derivacion", ""))

            edit_fecha.delete(0, tk.END)
            edit_fecha.insert(0, paciente.get("fecha_cita", ""))
    except Exception as e:
        messagebox.showerror("Error", f"Error al cargar registro: {e}")

def modificar_registro():
    folio_txt = edit_folio.get()
    if not folio_txt:
        messagebox.showwarning("Aviso", "Selecciona una cita de la tabla para editar.")
        return

    folio_num = int(folio_txt)
    nuevo_nombre = edit_nombre.get().strip()
    nuevo_diag = edit_diagnostico.get().strip()
    nueva_area = edit_area.get().strip()
    nueva_fecha = edit_fecha.get().strip()

    if not nuevo_nombre:
        messagebox.showerror("Error", "El nombre no puede estar vacío.")
        return

    try:
        res = coleccion.update_one(
            {"folio": folio_num},
            {"$set": {
                "nombre": nuevo_nombre,
                "diagnostico": nuevo_diag,
                "derivacion": nueva_area,
                "fecha_cita": nueva_fecha
            }}
        )
        if res.modified_count > 0:
            messagebox.showinfo("Actualizado", f"Cita #{folio_num} actualizada en MongoDB.")
        else:
            messagebox.showinfo("Aviso", "No se realizaron cambios.")
        refrescar_tabla()
    except Exception as e:
        messagebox.showerror("Error al actualizar", f"Error en MongoDB: {e}")

# 5. DELETE: ELIMINAR DE MONGODB
def eliminar_registro():
    folio_txt = edit_folio.get()
    if not folio_txt:
        messagebox.showwarning("Aviso", "Selecciona una cita de la tabla para eliminar.")
        return

    folio_num = int(folio_txt)
    confirmar = messagebox.askyesno("Confirmar", f"¿Eliminar permanentemente la cita #{folio_num} de MongoDB?")
    if confirmar:
        try:
            coleccion.delete_one({"folio": folio_num})
            messagebox.showinfo("Eliminado", f"Cita #{folio_num} eliminada de la base de datos.")
            
            edit_folio.config(state="normal")
            edit_folio.delete(0, tk.END)
            edit_folio.config(state="readonly")
            edit_nombre.delete(0, tk.END)
            edit_diagnostico.delete(0, tk.END)
            edit_area.delete(0, tk.END)
            edit_fecha.delete(0, tk.END)

            refrescar_tabla()
        except Exception as e:
            messagebox.showerror("Error al eliminar", f"No se pudo eliminar en MongoDB: {e}")


ventana = tk.Tk()
ventana.title("Hospital Médica MIA ")
ventana.geometry("1120x680")

col_izquierda = tk.LabelFrame(ventana, text=" Registro de Pacientes ", padx=10, pady=10)
col_izquierda.place(x=10, y=10, width=430, height=655)

lbl_cita_info = tk.Label(col_izquierda, text=f"Folio: #{num_cita_original} | Fecha: {fecha_str}\nMédico General: {doc_asignado}", fg="darkred", font=("Arial", 9, "bold"))
lbl_cita_info.pack(pady=4)

tk.Label(col_izquierda, text="-"*45).pack(pady=2)

f_campos = tk.Frame(col_izquierda)
f_campos.pack(fill="x", pady=2)

tk.Label(f_campos, text="Nombre:").grid(row=0, column=0, sticky="w", pady=2)
entry_nombre = tk.Entry(f_campos, width=24)
entry_nombre.grid(row=0, column=1, sticky="w", pady=2)

tk.Label(f_campos, text="Edad:").grid(row=1, column=0, sticky="w", pady=2)
entry_edad = tk.Entry(f_campos, width=10)
entry_edad.grid(row=1, column=1, sticky="w", pady=2)

tk.Label(f_campos, text="Oxígeno (%):").grid(row=2, column=0, sticky="w", pady=2)
entry_oxigeno = tk.Entry(f_campos, width=10)
entry_oxigeno.grid(row=2, column=1, sticky="w", pady=2)

tk.Label(f_campos, text="FC (lpm):").grid(row=3, column=0, sticky="w", pady=2)
entry_fc = tk.Entry(f_campos, width=10)
entry_fc.grid(row=3, column=1, sticky="w", pady=2)

tk.Label(f_campos, text="Presión (ej. 120/80):").grid(row=4, column=0, sticky="w", pady=2)
entry_presion = tk.Entry(f_campos, width=12)
entry_presion.grid(row=4, column=1, sticky="w", pady=2)

tk.Label(f_campos, text="Peso (kg):").grid(row=5, column=0, sticky="w", pady=2)
entry_peso = tk.Entry(f_campos, width=10)
entry_peso.grid(row=5, column=1, sticky="w", pady=2)

tk.Label(f_campos, text="Estatura (m):").grid(row=6, column=0, sticky="w", pady=2)
entry_talla = tk.Entry(f_campos, width=10)
entry_talla.grid(row=6, column=1, sticky="w", pady=2)

tk.Button(col_izquierda, text="Diagnosticar y Guardar en Mongo", command=procesar_datos,
          bg="#236B8E", fg="white", font=("Arial", 10, "bold")).pack(pady=8)

caja_resultados = tk.Text(col_izquierda, height=13, width=48, font=("Consolas", 9))
caja_resultados.pack(pady=3)

col_derecha = tk.LabelFrame(ventana, text=" Consultar Citas en Base de Datos (MongoDB) ", padx=10, pady=10)
col_derecha.place(x=450, y=10, width=655, height=655)

cols = ("Folio", "Nombre", "Edad", "PA", "IMC", "Área", "Diagnóstico", "Fecha Cita", "Médico")
tabla = ttk.Treeview(col_derecha, columns=cols, show="headings", height=12)

anchos = {"Folio": 55, "Nombre": 95, "Edad": 40, "PA": 55, "IMC": 45, "Área": 75, "Diagnóstico": 120, "Fecha Cita": 90, "Médico": 90}
for c in cols:
    tabla.heading(c, text=c)
    tabla.column(c, width=anchos[c], anchor="center" if c in ["Folio", "Edad", "PA", "IMC"] else "w")

scrollbar_x = ttk.Scrollbar(col_derecha, orient="horizontal", command=tabla.xview)
tabla.configure(xscrollcommand=scrollbar_x.set)
tabla.pack(fill="x")
scrollbar_x.pack(fill="x", pady=2)

tabla.bind("<<TreeviewSelect>>", al_seleccionar_fila)

f_edicion = tk.LabelFrame(col_derecha, text=" Opciones de Registro Seleccionado ", padx=10, pady=8)
f_edicion.pack(fill="x", pady=10)

tk.Label(f_edicion, text="Folio:").grid(row=0, column=0, sticky="w")
edit_folio = tk.Entry(f_edicion, width=10, state="readonly")
edit_folio.grid(row=0, column=1, sticky="w", padx=4, pady=2)

tk.Label(f_edicion, text="Nombre:").grid(row=0, column=2, sticky="w")
edit_nombre = tk.Entry(f_edicion, width=22)
edit_nombre.grid(row=0, column=3, sticky="w", padx=4, pady=2)

tk.Label(f_edicion, text="Diagnóstico:").grid(row=1, column=0, sticky="w")
edit_diagnostico = tk.Entry(f_edicion, width=45)
edit_diagnostico.grid(row=1, column=1, columnspan=3, sticky="w", padx=4, pady=2)

tk.Label(f_edicion, text="Área:").grid(row=2, column=0, sticky="w")
edit_area = tk.Entry(f_edicion, width=15)
edit_area.grid(row=2, column=1, sticky="w", padx=4, pady=2)

tk.Label(f_edicion, text="Fecha Cita:").grid(row=2, column=2, sticky="w")
edit_fecha = tk.Entry(f_edicion, width=22)
edit_fecha.grid(row=2, column=3, sticky="w", padx=4, pady=2)

f_btns = tk.Frame(col_derecha)
f_btns.pack(pady=5)

tk.Button(f_btns, text="Actualizar Registro", command=modificar_registro, bg="#2E8B57", fg="white", font=("Arial", 9, "bold")).pack(side="left", padx=6)
tk.Button(f_btns, text="Eliminar Registro", command=eliminar_registro, bg="#B22222", fg="white", font=("Arial", 9, "bold")).pack(side="left", padx=6)
tk.Button(f_btns, text="Recargar Tabla", command=refrescar_tabla, bg="#4682B4", fg="white", font=("Arial", 9, "bold")).pack(side="left", padx=6)

refrescar_tabla()

ventana.mainloop()