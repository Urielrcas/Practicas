"""
==============================================================
Primer Gráfico con Matplotlib
==============================================================
Materia: Extracción de Conocimiento en Bases de Datos
Objetivo: Aprender a construir una gráfica utilizando
Matplotlib.
==============================================================
"""

# ==========================================================
# IMPORTACIÓN DE LIBRERÍAS
# ==========================================================
import matplotlib.pyplot as plt
import numpy as np

# ==========================================================
# DATOS
# ==========================================================
# Meses del año
meses = [
    "Ene", "Feb", "Mar", "Abr",
    "May", "Jun", "Jul", "Ago",
    "Sep", "Oct", "Nov", "Dic"
]

# Ventas simuladas (miles de pesos)
ventas = [85, 90, 96, 105, 120, 135,
          150, 148, 160, 172, 181, 195]

# ==========================================================
# CONFIGURACIÓN GENERAL: ESTABLECE EL TAMAÑO DE LA FIGURA
# ==========================================================
fig, ax = plt.subplots(figsize=(14, 8))

# ==========================================================
# GRÁFICA PRINCIPAL: LÍNEA CON COLOR, GROSOR Y MARCADORES
# ==========================================================
ax.plot(
    meses,
    ventas,
    color="#1f77b4",
    linewidth=3,
    marker="o",
    markersize=9,
    markerfacecolor="white",
    markeredgewidth=2,
    zorder=3,
    label="Ventas mensuales"
)

# ==========================================================
# TÍTULO PRINCIPAL (ARRIBA) Y SUBTÍTULO (DEBAJO)
# ==========================================================
fig.suptitle(
    "Ventas Mensuales de la Empresa EcoMart",
    fontsize=22,
    fontweight="bold",
    y=0.97
)

ax.set_title(
    "Periodo Enero - Diciembre 2026",
    fontsize=13,
    color="gray",
    pad=15
)

# ==========================================================
# ETIQUETAS EN LOS EJES INDICANDO LA VARIABLE Y SUS UNIDADES
# ==========================================================
ax.set_xlabel("Mes", fontsize=15, fontweight="bold")
ax.set_ylabel("Ventas (miles de pesos)", fontsize=15, fontweight="bold")

# Margen extra arriba y abajo para que no se encimen los textos
ax.set_ylim(70, 215)

# ==========================================================
# CUADRÍCULA: FACILITA LA LECTURA DE LOS VALORES
# ==========================================================
ax.grid(linestyle="--", linewidth=0.7, alpha=0.5)

# ==========================================================
# ANOTACIONES: VALOR EXACTO DE CADA OBSERVACIÓN
# (desplazadas y con fondo blanco para que se distingan)
# ==========================================================
for x, y in zip(meses, ventas):
    ax.annotate(
        str(y),
        xy=(x, y),
        xytext=(0, 12),
        textcoords="offset points",
        ha="center",
        fontsize=10,
        fontweight="bold",
        bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="none", alpha=0.8),
        zorder=4
    )

# ==========================================================
# LÍNEA DE PROMEDIO: COMPARA CADA DATO CON EL PROMEDIO ANUAL
# ==========================================================
promedio = np.mean(ventas)

ax.axhline(
    promedio,
    color="red",
    linestyle="--",
    linewidth=2,
    zorder=2,
    label=f"Promedio anual ({promedio:.1f} miles de pesos)"
)

ax.text(
    -0.2,
    promedio + 3,
    f"Promedio anual = {promedio:.1f} miles de pesos",
    color="red",
    fontsize=11
)

# ==========================================================
# DESTACAR EL MÁXIMO: MARCADOR Y FLECHA
# ==========================================================
indice_max = np.argmax(ventas)

ax.scatter(
    meses[indice_max],
    ventas[indice_max],
    color="green",
    s=180,
    zorder=5,
    label="Máximo"
)

ax.annotate(
    f"Mayor venta del año\n({ventas[indice_max]} miles de pesos)",
    xy=(indice_max, ventas[indice_max]),
    xytext=(indice_max - 3.2, 200),
    arrowprops=dict(arrowstyle="->", color="green", lw=2),
    fontsize=12,
    color="green",
    va="center"
)

# ==========================================================
# LEYENDA (AL FINAL PARA QUE INCLUYA TODOS LOS ELEMENTOS)
# ==========================================================
ax.legend(fontsize=12, loc="lower right")

# ==========================================================
# PIE DE FIGURA: FUENTE DE LOS DATOS Y AUTOR
# ==========================================================
fig.text(
    0.01,
    0.01,
    "Conclusión: Estimado de las ventas | Elaboración propia | UTVT",
    fontsize=10,
    color="gray"
)

# ==========================================================
# QUITAR MARCO SUPERIOR Y DERECHO
# ==========================================================
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

# ==========================================================
# AJUSTAR ESPACIOS
# ==========================================================
plt.tight_layout(rect=[0, 0.03, 1, 0.97])

# ==========================================================
# GUARDAR IMAGEN
# ==========================================================
plt.savefig(
    "Grafica_Profesional_01.png",
    dpi=300,
    bbox_inches="tight"
)

# ==========================================================
# MOSTRAR
# ==========================================================
plt.show()

print("=" * 60)
print("Gráfica generada correctamente.")
print("Archivo guardado como:")
print("Grafica_Profesional_01.png")
print("=" * 60)