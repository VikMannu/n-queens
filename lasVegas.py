import time
import random
import sys

#variables para controlar el tiempo de ejecucion
maxTime=0.0
iterationTime=0.0

#estructura utilizada
columns = domain = []

#tamanho
tam=0
graficar=0
#variable contador de nodos expandidos
cantNodes=0

def printSolution(solution,tam):
    global graficar
    print(solution)
    if graficar == 1:
        for x in range(tam):
            for i in range(tam):
                if solution[i] == x+1:
                    print ("X", end=" ")
                else:
                    print ("--", end=" ")
            print ("\n")
        print ("\n")

def initArrays():
    global tam, domain, columns
    #inicializamos las columnas con valores por defecto

    domain = list(range(1, tam+1))
    columns = []

def readData():
    global tam, maxTime, iterationTime
    print("Ingrese el nro de reinas: ")
    tam=int(input())

    sys.setrecursionlimit(2000)

    print("Tiempo maximo de espera (s): ")
    enter=input()
    maxTime=float(enter)

    print("Tiempo maximo de espera entre iteraciones (s): ")
    enter=input()
    iterationTime = float(enter)

    print("Desea graficar la solucion encontrada? \n1. Si \n2. No")
    graficar = int(input())


def calculatePositions():
    global domain, columns, maxTime, cantNodes

    #ingresamos los datos de los parametros
    readData()

    #Variables de control del algoritmo
    notSolution=True
    solution=None
    start=end=time.time()

    #si no encuentra solucion que siga buscando mientras haya tiempo
    while end-start<maxTime and solution == None:
        initArrays()
        tiempo=time.time()
        solution=insertQueen(domain, columns, tiempo)
        if solution !=None:
            printSolution(solution,len(solution))
            notSolution=False

        end=time.time()

    if notSolution:
        print("No se encontraron soluciones en el tiempo ", maxTime)

    print("Nodos expandidos: ", cantNodes)
    print("Tiempo transcurrido: ", end-start," s")

def insertQueen(domain, columns, startIteration):
    global iterationTime, cantNodes

    #caso base, las reinas estan en posicion correcta
    if domain == []:
        return columns
    result=None
    #Buscamos una posicion aleatoria para la reina mientras exista alguna disponible que no probamos anteriorme
    notTested=list(domain)
    while notTested!=[] and result == None:
        endIteration=time.time()
        if endIteration-startIteration < iterationTime:
            random.seed(time.time())
            if len(notTested)>1:
                index= random.randint(0,len(notTested)-1)
            else:
                index=0
            position=notTested[index]

            #Actualizamos las posiciones probadas
            notTested.remove(position)

            #contar nodo
            cantNodes+=1

            #validamos la posicion
            if validatePosition(columns, position):
                #Pintamos a la nueva reina
                columns.append(position)
                #removemos del dominio la posicion utilizada
                domain.remove(position)

                result=insertQueen(domain,columns, time.time())
                #si no se encuentra ningun resultado posible
                if result==None:
                    #hacemos backtracking
                    domain.append(position)
                    #eliminamos la posicion que habiamos agregado
                    columns.remove(position)
        else:
            return None
    return result

def validatePosition(columns, position):
    #verificamos las restricciones de la insersion
    if len(columns)>0:
        for i in range(0, len(columns)):
            if not verifyRestriction(position, len(columns)+1, columns[i],i+1):
                return False
    return True

def verifyRestriction(row, column, queenRow, queenColumn):
    #verificar fila
    subtractionRow=row-queenRow
    #verificar columna
    subtractionColumn=column-queenColumn
    div= subtractionRow/subtractionColumn
    #Verificar la diagonal
    if div!= 1 and div!=-1:
        return True
    return False

def main():
    calculatePositions()
main()