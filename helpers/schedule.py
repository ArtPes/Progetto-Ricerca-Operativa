from helpers.soluzione import *
from helpers.utils import *


def list_to_mat(list):
    mat = []
    for i in range(0, len(list)):
        mat.append(list[i])
    return mat


def set_the_mat(lists, listp):
    matrixs = []  # matrice per le salette
    matrixp = []  # matrice per i pazienti
    newlistp = []
    for i in range(0, len(lists)):
        matrixs.append(list_to_mat(lists[i]))

    for i in range(0, len(listp)):
        id = listp[i].id
        test = listp[i].test_array
        sala = listp[i].saletta
        newlistp.append(test)

    for j in range(0, len(newlistp)):
        matrixp.append(list_to_mat(newlistp[j]))

    return (matrixp, matrixs)


def crea_nodo(mp, ms):
    # creo nodo da lista pazienti (paz,visita)
    nodi = []
    numn = 0
    ns = Nodo(0, 0, 0, 0)
    nodi.append(ns)
    for i in range(0, len(mp)):
        for j in range(0, len(mp[i])):
            numn += 1
            nd = Nodo(numn, i + 1, mp[i][j] + 1, 0)

            nodi.append(nd)

    for i in range(0, len(nodi)):
        for k in range(0, len(ms)):
            for j in range(0, len(ms[k])):
                if ms[k][j] == nodi[i].idP:
                    nodi[i].sala = k + 1
    nd = Nodo(numn + 1, 0, 0, 0)
    nodi.append(nd)

    return nodi, numn


def stampa3(matr):
    for i in range(0, len(matr)):
        print(i, end="   ", flush=True)
    print("\r")
    for i in range(0, len(matr)):
        print(str(i) + "  " + str(matr[i]))


def stampa_bool(matrix):
    matr = copia_grafo_booleano(matrix, len(matrix))
    for i in range(0, len(matr)):
        print(" -  " + str(i), end="", flush=True)
    print("\r")
    for i in range(0, len(matr)):
        print(str(i) + "  " + str(matr[i]))


def create_mat(nodi):
    dim = len(nodi)
    mat = [[0 for i in range(0, dim)] for j in range(0, dim)]
    return mat


def create_mat_bool(nodi):
    matbool = [[0 for i in range(0, len(nodi))] for j in range(0, len(nodi))]
    '''
    mette a True i nodi che:
        - hanno stesso paziente e ovviamente job diversi
    '''
    for i in range(0, len(nodi)):
        for j in range(0, len(nodi)):
            if nodi[i].idP == nodi[j].idP and nodi[i].visita != nodi[
                j].visita:  # nodi che condividono lo stesso paziente hanno archi disgiuntivi
                matbool[i][j] = True
            else:
                matbool[i][j] = False  # tutto il resto a false perchè non è variabile
    return matbool


