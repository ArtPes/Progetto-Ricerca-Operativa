from helpers.utils import *
from helpers.struct import *


def check_aciclico(grafo_new,len_nodi,durate,lista_nodi,max_makespan):
    # TODO: da implementare
    return True


def copia_grafo(grafo, len_nodi):
    # creo un nuovo grafo
    h, w = len_nodi, len_nodi
    grafo_new = [[0 for x in range(h)] for y in range(w)]
    # inseriesco i valori del vecchio grafo nel nuovo
    for i in range(0, len_nodi):
        for j in range(0, len_nodi):
            grafo_new[i][j] = grafo[i][j]
    return grafo_new


def soluzione_iniziale(grafo, grafo_fixed, lista_nodi,durate):

    len_nodi = len(lista_nodi)
    # creo nuovo grafo a partitrre dai valori del vecchio grafo
    grafo_new = copia_grafo(grafo, len_nodi)

    for i in range(0, len_nodi):
        trovato = False
        for j in range(0, len_nodi):
            if lista_nodi[i].visita == lista_nodi[j].visita and j > i and not trovato:
                if not grafo_fixed[i][j]:
                    trovato = True
                    grafo_new[i][j] = 1
                    grafo_new[j][i] = -1
                    print("Inserito arco tra: "+str(lista_nodi[i].idN)+"-->"+str(lista_nodi[j].idN))
                else:
                    trovato = True
                    print("Arco già inserito")

    max = 0
    for i in range(0,5):
        if durate[i]>max:
            max = durate[i]

    max_makespan = max*len_nodi
    print("Massimo makespan è:"+str(max_makespan))
    aciclico = check_aciclico(grafo_new,len_nodi,durate,lista_nodi,max_makespan)

    if aciclico:
        print("Non è aciclico, soluzione ok!")
    else:
        print("E' aciclico !!!!!!!!!")

    return grafo_new