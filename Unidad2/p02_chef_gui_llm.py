# ============================================================
# PRACTICA 2 (MODIFICADA)
# ASISTENTE CHEF Y NUTRICIÓN CON LLM + INTERFAZ GRÁFICA
# ============================================================
#
# Objetivo:
# Implementar un LLM ejecutado mediante Ollama, con:
#
#   1. Una configuración de sistema diferente
#      (Chef y asesor de nutrición).
#   2. Una interfaz gráfica (Tkinter) para interactuar
#      de forma más intuitiva.
#   3. Un breve resumen del historial para el usuario.
#
# Modelos (seleccionables desde la interfaz):
# llama3.2  y  llama3.2:1b
#
# Requisitos:
#   pip install ollama
#   ollama pull llama3.2
#   ollama pull llama3.2:1b
#
# ============================================================


# ------------------------------------------------------------
# 1. IMPORTAR LAS BIBLIOTECAS
# ------------------------------------------------------------

import threading
import tkinter as tk
from tkinter import scrolledtext, messagebox

import ollama


# ------------------------------------------------------------
# 2. CONFIGURACIÓN DEL MODELO
# ------------------------------------------------------------

#
# El usuario puede elegir el modelo desde la interfaz.
# El modelo chico (1b) es más rápido en equipos sin
# tarjeta gráfica, aunque sus respuestas son más simples.
#
# ------------------------------------------------------------

MODELOS = {
    "Llama Pro": "llama3.2",        # 3B  - mejor calidad
    "Llama Flash": "llama3.2:1b"    # 1B  - más rápido
}

MODELO = "llama3.2"


# ------------------------------------------------------------
# 3. CONFIGURACIÓN DEL SISTEMA (NUEVO ROL)
# ------------------------------------------------------------
#
# En lugar de un profesor de IA, ahora el asistente será
# un chef profesional con conocimientos de nutrición.
#
# ------------------------------------------------------------

mensaje_sistema = """
Eres "Chef Nutri", un chef profesional y asesor de nutrición.

Tu función es ayudar a las personas a cocinar de forma
sencilla, económica y saludable.

Debes:

1. Sugerir recetas con los ingredientes que el usuario tenga.
2. Dar la lista de ingredientes con cantidades aproximadas.
3. Explicar la preparación paso a paso y numerada.
4. Indicar el tiempo aproximado de preparación.
5. Dar un dato nutricional breve (calorías aproximadas,
   proteínas o beneficios).
6. Proponer sustituciones si falta algún ingrediente o si
   el usuario tiene alguna restricción (vegetariano,
   sin gluten, diabetes, etc.).
7. Responder siempre en español y de forma amable.
8. Si te preguntan algo que no sea de cocina o nutrición,
   indica amablemente que solo puedes ayudar con esos temas.
"""


# ------------------------------------------------------------
# 4. CREAR HISTORIAL
# ------------------------------------------------------------

mensajes = [
    {
        "role": "system",
        "content": mensaje_sistema
    }
]


# ------------------------------------------------------------
# 5. COLORES Y FUENTES DE LA INTERFAZ
# ------------------------------------------------------------

COLOR_FONDO = "#FFF8F0"
COLOR_ENCABEZADO = "#D35400"
COLOR_USUARIO = "#1F618D"
COLOR_CHEF = "#1E8449"
COLOR_SISTEMA = "#7F8C8D"

FUENTE = ("Segoe UI", 11)
FUENTE_TITULO = ("Segoe UI", 16, "bold")


# ============================================================
# 6. FUNCIONES DE LA INTERFAZ
# ============================================================

# ------------------------------------------------------------
# Escribir un mensaje en el área de chat
# ------------------------------------------------------------

def mostrar_mensaje(autor, texto, etiqueta):

    area_chat.config(state="normal")

    area_chat.insert(tk.END, autor + ":\n", etiqueta + "_autor")
    area_chat.insert(tk.END, texto + "\n\n", etiqueta)

    area_chat.config(state="disabled")
    area_chat.see(tk.END)


# ------------------------------------------------------------
# Activar / desactivar controles mientras el LLM responde
# ------------------------------------------------------------