# matp e' la matrice start
# nodi e' la lista dei nodi
# mats e' la lista delle salette che mi serve per capire chi inizia e finisce le op
def create_initial_sol(matp, nodi, mats):
    # TODO: funzione inutile, non la chiamiamo mai
    # 1 per uscenti dal nodo, -1 per entranti
    fst_nd = []  # primi nodi
    max_tmp = 0
    ind = 0
    for i in range(0, len(mats)):
        fst_nd.append(mats[i][0])
    for i in range(0, len(fst_nd)):
        max_tmp = 0
        for j in range(0, len(matp)):
            if nodi[j].idP == fst_nd[i] and max_tmp < nodi[j].visita:
                max_tmp = nodi[j].visita
                ind = nodi[j].idN
        matp[0][ind] = 1
        matp[ind][0] = -1

    # stessa cosa per nodo finale
    lst_nd = []  # ultimi nodi
    min_tmp = 9  # inizializzo al max delle visite+1
    for i in range(0, len(mats)):
        lst_nd.append(mats[i][len(mats[i]) - 1])
    for i in range(0, len(lst_nd)):
        min_tmp = 9
        for j in range(0, len(matp)):
            if nodi[j].idP == lst_nd[i] and min_tmp > nodi[j].visita:
                print("//////////////////")
                min_tmp = nodi[j].visita
                ind = nodi[j].idN
        matp[len(matp[j]) - 1][ind] = -1
        matp[ind][len(matp[j]) - 1] = 1

    """ciclo i e j mi serve per prendere i pazienti da ogni saletta 
        in seguito ciclo con z su la lunghezza di nodi (indice di riga matrice)
        (in nodi ho la lista dei nodi con id nodo, id paziente e quale visita)
        se trovo che l idP(id paziente di Nodo) è lo stesso del paziente estratto dalla lista delle salette
        ciclo sulle colonne della nostra matrice mstart che viene passata come matp sempre di dimensione nodo
        quando trovo che l id del paziente e' presente in altri nodi all interno della lista [[per es P1= {n1=(1,2),n2={1,4)}]]
        vado a mettere 1 nella cella a cui deve seguire quel nodo (vedi 1 per uscenti)
    """
    for i in range(0, len(mats)):
        for j in range(0, len(mats[i])):
            for z in range(1, len(nodi) - 1):
                if nodi[z].idP == mats[i][j]:

                    for k in range(1, len(matp[z]) - 1):
                        # print("primo if, nodiz vale: " + str(nodi[z].idN) + " i vale " + str(i) + " j vale " + str(
                        # j) + " k vale : " + str(k))
                        if nodi[z].idP == nodi[k].idP:
                            matp[z][k] = 1
                            matp[k][z] = 1
                            if z == k:
                                matp[z][k] = 0

    # facciamo prima i piu' pesanti poi gli altri
    for i in range(1, len(matp) - 1):
        for j in range(1, len(matp[i]) - 1):
            if matp[i][j] != 0 and matp[i][j] == matp[j][i]:
                if nodi[i].visita >= nodi[j].visita:
                    matp[i][j] = 1
                    matp[j][i] = -1
                if nodi[i].visita < nodi[j].visita:
                    matp[i][j] = -1
                    matp[j][i] = 1

    return matp


def initial_sol(matp, nodi, mats, listp):
    # assegno pazienti da salette e scelgo il nodo iniziale
    fst_nd = []  # primi nodi
    max_tmp = 0
    for i in range(0, len(mats)):
        fst_nd.append(mats[i][0])
    for i in range(0, len(fst_nd)):
        max_tmp = 0
        for j in range(0, len(matp)):
            if nodi[j].idP == fst_nd[i] and max_tmp < nodi[j].visita:
                max_tmp = nodi[j].visita
                ind = nodi[j].idN
        matp[0][ind] = 1
        matp[ind][0] = -1

    lst_nd = []  # ultimi nodi
    min_tmp = 9  # inizializzo al max delle visite+1
    for i in range(0, len(mats)):
        lst_nd.append(mats[i][len(mats[i]) - 1])
    for i in range(0, len(lst_nd)):
        min_tmp = 9
        for j in range(0, len(matp)):
            if nodi[j].idP == lst_nd[i] and min_tmp > nodi[j].visita:
                # print("//////////////////")
                min_tmp = nodi[j].visita
                ind = nodi[j].idN
        matp[len(matp[j]) - 1][ind] = -1
        matp[ind][len(matp[j]) - 1] = 1

    # ordino i nodi escludendo il nodo 0 e len-2 che quindi e' l ultimo
    tmpnd = []
    res = []
    for i in range(0, len(listp)):
        for j in range(0, len(nodi)):
            if i + 1 == nodi[j].idP:
                tmpnd.append(nodi[j])
        # TODO: funziona solo per il primo paziente, gli altri li mette a caso
        res = sort_nodi_for_visit(tmpnd)
        lres = len(res) - 1
        # print(res)
        for k in range(0, len(res)):
            if k < lres:
                matp[res[k]][res[k + 1]] = 1
                matp[res[k + 1]][res[k]] = -1
        tmpnd.clear()
    return matp


