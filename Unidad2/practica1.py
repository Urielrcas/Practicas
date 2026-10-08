import tkinter as tk
from tkinter import ttk

# Estados y conexiones (forma de arbol)
#
#             A
#           /   \
#          B     C
#         / \   / \
#        D   E F   G
#
estados = ["A", "B", "C", "D", "E", "F", "G"]

acciones = {
    "A": ["B", "C"],
    "B": ["A", "D", "E"],
    "C": ["A", "F", "G"],
    "D": ["B"],
    "E": ["B"],
    "F": ["C"],
    "G": ["C"],
}

# Posicion de cada punto en el arbol
posiciones = {
    "A": (200, 40),
    "B": (110, 110), "C": (290, 110),
    "D": (60, 180), "E": (160, 180), "F": (240, 180), "G": (340, 180),
}


# Busqueda en anchura
def busqueda_anchura(inicio, objetivo):
    cola = [[inicio]]
    visitados = set()
    pasos = []

    while cola:
        camino = cola.pop(0)
        actual = camino[-1]

        if actual in visitados:
            continue

        visitados.add(actual)
        pasos.append(camino)

        if actual == objetivo:
            return camino, pasos

        for vecino in acciones[actual]:
            if vecino not in visitados:
                cola.append(camino + [vecino])

    return None, pasos


# Texto de cada movimiento
def narrar(anterior, camino):
    if anterior is None:
        return "Empiezas en " + camino[0]

    if anterior[-1] == camino[-2]:
        return "Te mueves de " + anterior[-1] + " a " + camino[-1]

    # Si no es vecino directo, regresa por donde vino
    return "Regresas a " + camino[-2] + " y te mueves a " + camino[-1]


# Dibujar el mapa
def dibujar(colores={}):
    canvas.delete("all")

    for origen in acciones:
        for destino in acciones[origen]:
            x1, y1 = posiciones[origen]
            x2, y2 = posiciones[destino]
            canvas.create_line(x1, y1, x2, y2, width=2)

    for estado in posiciones:
        x, y = posiciones[estado]
        color = colores.get(estado, "white")
        canvas.create_oval(x - 20, y - 20, x + 20, y + 20, fill=color, width=2)
        canvas.create_text(x, y, text=estado, font=("Arial", 12, "bold"))


def buscar():
    global solucion, pasos, visitados
    solucion, pasos = busqueda_anchura(combo_inicio.get(), combo_objetivo.get())
    visitados = []
    texto.delete("1.0", tk.END)
    boton.config(state="disabled")
    mostrar_paso(0)


def mostrar_paso(i):
    if i < len(pasos):
        camino = pasos[i]
        anterior = pasos[i - 1] if i > 0 else None

        colores = {e: "lightblue" for e in visitados}
        colores[camino[-1]] = "yellow"
        dibujar(colores)

        texto.insert(tk.END, narrar(anterior, camino) + "\n")
        visitados.append(camino[-1])
        ventana.after(1000, mostrar_paso, i + 1)
    else:
        if solucion:
            colores = {e: "lightblue" for e in visitados}
            for e in solucion:
                colores[e] = "lightgreen"
            dibujar(colores)
            texto.insert(tk.END, "\nObjetivo encontrado\n")
            texto.insert(tk.END, "Ruta: " + " -> ".join(solucion) + "\n")
            texto.insert(tk.END, "Movimientos: " + str(len(solucion) - 1))
        else:
            texto.insert(tk.END, "\nNo se encontro solucion")
        boton.config(state="normal")


# Ventana
ventana = tk.Tk()
ventana.title("Busqueda en Anchura")

frame = tk.Frame(ventana)
frame.pack(pady=10)

tk.Label(frame, text="Inicio:").grid(row=0, column=0)
combo_inicio = ttk.Combobox(frame, values=estados, state="readonly", width=4)
combo_inicio.set("A")
combo_inicio.grid(row=0, column=1, padx=5)

tk.Label(frame, text="Objetivo:").grid(row=0, column=2)
combo_objetivo = ttk.Combobox(frame, values=estados, state="readonly", width=4)
combo_objetivo.set("G")
combo_objetivo.grid(row=0, column=3, padx=5)

boton = tk.Button(frame, text="Buscar", command=buscar)
boton.grid(row=0, column=4, padx=10)

canvas = tk.Canvas(ventana, width=400, height=220, bg="white")
canvas.pack(padx=10)

texto = tk.Text(ventana, width=45, height=10)
texto.pack(padx=10, pady=10)

dibujar()
ventana.mainloop()