def bloquear_controles(bloquear):

    estado = "disabled" if bloquear else "normal"

    boton_enviar.config(state=estado)
    entrada.config(state=estado)

    barra_menu.entryconfig("Modelo", state=estado)
    barra_menu.entryconfig("Historial", state=estado)

    if bloquear:
        etiqueta_estado.config(text="Chef Nutri está pensando...")
    else:
        etiqueta_estado.config(text="Listo")
        entrada.focus()


# ------------------------------------------------------------
# Enviar la pregunta del usuario
# ------------------------------------------------------------

def enviar_pregunta(event=None):

    pregunta = entrada.get().strip()

    if pregunta == "":
        return

    entrada.delete(0, tk.END)

    mostrar_mensaje("Tú", pregunta, "usuario")

    mensajes.append(
        {
            "role": "user",
            "content": pregunta
        }
    )

    bloquear_controles(True)

    # El LLM se consulta en un hilo aparte para que la
    # ventana no se congele mientras espera la respuesta.

    hilo = threading.Thread(target=consultar_llm, daemon=True)
    hilo.start()


# ------------------------------------------------------------
# Consultar al LLM (se ejecuta en segundo plano)
# ------------------------------------------------------------

def consultar_llm():

    contenido = ""
    iniciada = False

    try:

        # Con stream=True el LLM envía la respuesta en
        # fragmentos pequeños conforme la va generando.

        respuesta = ollama.chat(
            model=MODELO,
            messages=mensajes,
            stream=True
        )

        for fragmento in respuesta:

            texto = fragmento["message"]["content"]

            if not iniciada:
                ventana.after(0, iniciar_respuesta)
                iniciada = True

            contenido += texto

            ventana.after(0, agregar_fragmento, texto)

        mensajes.append(
            {
                "role": "assistant",
                "content": contenido
            }
        )

        ventana.after(0, terminar_respuesta)

    except Exception as error:

        # Eliminamos la pregunta del historial porque
        # no pudo ser procesada.

        mensajes.pop()

        if iniciada:
            ventana.after(0, agregar_fragmento, "\n\n")

        ventana.after(0, mostrar_error, error)


# ------------------------------------------------------------
# Mostrar la respuesta mientras se escribe
# ------------------------------------------------------------

def iniciar_respuesta():

    etiqueta_estado.config(text="Chef Nutri está escribiendo...")

    area_chat.config(state="normal")
    area_chat.insert(tk.END, "Chef Nutri:\n", "chef_autor")
    area_chat.config(state="disabled")


def agregar_fragmento(texto):

    area_chat.config(state="normal")
    area_chat.insert(tk.END, texto, "chef")
    area_chat.config(state="disabled")
    area_chat.see(tk.END)


def terminar_respuesta():

    agregar_fragmento("\n\n")
    actualizar_contador()
    bloquear_controles(False)


def mostrar_error(error):

    mostrar_mensaje(
        "Sistema",
        "ERROR AL CONECTARSE CON EL LLM\n"
        + str(error)
        + "\nVerifica que Ollama esté ejecutándose.",
        "sistema"
    )

    bloquear_controles(False)


# ============================================================
# 7. RESUMEN DEL HISTORIAL
# ============================================================
#
# El resumen tiene dos partes:
#
#   a) Estadísticas locales (no requieren al LLM):
#      número de preguntas y lista de temas consultados.
#
#   b) Un resumen breve generado por el propio LLM
#      a partir de toda la conversación.
#
# ------------------------------------------------------------

def obtener_preguntas():

    return [m["content"] for m in mensajes if m["role"] == "user"]


def resumen_local():

    preguntas = obtener_preguntas()

    texto = "Preguntas realizadas: " + str(len(preguntas)) + "\n"
    texto += "Temas consultados:\n"

    for i, pregunta in enumerate(preguntas, start=1):

        # Recortamos preguntas largas para que el resumen
        # sea breve.

        if len(pregunta) > 60:
            pregunta = pregunta[:60] + "..."

        texto += "  " + str(i) + ". " + pregunta + "\n"

    return texto


def generar_resumen():

    if len(obtener_preguntas()) == 0:

        messagebox.showinfo(
            "Resumen del historial",
            "Aún no hay conversación para resumir."
        )

        return

    bloquear_controles(True)
    etiqueta_estado.config(text="Generando resumen...")

    hilo = threading.Thread(target=consultar_resumen, daemon=True)
    hilo.start()