def sort_nodi_for_visit(list_nodi):
    lord = []  # lista ordinata
    vtmp = 0
    tmp = []
    ind = 0
    for i in range(0, len(list_nodi)):
        tmp.append(list_nodi[i].visita)
    tmp = bubble_sort(tmp)
    for i in range(0, len(list_nodi)):
        for j in range(0, len(list_nodi)):
            if tmp[i] == list_nodi[j].visita:
                ind = list_nodi[j].idN
        lord.append(ind)
    return lord


def bubble_sort(l):
    ll = len(l)
    for i in range(0, ll):
        for j in range(ll - 1):
            if l[j] < l[j + 1]:
                t = l[j + 1]
                l[j + 1] = l[j]
                l[j] = t
    return l


def process(lists, listp, durataTest, stampa):
    mp, ms = set_the_mat(lists, listp)

    nodi, numn = crea_nodo(mp, ms)
    mstart = create_mat(nodi)

    # crea la soluzione e poi crea matrice bool
    matp = initial_sol(mstart, nodi, ms, listp)

    # crea matrice booleana che ha per come valori True solo archi DISGIUNTIVI
    mstartbool = create_mat_bool(nodi)
    if stampa:
        print("\nStampa Matrice Booleana: ")
        # stampa3(mstartbool)
        stampa_bool(mstartbool)

    # inserisco archi tra nodi che hanno la stessa visita
    soluzione = soluzione_iniziale(mstart, mstartbool, nodi, durataTest, stampa)
    if stampa:
        print("\nStampa di una possibile soluzione: ")
        stampa3(soluzione)

    # calcolo makespan usando la black box
    makespan, lista_tot = critical_path(soluzione, nodi, durataTest, stampa)

    # if stampa:
    # crea il grafo con plotly con la prima soluzione
    # grafico_gantt(lista_tot)

    print("\nMakespan sol grezza è: " + str(makespan))
    if stampa:
        print("\n TABU SEARCH \n")
    sol = tabu_search(soluzione, makespan, mstartbool, nodi, durataTest, stampa)
    # if stampa:
    # crea il grafo con plotly con la soluzione trovata dalla tabu
    # grafico_gantt(sol.lista_tot)

    # stampa un grafo con tutti i makespan trovati
    grafo_makespan(sol.lista_makespan, sol.makespan, makespan)
    return sol


def greedy(lists, listp, durataTest, stampa):
    mp, ms = set_the_mat(lists, listp)

    nodi, numn = crea_nodo(mp, ms)
    mstart = create_mat(nodi)

    # crea la soluzione e poi crea matrice bool
    matp = initial_sol(mstart, nodi, ms, listp)

    # crea matrice booleana che ha per come valori True solo archi DISGIUNTIVI
    mstartbool = create_mat_bool(nodi)
    if stampa:
        print("\nStampa Matrice Booleana: ")
        # stampa3(mstartbool)
        stampa_bool(mstartbool)

    # inserisco archi tra nodi che hanno la stessa visita
    soluzione = soluzione_iniziale(mstart, mstartbool, nodi, durataTest, stampa)
    if stampa:
        print("\nStampa di una possibile soluzione: ")
        stampa3(soluzione)

    # calcolo makespan usando la black box
    makespan, lista_tot = critical_path(soluzione, nodi, durataTest, stampa)

    return makespan, lista_tot


def path_relinking(listp, list_best, list_cand, k):
    lists = []
    if list_cand[k] == list_best[k]: # se sono ugali non cambio nulla, restituisco la sol così
        list_cand = list_cand
    else : # se sono diversi
        index = choose_el(list_cand,list_best[k]) # cerco l'indice nella sol candidate del valore nella soluzione best
        list_cand[k], list_cand[index] = list_cand[index], list_cand[k]

    listp_new = [] #nuova lista pazienti
    for a in list_cand:
        for b in listp:
            if b.id == a:
                listp_new.append(b)

    sala1, sala2, sala3 = inserimento_ordine_arrivo(listp_new)

    lists.append(sala1)
    lists.append(sala2)
    lists.append(sala3)

    return lists, listp_new
