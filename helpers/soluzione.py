from helpers.utils import *
from helpers.struct import *

def check_aciclico(grafo, durate, lista_nodi, max_makespan):
    costo = []
    nodi_visita = UnorderedList()
    nodi_visita.add(0)

    # array di 0 per confrontare i costi
    for i in range(0, len(lista_nodi)):
        costo.append(0)

    while not nodi_visita.isEmpty():
        item = nodi_visita.getFirst()
        nodo = item.data
        for i in range(0, len(lista_nodi)):
            if grafo[nodo][i] == 1:
                if not nodi_visita.search(i):
                    nodi_visita.add(i)
                    test = lista_nodi[nodo].visita
                    if costo[nodo] + durate[test] >= costo[i]:
                        costo[i] = durate[test] + costo[nodo]
                    if costo[i]>=max_makespan:
                        return False
        nodi_visita.remove(nodo)
    return True

def copia_grafo_booleano(grafo, len_nodi):
    # creo un nuovo grafo
    h, w = len_nodi, len_nodi
    grafo_new = [[0 for x in range(h)] for y in range(w)]
    # inseriesco i valori del vecchio grafo nel nuovo
    for i in range(0, len_nodi):
        for j in range(0, len_nodi):
            if grafo[i][j] == True:
                grafo_new[i][j] = '0'
            else:
                grafo_new[i][j] = '_'
    return grafo_new

def copia_grafo(grafo, len_nodi):
    # creo un nuovo grafo
    h, w = len_nodi, len_nodi
    grafo_new = [[0 for x in range(h)] for y in range(w)]
    # inseriesco i valori del vecchio grafo nel nuovo
    for i in range(0, len_nodi):
        for j in range(0, len_nodi):
            grafo_new[i][j] = grafo[i][j]
    return grafo_new

def soluzione_iniziale(grafo, grafo_fixed, lista_nodi, durate):
    len_nodi = len(lista_nodi)
    # creo nuovo grafo a partire dai valori del vecchio grafo
    grafo_new = copia_grafo(grafo, len_nodi)

    for i in range(0, len_nodi):
        trovato = False
        for j in range(0, len_nodi):
            if lista_nodi[i].visita == lista_nodi[j].visita and j > i and not trovato:
                if grafo_fixed[i][j]:
                    trovato = True
                    grafo_new[i][j] = 1
                    grafo_new[j][i] = -1
                    print("Inserito arco tra: " + str(lista_nodi[i].idN) + "-->" + str(lista_nodi[j].idN))
    max = 0
    for i in range(0, 5):
        if durate[i] > max:
            max = durate[i]

    max_makespan = max * len_nodi
    print("\nMassimo makespan è:" + str(max_makespan))
    aciclico = check_aciclico(grafo_new, durate, lista_nodi, max_makespan)
    if aciclico:
        print("\nNon è ciclico, soluzione ok!")
    else:
        print("\nE' ciclico, vi è un LOOP !!!!!!!!!")

    return grafo_new

def critical_path(grafo, nodi):
    costo = []
    nodi_visita = UnorderedList()
    nodi_visita.add(0)
    durate = [1,2,4,6,8,0]
    # array di 0 per confrontare i costi
    for i in range(0, len(nodi)):
        costo.append(0)

    while not nodi_visita.isEmpty():
        item = nodi_visita.getFirst()
        nodo = item.data
        for i in range(0, len(nodi)):
            if grafo[nodo][i] == 1:
                if not nodi_visita.search(i):
                    nodi_visita.add(i)
                    test = nodi[i].visita
                    if test == -1: #se prossimo nodo è quello di fine
                        test = 5
                    if costo[nodo] + durate[test] >= costo[i]:
                        costo[i] = durate[test] + costo[nodo]
        nodi_visita.remove(nodo)
    '''
    nodi_visita = []
    nodi_visita.append(0)
    while nodi_visita:
        nodo = nodi_visita[0]
        for i in range(0, len(nodi)):
            if grafo[nodo][i] == 1:
                if not i in nodi_visita:
                    nodi_visita.append(i)
                    test = nodi[i].visita
                    if test == -1:
                        test = 5
                    if costo[nodo] + durate[test] >= costo[i]:
                        costo[i] = durate[test] + costo[nodo]
        nodi_visita.remove(nodo)
        
        '''
    #print(costo)
    max = massimo(costo)
    return max

def massimo(lista):
    a=0
    for i in range(0,len(lista)):
        if lista[i]>a:
            a=lista[i]
    return a

def trova_archi(nodi,len_nodi,grafo_disgiuntivo):
    lista = []
    for i in range(1,len_nodi):
        for j in range(1,len_nodi):
            if grafo_disgiuntivo[i][j] and i<j:
                lista.append(Arco(nodi[i].visita,i,j))
    return lista

def tabu_search(grafo_candidato,makespan_candidato,grafo_disgiuntivo,
                nodi, durate):
    makespan_temp_s = 0
    makespan_temp_r = 0
    makespan_candidato_temp = makespan_candidato

    grafo_partenza = copia_grafo(grafo_candidato,len(nodi))

    tabu_list = UnorderedList()
    archi_da_decidere = UnorderedList()

    # archi su cui apporto decisioni
    archi_da_decidere = trova_archi(nodi,len(nodi),grafo_disgiuntivo)

    for a in archi_da_decidere:
        print("Visita: "+str(a.visita)+" Archi: "+str(a.primo_estremo)+","+str(a.secondo_estremo))

    capacita = len(durate)/2+len(archi_da_decidere)/10

    # numero massimo di iterazioni della tabu search, volendo possiamo impostarlo noi staticamente
    iterazioni = len(nodi)*len(archi_da_decidere)

    max=0
    for i in range(0,len(durate)):
        if durate[i]>max:
            max = durate[i]
    max_makespan = max * len(nodi)

    # while iterazioni>0:
    #    iterazioni -= iterazioni