def consultar_resumen():

    # Construimos una petición aparte para NO alterar el
    # historial principal de la conversación.

    conversacion = ""

    for m in mensajes[1:]:

        autor = "Usuario" if m["role"] == "user" else "Chef"
        conversacion += autor + ": " + m["content"] + "\n"

    peticion = [
        {
            "role": "system",
            "content": "Resumes conversaciones en español de forma "
                       "muy breve (máximo 5 viñetas)."
        },
        {
            "role": "user",
            "content": "Resume la siguiente conversación indicando "
                       "qué recetas o consejos se dieron:\n\n"
                       + conversacion
        }
    ]

    try:

        respuesta = ollama.chat(model=MODELO, messages=peticion)
        resumen_llm = respuesta["message"]["content"]

    except Exception as error:

        resumen_llm = "(No se pudo generar con el LLM: " + str(error) + ")"

    texto = resumen_local() + "\nResumen de la conversación:\n" + resumen_llm

    ventana.after(0, mostrar_resumen, texto)


def mostrar_resumen(texto):

    bloquear_controles(False)
    mostrar_mensaje("Resumen del historial", texto, "sistema")


# ------------------------------------------------------------
# Otras acciones
# ------------------------------------------------------------

def nueva_conversacion():

    if messagebox.askyesno("Nueva conversación",
                           "¿Deseas borrar el historial actual?"):

        del mensajes[1:]

        area_chat.config(state="normal")
        area_chat.delete("1.0", tk.END)
        area_chat.config(state="disabled")

        actualizar_contador()
        mensaje_bienvenida()


def cambiar_modelo():

    # El historial se conserva, así que el nuevo modelo
    # continúa la misma conversación.

    global MODELO

    nombre = modelo_elegido.get()
    MODELO = MODELOS[nombre]

    etiqueta_modelo.config(text="Modelo actual: " + nombre)

    mostrar_mensaje(
        "Sistema",
        "Modelo cambiado a: " + nombre + " (" + MODELO + ")",
        "sistema"
    )


def ver_historial():

    # Abre una ventana aparte con la conversación completa.

    if len(obtener_preguntas()) == 0:

        messagebox.showinfo("Historial", "Aún no hay conversación.")

        return

    ventana_historial = tk.Toplevel(ventana)
    ventana_historial.title("Historial de la conversación")
    ventana_historial.geometry("640x480")

    texto = scrolledtext.ScrolledText(ventana_historial, wrap="word",
                                      font=FUENTE, padx=10, pady=10)
    texto.pack(fill="both", expand=True)

    texto.tag_config("usuario", foreground=COLOR_USUARIO,
                     font=("Segoe UI", 11, "bold"))
    texto.tag_config("chef", foreground=COLOR_CHEF,
                     font=("Segoe UI", 11, "bold"))

    for m in mensajes[1:]:

        if m["role"] == "user":
            texto.insert(tk.END, "Tú:\n", "usuario")
        else:
            texto.insert(tk.END, "Chef Nutri:\n", "chef")

        texto.insert(tk.END, m["content"] + "\n\n")

    texto.config(state="disabled")


def actualizar_contador():

    etiqueta_contador.config(
        text="Mensajes en historial: " + str(len(mensajes) - 1)
    )


def salir():

    ventana.destroy()


def mensaje_bienvenida():

    mostrar_mensaje(
        "Chef Nutri",
        "¡Hola! Soy tu chef y asesor de nutrición. "
        "Dime qué ingredientes tienes o qué te gustaría cocinar.",
        "chef"
    )


# ============================================================
# 8. CONSTRUCCIÓN DE LA VENTANA
# ============================================================

ventana = tk.Tk()
ventana.title("Chef Nutri - Asistente con LLM")
ventana.geometry("820x640")
ventana.configure(bg=COLOR_FONDO)
ventana.protocol("WM_DELETE_WINDOW", salir)


# ------------------------------------------------------------
# Barra de menú
# ------------------------------------------------------------

barra_menu = tk.Menu(ventana)

# Menú Archivo

menu_archivo = tk.Menu(barra_menu, tearoff=0)
menu_archivo.add_command(label="Salir", command=salir)

barra_menu.add_cascade(label="Archivo", menu=menu_archivo)

# Menú Modelo: solo uno puede estar seleccionado

modelo_elegido = tk.StringVar(value="Llama Pro")

menu_modelo = tk.Menu(barra_menu, tearoff=0)

