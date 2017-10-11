from helpers.soluzione import *
import time

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
    # stampa nodi per creare grafo a mano easy
    # for nd in nodi:
    #    print("Nodo " + str(nd.idN) + ": (" + str(nd.idP) + "," + str(nd.visita+1) + ")")

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
    mette a False i nodi che:
        - hanno stessa riga e colonna
        - hanno pazienti diversi e lavori diversi
    '''
    for i in range(0, len(nodi)):
        for j in range(0, len(nodi)):
            if nodi[i].visita != -1:  # nodi con valore visita -1 ossia nodi di start ed end
                matbool[i][j] = False
            if nodi[i].idP != nodi[j].idP and nodi[i].visita == nodi[
                j].visita:  # nodi che condividono lo stesso test possono hanno archi disgiuntivi
                matbool[i][j] = True
            else:
                matbool[i][j] = False  # tutto il resto a false perchè non è variabile
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
    # stampa3(matp)
    # crea matrice booleana che ha per come valori True solo archi DISGIUNTIVI
    # mstartbool = create_mat_bool(nodi)
    # print("\nStampa Matrice Booleana: ")
    # stampa3(mstartbool)
    # stampa_bool(mstartbool)

    # crea una prima soluzione possibile
    # soluzione = soluzione_iniziale(mstart, mstartbool, nodi, durataTest)
    # print("\nStampa di una possibile soluzione: ")
    # stampa3(soluzione)
    '''
    calcolo il makespan della soluzione_iniziale utilizzando un algoritmo di label correcting 
    adattato alla ricerca del critical path di un grafo:
    la condizione di bellman utilizzata per l'aggiornamento della label del costo 
    è C(nodo_precedente)+D(nodo_precedente)>C(nodo_attuale)
    con C(i) costo del percorso fino al nodo i e D(i) durata dell'operazione del nodo i
    il makespan è ottenuto andando a isolare C(nodo_finale) al termine dell'algoritmo
    a differenza dell'algoritmo di label correcting per shortest path, non tengo in memoria i predecessori
    dei nodi perchè non sono interessato a qual'è il critical path ma solo al suo valore
    '''

    # makespan = critical_path(soluzione, nodi)
    # print("\nMakespan è: " + str(makespan))

    # print("\n TABU SEARCH\n")
    # sol = tabu_search(soluzione,makespan,mstartbool,nodi,durataTest)

    # print("\nGrafo finale: ")
    # stampa3(sol.grafo)
    # print("\nMAKESPAN FINALE: "+ str(sol.makespan))


    # bazza del check dei task relativi ai pazienti
    # i test non si sovrappongono
    lista_task = insert_task(listp)

    ts1,ts2,ts3= check_gantt(lista_task)

def check_gantt(lista_task):
    time = 0

    # metto i task in un array che definisce la sala in cui sono cosi facilito i vincoli tra pazienti nelle salette
    sala1 = []
    sala2 = []
    sala3 = []

    for i in range(0, len(lista_task)):
        if lista_task[i].sala == 1:
            sala1.append(lista_task[i])
        if lista_task[i].sala == 2:
            sala2.append(lista_task[i])
        if lista_task[i].sala == 3:
            sala3.append(lista_task[i])

    sala1,sala2,sala3=black_box(sala1 , sala2 , sala3)

    # vincoli start-end tra pazienti della stessa sala
    #vincoli_tra_paz_stessa_sala(sala1,0)
    #vincoli_tra_paz_stessa_sala(sala2,0)
    #vincoli_tra_paz_stessa_sala(sala3,0)

    # vincoli tra pazienti delle 3 salette (test non si sovrappongono)

    #vincolo_tra_test_uguali(sala1,sala2,sala3)



    for i in sala1:
        print("Paziente:" + str(i.paziente) + " Sala:" + str(i.sala) + " Test:" + str(i.test) + " Start:" + str(
            i.start) + " End: " + str(i.end))
    for i in sala2:
        print("Paziente:" + str(i.paziente) + " Sala:" + str(i.sala) + " Test:" + str(i.test) + " Start:" + str(
            i.start) + " End: " + str(i.end))
    for i in sala3:
        print("Paziente:" + str(i.paziente) + " Sala:" + str(i.sala) + " Test:" + str(i.test) + " Start:" + str(
            i.start) + " End: " + str(i.end))
    return sala1,sala2,sala3


def vincolo_tra_test_uguali(lista1,lista2,lista3):

    for t in range(1,5):# ciclo per ogni test
        for i in range(0, len(lista1)):
            for j in range(0, len(lista2)):
                for k in range(0,len(lista3)):
                    if lista1[i].test == t:
                        if lista2[j].test == t: #se hanno lo stesso test
                            if not lista2[j].start >= lista1[i].end:
                                shift_list(lista2,lista1[i].durata,j) #shift della durata del task nella lista1 tutta la lista2
                                vincoli_tra_paz_stessa_sala(lista1,i)
                                vincoli_tra_paz_stessa_sala(lista2,j)
                            #elif not lista1[i].start >= lista2[i].end:
                            #    shift_list(lista1,lista2[j].durata,i)
                        if lista3[k].test == t:
                            if not lista3[k].start >= lista1[i].end:
                                shift_list(lista3,lista1[i].durata,k)
                                vincoli_tra_paz_stessa_sala(lista1,i)
                                vincoli_tra_paz_stessa_sala(lista3,k)
                            #elif not lista1[i].start >= lista3[k].end:
                            #    shift_list(lista1, lista3[k].durata,i)
                    if lista2[j].test == t:
                        if lista1[i].test == t:
                            if not lista2[j].start >= lista1[i].end:
                                shift_list(lista2,lista1[i].durata,j) #shift della durata del task nella lista1 tutta la lista2
                                vincoli_tra_paz_stessa_sala(lista1,i)
                                vincoli_tra_paz_stessa_sala(lista2,j)
                            #elif not lista1[i].start >= lista2[i].end:
                            #    shift_list(lista1,lista2[j].durata,i)
                        if lista3[k].test == t:
                            if not lista3[k].start >= lista2[j].end:
                                shift_list(lista3,lista2[j].durata,k)
                                vincoli_tra_paz_stessa_sala(lista2,j)
                                vincoli_tra_paz_stessa_sala(lista3,k)
                            #elif not lista2[j].start >= lista3[k].end:
                            #    shift_list(lista1, lista3[k].durata,j)




def vincoli_tra_paz_diversa_sala(lista1,lista2,lista3):

    for i in range(0,len(lista1)):
        for j in range(0,len(lista2)):
                 if lista1[i].test == lista2[j].test:
                     shift_list(lista2,lista1[i].durata)
                 #if lista1[i].test == lista3[j].test:


def shift_list(list,shift,index):
    #shift dall'indice i-esimo in poi, nno tutti i task della lista
    for i in range(index,len(list)):
        list[i].start = list[i].start + shift
        list[i].end = list[i].end + shift

def vincoli_tra_paz_stessa_sala(sala,index):

    for i in range(index, len(sala)):#parto da i-esimo elemento perchè non devo sempre settare tutta la lista
        if i < (len(sala) - 1):  # se non sono arrivato all'ultimo task
                if not sala[i + 1].start >= sala[i].end:
                    while sala[i + 1].start >= sala[i].end:
                        sala[i+1].start = sala[i+1].start + 1
                elif sala[i + 1].start >= sala[i].end:
                    sala[i + 1].start = sala[i].end



def insert_task(listp):
    list_task = []
    # creo il task relativo a ogni paziente
    for i in range(0, len(listp)):
        task = crea_task(listp[i])
        list_task = task + list_task
    return list_task

# per ogni paziente, per ogni suo test, crea un task
def crea_task(paziente):
    tasks_paziente = []
    for i in paziente.test_array:
        task = Task(paziente.id, paziente.saletta, i, 0)
        tasks_paziente.append(task)
        # print("\n Paziente: " + str(task.paziente) + " Sala: " + str(task.sala) + " Test: " + str(task.test))
    return tasks_paziente


def black_box(ts1,ts2,ts3):
    ttot=0 #tempo totale esecuzione
    # #tempi totali per ogni saletta
    tt1=0
    tt2=0
    tt3=0
    check_box= False
    ## tempi per rilascio evitare la sovrapposizione di job
    tmp1=110
    tmp2=110
    tmp3=110
    #variabile per evitare il sovrapporsi di op
    test_before = []
    # lock per test -->mutua esclusione
    t1=False
    t2=False
    t3=False
    t4=False
    t5=False
    lock = [] #a che saletta do il lock  -->a chi do la mutua esclusione
    #contatori 3 salette
    c1=0
    c2=0
    c3=0
    # contatori 3 salette temporanei
    c1t= 0
    c2t= 0
    c3t= 0
    #setto una variabile per ogni saletta se sta facendo un test in maniera
    #da poter incrementare il tempo di uno puramente nel caso sia in idle
    idles1=False
    idles2=False
    idles3=False
    #Inizializzo i lock
    for i in range (0,5):
        lock.append('')
    #Inizializzo variabili test prec
    for i in range(0,3):
        test_before.append(0)

    #idles1,idles2,idles3=False
    while check_box is False:
        #check_box variabile che mi serve per ciclare(finche' tutti e 3 gli indici son stati esauriti rimane a false)
        #controllo per lunghezza task ts1

        #                          ----------- SALA 1 --------
        if c1<len(ts1):

            # ------------          test 1 per task sala 1      -------
            if ts1[c1t].test==1:
                if t1==True and lock[0]!="s1" and idles1==False :
                    tt1+=1

                if t1 == True and lock[0]=="s1":
                    if tt1 >= ts1[c1t].end:
                        lock[0]=''
                        t1=False
                        tmp1=tt1
                        test_before[0]=1
                        c1+=1
                        idles1=False
                    else:
                        tt1+=1
                elif t1== False and (test_before[1]!=1  and test_before[2]!=1 ) :
                    if ts1[c1t].test == 1:  #and (test_before[1]!=1 or test_before[2]!=1 ): #reinserisco il controllo perchè mi rifarebbe la stessa visita
                        ts1[c1t].start=tt1
                        ts1[c1t].end = tt1+1
                        tt1+=1
                        t1=True
                        lock[0]="s1"
                        idles1=True

                        #else:
                        #tt1+=1
            # ------------          test 2 per task sala 1      -------
            if ts1[c1t].test==2:
                if t2==True and lock[1]!="s1" and idles1==False  :
                    tt1+=1

                if t2 == True and lock[1]=="s1":
                    if tt1 >= ts1[c1t].end:
                        lock[1]=''
                        t2=False
                        c1+=1
                        tmp1 = tt1
                        test_before[0] = 2
                        idles1=False
                    else:
                        tt1+=1
                elif t2== False and (test_before[1]!=2  and  test_before[2]!=2 ):
                    if ts1[c1t].test == 2: #and (test_before[1]!=2 or test_before[2]!=2 ):
                        ts1[c1t].start=tt1
                        ts1[c1t].end = tt1 + 2
                        tt1 +=1
                        t2=True
                        lock[1]="s1"
                        idles1=True

                        #else:
                        #tt1+=1
            # ------------          test 3 per task sala 1      -------
            if ts1[c1t].test==3:
                if t3==True and lock[2]!="s1" and idles1==False :
                    tt1 +=1

                if t3 == True and lock[2]=="s1":
                    if tt1 >= ts1[c1t].end:
                        lock[2]=''
                        t3=False
                        tmp1 = tt1
                        test_before[0] = 3
                        c1+=1
                        idles1=False
                    else:
                        tt1+=1
                elif t3== False and (test_before[1]!=3  and  test_before[2]!=3 ):
                    if ts1[c1t].test == 3:
                        ts1[c1t].start=tt1
                        ts1[c1t].end = tt1 + 4
                        tt1 +=1
                        t3=True
                        lock[2]="s1"
                        idles1=True

                        #else:
                        #tt1+=1
            # ------------          test 4 per task sala 1      -------
            if ts1[c1t].test==4:
                if t4==True and lock[3]!="s1" and idles1==False :
                    tt1 +=1

                #se i tempi vengono sballati di uno bisogna invertire queste due condizioni
                if t4 == True and lock[3]=="s1":
                    if tt1 >= ts1[c1t].end:
                        lock[3]=''
                        t4=False
                        c1+=1
                        test_before[0] = 4
                        tmp1 = tt1
                        idles1=False
                    else:
                        tt1+=1
                elif t4== False and (test_before[1]!=4  and  test_before[2]!=4 ):
                    if ts1[c1t].test == 4 :
                        ts1[c1t].start=tt1
                        ts1[c1t].end = tt1 + 6
                        tt1 +=1
                        t4=True
                        lock[3]="s1"
                        idles1=True

                        #else:
                        #tt1+1
            # ------------          test 5 per task sala 1      -------
            if ts1[c1t].test==5:
                if t5 ==True and lock[4]!="s1" and idles1==False :#and (test_before[1]==5 or test_before[2]==5 ):
                    tt1 +=1

                #se i tempi vengono sballati di uno bisogna invertire queste due condizioni
                if t5 == True and lock[4]=="s1":
                    if tt1 >= ts1[c1t].end:
                        lock[4]=''
                        t5=False
                        c1+=1
                        test_before[0] = 5
                        tmp1 = tt1
                        idles1=False
                    else:
                        tt1+=1
                elif t5== False and (test_before[1]!=5  and  test_before[2]!=5 ):
                    if ts1[c1t].test == 5:
                        ts1[c1t].start=tt1
                        ts1[c1t].end = tt1 + 8
                        tt1 +=1
                        t5=True
                        lock[4]="s1"
                        idles1=True

                        #else:
                        #tt1+=1
        #                           ----------- SALA 2 --------
        if c2<len(ts2):

            #tt2+=1
            # ------------          test 1 per task sala 2      -------
            if ts2[c2t].test==1:
                if t1==True and lock[0]!="s2" and idles2==False:# and (test_before[0]==1 or test_before[2]==1 ):
                    tt2+=1

                if t1 == True and lock[0]=="s2":
                    if tt2 >= ts2[c2t].end:
                        lock[0]=''
                        t1=False
                        c2+=1
                        test_before[1] = 1
                        tmp2 = tt2
                        idles2=False
                    else:
                        tt2+=1
                elif t1== False and (test_before[0]!=1 and test_before[2]!=1 ):
                    if ts2[c2t].test == 1 :
                        #reinserisco il controllo perchè mi rifarebbe la stessa visita
                        ts2[c2t].start=tt2
                        ts2[c2t].end = tt2 + 1
                        tt2 +=1
                        t1=True
                        lock[0]="s2"
                        idles2=True
                elif t1 == False and (test_before[0] == 1 or test_before[2] == 1):
                    if (test_before[0]==1):
                        tt2=ts1[c1t].end

                        #else:
                        #tt2+=1
            # ------------          test 2 per task sala 2      -------
            if ts2[c2t].test==2:
                if t2==True and lock[1]!="s2" and idles2==False:# and (test_before[0]==2 or test_before[2]==2 ):
                    tt2 +=1

                if t2 == True and lock[1]=="s2":
                    if tt2 >= ts2[c2t].end:
                        lock[1]=''
                        t2=False
                        c2+=1
                        test_before[1] = 2
                        tmp2 = tt2
                        idles2=False
                    else:
                        tt2+=1
                elif t2== False and (test_before[0]!=2 and test_before[2]!=2 ):
                    if ts2[c2t].test == 2:
                        ts2[c2t].start=tt2
                        ts2[c2t].end = tt2 + 2
                        tt2 +=1
                        t2=True
                        lock[1]="s2"
                        idles2=True
                elif t2 == False and (test_before[0] == 2 or test_before[2] == 2):
                    if (test_before[0]==2):
                        tt2=ts1[c1t].end
                        #else:
                        #tt2+=1
            # ------------          test 3 per task sala 2      -------
            if ts2[c2t].test==3:
                if t3==True and lock[2]!="s2" and idles2==False:# and (test_before[0]==3 or test_before[2]==3 ):
                    tt2 +=1

                if t3 == True and lock[2]=="s2":
                    if tt2 >= ts2[c2t].end:
                        lock[2]=''
                        t3=False
                        c2+=1
                        tmp2 = tt2
                        test_before[1] = 3
                        idles2=False
                    else:
                        tt2+=1
                elif t3== False and (test_before[0]!=3  and  test_before[2]!=3 ):
                    if ts2[c2t].test == 3:
                        ts2[c2t].start=tt2
                        ts2[c2t].end = tt2 + 4
                        tt2 +=1
                        t3=True
                        lock[2]="s2"
                        idles2=True
                elif t3 == False and (test_before[0] == 3 or test_before[2] == 3):
                    if (test_before[0]==3):
                        tt2=ts1[c1t].end
                        #else:
                        #tt2+=1
            # ------------          test 4 per task sala 2      -------
            if ts2[c2t].test==4:
                if t4==True and lock[3]!="s2" and idles2==False:# and (test_before[0]==4 or test_before[2]==4 ):
                    tt2 +=1

                #se i tempi vengono sballati di uno bisogna invertire queste due condizioni
                if t4 == True and lock[3]=="s2":
                    if tt2 >= ts2[c2t].end:
                        lock[3]=''
                        t4=False
                        c2+=1
                        test_before[1] = 4
                        tmp2 = tt2
                        idles2=False
                    else:
                        tt2+=1
                elif t4== False and (test_before[0]!=4  and  test_before[2]!=4 ):
                    if ts2[c2t].test == 4 :
                        ts2[c2t].start=tt2
                        ts2[c2t].end = tt2 + 6
                        tt2 +=1
                        t4=True
                        lock[3]="s2"
                        idles2=True
                elif t4 == False and (test_before[0] == 4 or test_before[2] == 4):
                    if (test_before[0]==4):
                        tt2=ts1[c1t].end
                        #else:
                        #tt2+=1
            # ------------          test 5 per task sala 2      -------
            if ts2[c2t].test==5:
                if t5 ==True and lock[4]!="s2" and idles2==False :#and (test_before[0]==5 or test_before[2]==5 ):
                    tt2 +=1

                #se i tempi vengono sballati di uno bisogna invertire queste due condizioni
                if t5 == True and lock[4]=="s2":
                    if tt2 >= ts2[c2t].end:
                        lock[4]=''
                        t5=False
                        c2+=1
                        test_before[1] = 5
                        tmp2 = tt2
                        idles2=False
                    else:
                        tt2+=1
                elif t5== False and (test_before[0]!=5  and  test_before[2]!=5 ):
                    if ts2[c2t].test == 5:
                        ts2[c2t].start=tt2
                        ts2[c2t].end = tt2 + 8
                        tt2 +=1
                        t5=True
                        lock[4]="s2"
                        idles2=True
                elif t5 == False and (test_before[0] == 5 or test_before[2] == 5):
                    if (test_before[0]==5):
                        tt2=ts1[c1t].end
                        #else:
                        #tt2+=1
        #                               ----------- SALA 3--------
        if c3<len(ts3):

            # ------------          test 1 per task sala 3      -------
            #tt3+=1
            if ts3[c3t].test==1:
                if t1==True and lock[0]!="s3" and idles3==False:# and (test_before[0]==1 or test_before[1]==1 ):
                    tt3+=1

                if t1 == True and lock[0]=="s3":
                    if tt3 >= ts3[c3t].end:
                        lock[0]=''
                        t1=False
                        c3+=1
                        test_before[2] = 1
                        tmp3 = tt3
                        idles3=False
                    else:
                        tt3+=1
                elif t1== False and (test_before[0]!=1  and  test_before[1]!=1 ):
                    if ts3[c3t].test == 1:
                        #reinserisco il controllo perchè mi rifarebbe la stessa visita
                        ts3[c3t].start=tt3
                        ts3[c3t].end = tt3 + 1
                        tt3 +=1
                        t1=True
                        lock[0]="s3"
                        idles3=True
                elif t1 == False and (test_before[0] == 1 or test_before[1] == 1):
                    if test_before[0]==1 :
                        tt3=ts1[c1t].end
                    elif test_before[1]==1:
                        tt3=ts2[c2t].end
                        #else:
                        #tt3+=1
            # ------------          test 2 per task sala 3      -------
            if ts3[c3t].test==2:
                if t2==True and lock[1]!="s3" and idles3==False :#and (test_before[0]==2 or test_before[1]==2 ):
                    tt3 +=1

                if t2 == True and lock[1]=="s3":
                    if tt3 >= ts3[c3t].end:
                        lock[1]=''
                        t2=False
                        c3+=1
                        test_before[2] = 2
                        tmp3 = tt3
                        idles3=False
                    else:
                        tt3+=1
                elif t2== False and test_before[0]!=2  and  test_before[1]!=2 :
                    if ts3[c3t].test == 2:
                        ts3[c3t].start=tt3
                        ts3[c3t].end = tt3 + 2
                        tt3 +=1
                        t2=True
                        lock[1]="s3"
                        idles3=True
                elif t2 == False and (test_before[0] == 2 or test_before[1] == 2):
                    if test_before[0] == 2:
                        tt3 = ts1[c1t].end
                    elif test_before[1] == 2:
                        tt3 = ts2[c2t].end
                        #else:
                        #tt3+=1
            # ------------          test 3 per task sala 3      -------
            if ts3[c3t].test==3:
                if t3==True and lock[2]!="s3" and idles3==False: # and (test_before[0]==3 or test_before[1]==3 ):
                    tt3 +=1

                if t3 == True and lock[2]=="s3":
                    if tt3 >= ts3[c3t].end:
                        lock[2]=''
                        t3=False
                        c3+=1
                        test_before[2] = 3
                        tmp3 = tt3
                        idles3=False
                    else:
                        tt3+=1
                elif t3== False and test_before[0]!=3  and  test_before[1]!=3 :
                    if ts3[c3t].test == 3:
                        ts3[c3t].start=tt3
                        ts3[c3t].end = tt3 + 4
                        tt3 +=1
                        t3=True
                        lock[2]="s3"
                        idles3=True
                elif t3== False and (test_before[0] == 3 or test_before[1] == 3):
                    if test_before[0] == 3:
                        tt3 = ts1[c1t].end
                    elif test_before[1] == 3:
                        tt3 = ts2[c2t].end
                        #else:
                        #tt3+=1

            # ------------          test 4 per task sala 3      -------
            if ts3[c3t].test==4:
                if t4==True and lock[3]!="s3" and idles3==False:#and (test_before[0]==4 or test_before[1]==4 ):
                    tt3 +=1

                #se i tempi vengono sballati di uno bisogna invertire queste due condizioni
                if t4 == True and lock[3]=="s3":
                    if tt3 >= ts3[c3t].end:
                        lock[3]=''
                        t4=False
                        c3+=1
                        test_before[2] = 4
                        tmp3 = tt3
                        idles3=False
                    else:
                        tt3+=1
                elif t4== False and (test_before[0]!=4  and  test_before[1]!=4 ):
                    if ts3[c3t].test == 4 :
                        ts3[c3t].start=tt3
                        ts3[c3t].end = tt3 + 6
                        tt3 +=1
                        t4=True
                        lock[3]="s3"
                        idles3=True
                elif t4 == False and (test_before[0] == 4 or test_before[1] == 4):
                    if test_before[0] == 4:
                        tt3 = ts1[c1t].end
                    elif test_before[1] == 4:
                        tt3 = ts2[c2t].end
                        #else:
                        #tt3+=1
            # ------------          test 5 per task sala 3      -------
            if ts3[c3t].test==5:
                if t5 ==True and lock[4]!="s3" and idles3==False :#and (test_before[0]==5 or test_before[1]==5 ):
                    tt3 +=1

                #se i tempi vengono sballati di uno bisogna invertire queste due condizioni
                if t5 == True and lock[4]=="s3":
                    if tt3 >= ts3[c3t].end:
                        lock[4]=''
                        t5=False
                        c3+=1
                        test_before[2] = 5
                        tmp3 = tt3
                        idles3=False
                    else:
                        tt3+=1
                elif t5== False and test_before[0]!=5 and test_before[1]!=5 :
                    if ts3[c3t].test == 5:
                        ts3[c3t].start=tt3
                        ts3[c3t].end = tt3 + 8
                        tt3 +=1
                        t5=True
                        lock[4]="s3"
                        idles3=True
                elif t5 == False and (test_before[0] == 5 or test_before[1] == 5):
                    if test_before[0] == 5:
                        tt3 = ts1[c1t].end
                    elif test_before[1] == 5:
                        tt3 = ts2[c2t].end
                    #else:
                        #tt3+=1
        if tmp1== tt1:
            test_before[0] = 0
        if tmp2 == tt2:
            test_before[1] = 0
        if tmp3== tt3:
            test_before[2] = 0
        ttot+=1
        #time.sleep(1)
        c1t=c1
        c2t=c2
        c3t=c3
        a=len(ts1)
        b=len(ts2)
        c=len(ts3)
        if c1==a and c2==b and c3==c:
            check_box=True;

    print ("\ntt1\n"+str(tt1))
    print("\n tt2 \n"+str(tt2))
    print("\ntt3\n"+str(tt3))
    return ts1,ts2,ts3


















