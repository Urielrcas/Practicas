import sys

print("=" * 55)
print("       SISTEMA DE AUTORIZACIÓN PARA EXAMEN")
print("=" * 55)

# ----------------------------------------------------------
# 1. ENTRADA DE DATOS
# ----------------------------------------------------------

lista_oficial = input(
    "¿Aparece en la lista oficial? (si/no): "
).lower()

if lista_oficial != "si":
    print ("El alumno no puede presentar el examen ya que no esta en la lista")
    sys.exit()

asistencia = float(input("Ingresa el porcentaje de asistencia: "))
promedio = float(input("Ingresa el promedio: "))

proyecto = input(
    "¿Entregó el proyecto? (si/no): "
).lower()

adeudos = input(
    "¿Tiene adeudos? (si/no): "
).lower()

autorizacion = input(
    "¿Tiene autorización especial? (si/no): "
).lower()




# P: El alumno tiene asistencia suficiente
P = asistencia >= 80

# Q: El alumno tiene promedio aprobatorio
Q = promedio >= 8

# R: El alumno entregó el proyecto
R = proyecto == "si"

# S: El alumno NO tiene adeudos
S = adeudos == "no"

# T: El alumno tiene autorización especial
T = autorizacion == "si"

# U: El alumno aparece en la lista oficial
U = lista_oficial == "si"


# ----------------------------------------------------------
# 3. MOSTRAR LAS PROPOSICIONES
# ----------------------------------------------------------

print("\n" + "=" * 55)
print("             VALORES DE LAS PROPOSICIONES")
print("=" * 55)

print("P - Asistencia suficiente :", P)
print("Q - Promedio aprobatorio :", Q)
print("R - Proyecto entregado   :", R)
print("S - Sin adeudos          :", S)
print("T - Autorización especial:", T)
print("U - Aparece en lista     :", U)


# ==========================================================
# 4. NEGACIÓN
# ==========================================================


no_P = not P

print("\nNEGACIÓN")
print("¬P =", no_P)


# ==========================================================
# 5. CONJUNCIÓN
# ==========================================================



conjuncion = P and Q

print("\nCONJUNCIÓN")
print("P ∧ Q =", conjuncion)


# ==========================================================
# 6. DISYUNCIÓN
# ==========================================================


disyuncion = Q or T

print("\nDISYUNCIÓN")
print("Q ∨ T =", disyuncion)


# ==========================================================
# 7. CONDICIONAL
# ==========================================================

# El condicional:

# P → Q = (NOT P) OR Q

condicional = (not P) or Q

print("\nCONDICIONAL")
print("P → Q =", condicional)


# ==========================================================
# 8. BICONDICIONAL
# ==========================================================

bicondicional = P == Q

print("\nBICONDICIONAL")
print("P ↔ Q =", bicondicional)


# ==========================================================
# 9. EXPRESIÓN CON PARÉNTESIS
# ==========================================================


resultado = (P and Q and R and S and U) or T

print("\nEXPRESIÓN CON PARÉNTESIS")
print("(P ∧ Q ∧ R ∧ S ∨ T ) ∧ U=", resultado)


# ==========================================================
# 10. BICONDICIONAL PARA AUTORIZACIÓN
# ==========================================================


autorizacion_correcta = T == U

print("\nBICONDICIONAL DE AUTORIZACIÓN")
print("T ↔ U =", autorizacion_correcta)


# ==========================================================
# 11. RESULTADO FINAL
# ==========================================================

print("\n" + "=" * 55)
print("                  RESULTADO FINAL")
print("=" * 55)

if resultado:
    print("El alumno PUEDE presentar el examen.")
else:
    print("El alumno NO puede presentar el examen.")

if autorizacion_correcta:
    print("La autorización COINCIDE con la lista oficial.")
else:
    print("ADVERTENCIA: La autorización NO coincide con la lista oficial.")