for nombre in MODELOS:

    menu_modelo.add_radiobutton(
        label=nombre + "  (" + MODELOS[nombre] + ")",
        variable=modelo_elegido,
        value=nombre,
        command=cambiar_modelo
    )

barra_menu.add_cascade(label="Modelo", menu=menu_modelo)

# Menú Historial

menu_historial = tk.Menu(barra_menu, tearoff=0)
menu_historial.add_command(label="Ver historial completo",
                           command=ver_historial)
menu_historial.add_command(label="Resumen del historial",
                           command=generar_resumen)
menu_historial.add_separator()
menu_historial.add_command(label="Nueva conversación",
                           command=nueva_conversacion)

barra_menu.add_cascade(label="Historial", menu=menu_historial)

ventana.config(menu=barra_menu)


# ------------------------------------------------------------
# Encabezado
# ------------------------------------------------------------

encabezado = tk.Frame(ventana, bg=COLOR_ENCABEZADO)
encabezado.pack(fill="x")

tk.Label(
    encabezado,
    text="🍳  CHEF NUTRI - ASISTENTE DE COCINA CON LLM",
    font=FUENTE_TITULO,
    bg=COLOR_ENCABEZADO,
    fg="white",
    pady=10
).pack()

etiqueta_modelo = tk.Label(
    encabezado,
    text="Modelo actual: Llama Pro",
    font=("Segoe UI", 10),
    bg=COLOR_ENCABEZADO,
    fg="white"
)
etiqueta_modelo.pack(pady=(0, 8))


# ------------------------------------------------------------
# Área de chat
# ------------------------------------------------------------

area_chat = scrolledtext.ScrolledText(
    ventana,
    wrap="word",
    font=FUENTE,
    bg="white",
    padx=10,
    pady=10,
    state="disabled"
)
area_chat.pack(fill="both", expand=True, padx=10, pady=10)

area_chat.tag_config("usuario_autor", foreground=COLOR_USUARIO,
                     font=("Segoe UI", 11, "bold"))
area_chat.tag_config("usuario", foreground=COLOR_USUARIO)

area_chat.tag_config("chef_autor", foreground=COLOR_CHEF,
                     font=("Segoe UI", 11, "bold"))
area_chat.tag_config("chef", foreground="black")

area_chat.tag_config("sistema_autor", foreground=COLOR_SISTEMA,
                     font=("Segoe UI", 11, "bold"))
area_chat.tag_config("sistema", foreground=COLOR_SISTEMA)


# ------------------------------------------------------------
# Entrada de texto y botón enviar
# ------------------------------------------------------------

marco_entrada = tk.Frame(ventana, bg=COLOR_FONDO)
marco_entrada.pack(fill="x", padx=10)

entrada = tk.Entry(marco_entrada, font=FUENTE)
entrada.pack(side="left", fill="x", expand=True, ipady=6)
entrada.bind("<Return>", enviar_pregunta)

boton_enviar = tk.Button(
    marco_entrada,
    text="Enviar",
    font=FUENTE,
    bg=COLOR_CHEF,
    fg="white",
    command=enviar_pregunta
)
boton_enviar.pack(side="left", padx=(8, 0))
marco_entrada.pack_configure(pady=(0, 10))


# ------------------------------------------------------------
# Barra de estado
# ------------------------------------------------------------

barra_estado = tk.Frame(ventana, bg="#EAEAEA")
barra_estado.pack(fill="x", side="bottom")

etiqueta_estado = tk.Label(barra_estado, text="Listo",
                           bg="#EAEAEA", anchor="w")
etiqueta_estado.pack(side="left", padx=10)

etiqueta_contador = tk.Label(barra_estado, text="",
                             bg="#EAEAEA", anchor="e")
etiqueta_contador.pack(side="right", padx=10)


# ============================================================
# 9. INICIAR PROGRAMA
# ============================================================

actualizar_contador()
mensaje_bienvenida()
entrada.focus()

ventana.mainloop()


# python -m py_compile Unidad2/p02_chef_gui_llm.py (comprueba la sintaxis)

        #       SYSTEM  (Chef Nutri)
        #         │
        #         ▼
        #    Comportamiento
        #         │
        #         ▼
# USER (GUI) ──► LLM ──► ASSISTANT (GUI)
        #                    │
        #                    ▼
        #            HISTORIAL ──► RESUMEN
