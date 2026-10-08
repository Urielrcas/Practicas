pro = int(input("Cuantas proposiciones se van a evaluar: "))
valor = [True, False]

if pro == 2:
    print("P \t Q \t P AND Q \t P OR Q")
    print("-" * 50)
    for P in valor:
        for Q in valor:
            resultado_and = P and Q
            resultado_or = P or Q
            print(P, "\t", Q, "\t", resultado_and, "\t\t", resultado_or)

elif pro == 3:
    print("P \t Q \t R \t AND  \t OR ")
    print("-" * 65)
    for P in valor:
        for Q in valor:
            for R in valor:
                resultado_and = P and Q and R
                resultado_or = P or Q or R
                print(P, "\t", Q, "\t", R, "\t", resultado_and, "\t\t", resultado_or)

elif pro == 4:
    print("P \t Q \t R \t S \t AND \t OR ")
    print("-" * 80) 
    for P in valor:
        for Q in valor:
            for R in valor:
                for S in valor:
                    resultado_and = P and Q and R and S
                    resultado_or = P or Q or R or S
                    
                    print(P, "\t", Q, "\t", R, "\t", S, "\t", resultado_and, "\t\t", resultado_or)
else:
    print("Este programa solo soporta 2, 3 o 4 proposiciones.")