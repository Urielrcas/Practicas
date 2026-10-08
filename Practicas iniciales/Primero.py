asistencias = float(input("Ingresa tu porcentaje de asistencias: "))
promedio = float(input("Ingresa tu promedio: "))
proyecto= input("Entregaste tu proyecto Si/No: ").lower()

P=asistencias>=80
Q=promedio>=8
R=proyecto=="si"
resultado= P and Q and R
print("Evaluacion")
print(P)
print(Q)
print(R)

if resultado:
    print("Aprobaste")