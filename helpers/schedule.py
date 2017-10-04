from helpers.utils import *
from helpers.struct import *
from helpers.soluzione import *


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
        test = set_test(listp[i].test_array)
        sala = listp[i].saletta
        newlistp.append(test)

    for j in range(0, len(newlistp)):
        matrixp.append(list_to_mat(newlistp[j]))

    return (matrixp, matrixs)


def crea_nodo(mp):
    # creo nodo da lista pazienti (paz,visita)
    nodi = []
    numn = 0
    ns = Nodo(0, 0, 0)
    nodi.append(ns)
    for i in range(0, len(mp)):
        for j in range(0, len(mp[i])):
            numn += 1
            nd = Nodo(numn, i + 1, mp[i][j])
            nodi.append(nd)
    nd = Nodo(numn + 1, 0, 0)
    nodi.append(nd)
    #stampa nodi per creare grafo a mano easy
    for nd in nodi:
        print("Nodo " + str(nd.idN) + ": (" + str(nd.idP) + "," + str(nd.visita+1) + ")")

    return nodi, numn


def stampa3(matr):
    for i in range(0, len(matr)):
        print(i, end="   ", flush=True)
    print("\r")
    for i in range(0, len(matr)):
        print(str(i) + "  " + str(matr[i]))

def stampa_bool(matrix):
    matr = copia_grafo_booleano(matrix,len(matrix))
    for i in range(0, len(matr)):
        print(" -  "+str(i), end="", flush=True)
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
    mette a False i nodi che:
        - hanno stessa riga e colonna
        - hanno pazienti diversi e lavori diversi
    '''
    for i in range(0, len(nodi)):
        for j in range(0, len(nodi)):
            if nodi[i].visita != -1: #nodi con valore visita -1 ossia nodi di start ed end
                matbool[i][j] = False
            if nodi[i].idP != nodi[j].idP and nodi[i].visita == nodi[j].visita:# nodi che condividono lo stesso test possono hanno archi disgiuntivi
                matbool[i][j] = True
            else:
                matbool[i][j] = False #tutto il resto a false perchè non è variabile

    # tutti nodi sono collegati a quello di partenza
    '''for i in range(1, len(nodi) - 1):
        matbool[0][i] = False

    # tutti nodi sono collegati a quello di fine
    for i in range(1, len(nodi) - 1):
        matbool[i][len(nodi) - 1] = False

    # impongo che nodo partenza e nodo arrivo non possono essere uguali
    matbool[0][len(nodi) - 1] = False
    matbool[len(nodi) - 1][0] = False'''

    return matbool


# matp e' la matrice start
# nodi e' la lista dei nodi
# mats e' la lista delle salette che mi serve per capire chi inizia e finisce le op
def create_initial_sol(matp, nodi, mats):
    # 1 per uscenti dal nodo, -1 per entranti
    st_op = []  # start operation
    last_op = []  # last operation
    # metto a 0 le celle con righe=colonne
    """for i in range(0,len(matp)):
        for j in range(0,len(matp[i])):
            if i == j:
                    matp[i][j]=0"""
    # cerco operazioni iniziali nodo 0
    """for i in range(0, len(mats)):
        st_op.append(mats[i][0])
        print("mats i0:"+str(mats[i][0]))
    print("\nPazienti che possono essere successivi al nodo iniziale: "+str(st_op))
    for i in range(0, len(st_op)):
        max_percorso=0
        for j in range(0, len(matp)):
            if nodi[j].idP == st_op[i]:
                if max_percorso< nodi[j].visita:
                    max_percorso= nodi[j].visita
                    matp[0][nodi[j].idP+1] = 1
                    matp[nodi[j].idP+1][0] = -1"""

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
    """for i in range(0, len(mats)):
        last_op.append(mats[i][len(mats[i]) - 1])
    print("\nPazienti che possono raggiungere il nodo finale: "+str(last_op))
    for i in range(0, len(last_op)):
        for j in range(0, len(matp)):
            if nodi[j].idP == last_op[i]:
                matp[len(matp[j]) - 1][j] = -1
                matp[j][len(matp[j]) - 1] = 0"""
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
    # stampa3(matp)
    # inserisco i nodi successivi
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
                print("//////////////////")
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

        res = sort_nodi_for_visit(tmpnd)
        lres = len(res) - 1
        print(res)
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


# 0 nessun legame
# 1va in
# -1 riceve

def process(lists, listp, durataTest):
    mp, ms = set_the_mat(lists, listp)

    # stampa_matrici(mp,"paziente","visita")
    # stampa_matrici(ms, "saletta", "paziente")

    nodi, numn = crea_nodo(mp)
    mstart = create_mat(nodi)

    # crea la soluzione e poi crea matrice bool
    # matp = create_initial_sol(mstart, nodi, ms)
    matp = initial_sol(mstart, nodi, ms, listp)
    stampa3(matp)
    #crea matrice booleana che ha per come valori True solo archi DISGIUNTIVI
    mstartbool = create_mat_bool(nodi)
    print("\nStampa Matrice Booleana: ")
    #stampa3(mstartbool)
    stampa_bool(mstartbool)

    # crea una prima soluzione possibile
    soluzione = soluzione_iniziale(mstart, mstartbool, nodi, durataTest)
    print("\nStampa di una possibile soluzione: ")
    stampa3(soluzione)

    makespan = critical_path(soluzione, nodi)
    print("\nMakespan è: " + str(makespan))

    print("\n TABU SEARCH")
    sol = tabu_search(soluzione,makespan,mstartbool,nodi,durataTest)

    print("\n")
    print("MAKESPAN FINALE: "+ str(sol.makespan))