from helpers.grafo_gantt import *
from helpers.struct_p import *


def lista_nodi_da_grafo(grafo, nodi):
    # parto da 1 per evitare i nodi start e end
    for i in range(1, len(nodi) - 1):
        for j in range(1, len(nodi) - 1):
            if grafo[i][j] == 1:  # se l'arco è uscente dal nodo i-esimo. Ossia i-->j
                nodi[i], nodi[j] = nodi[j], nodi[i]

    return nodi


def check_aciclico(grafo, durate, lista_nodi, max_makespan):
    costo = []
    nodi_visita = []
    nodi_visita.append(0)

    for i in range(0, len(lista_nodi)):
        costo.append(0)

    while not nodi_visita:
        nodo = nodi_visita[0]
        for i in range(0, len(lista_nodi)):
            if grafo[nodo][i] == 1:
                if i not in nodi_visita:
                    nodi_visita.append(i)
                    test = lista_nodi[nodo].visita
                    if costo[nodo] + durate[test] >= costo[i]:
                        costo[i] = durate[test] + costo[nodo]
                    if costo[i] >= max_makespan:
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


def soluzione_iniziale(grafo, grafo_fixed, lista_nodi, durate, stampa):
    len_nodi = len(lista_nodi)
    # creo nuovo grafo a partire dai valori del vecchio grafo
    grafo_new = copia_grafo(grafo, len_nodi)

    for i in range(0, len_nodi):
        trovato = False
        for j in range(0, len_nodi):
            if lista_nodi[i].visita != lista_nodi[j].visita and lista_nodi[i].idP == lista_nodi[j].idP and j > i and not trovato:
                if grafo_fixed[i][j]:
                    trovato = True
                    grafo_new[i][j] = 1
                    grafo_new[j][i] = -1
                    if stampa:
                        print("Inserito arco tra: " + str(lista_nodi[i].idN) + "-->" + str(lista_nodi[j].idN))
    max = 0
    for i in range(0, 5):
        if durate[i] > max:
            max = durate[i]
    max_makespan = max * len_nodi
    if stampa:
        print("\nMassimo makespan è:" + str(max_makespan))
    aciclico = check_aciclico(grafo_new, durate, lista_nodi, max_makespan)
    if aciclico:
        if stampa:
            print("\nNon è ciclico, si può procedere")
    else:
        if stampa:
            print("\nE' ciclico, vi è un LOOP !!!!!!!!!")
    return grafo_new


def critical_path(grafo, nodi, durate, stampa):

    # non ci interessa tanto il percorso migliore fra i nodi, ma il loro makespan. Questo perchè la scelta della
    # posizione di un task non influisce solo sul singolo cammino di un paziente ma anche su quello degli altri
    new_nodi = lista_nodi_da_grafo(grafo, nodi)

    lista_task = insert_task_da_nodo(new_nodi)

    ts1, ts2, ts3 = check_gantt(lista_task, stampa)

    # cerco il task con la fine più grande
    lista_tot = ts1 + ts2 + ts3
    makespan = 0
    for i in lista_tot:
        if i.end > makespan:
            makespan = i.end

    return makespan, lista_tot


def trova_archi(nodi, len_nodi, grafo_disgiuntivo):
    lista = []
    for i in range(1, len_nodi):
        for j in range(1, len_nodi):
            if grafo_disgiuntivo[i][j] and i < j:
                lista.append(Arco(nodi[i].visita, i, j))
    return lista


def trova_archi_esistenti(nodi, len_nodi, grafo_disgiuntivo, archi_da_decidere, grafo_partenza):
    lista = []

    for i in range(0, len(archi_da_decidere)):
        arco = Arco(archi_da_decidere[i].visita, archi_da_decidere[i].primo_estremo,
                    archi_da_decidere[i].secondo_estremo)
        if grafo_partenza[arco.primo_estremo][arco.secondo_estremo] != 0:
            lista.append(arco)

    return lista


def cerca_archi_non_esistenti(archi_da_decidere, grafo, num_of_nodi, fixed, nodi):
    temp = []
    size = len(archi_da_decidere)
    for i in range(0, size):
        arc_temp = archi_da_decidere[i]
    if grafo[arc_temp.primo_estremo][arc_temp.secondo_estremo] == 0:
        temp.append(arc_temp)

    return temp


def conta_entranti(grafo, num_of_nodi, indice_secondo):
    counter = 0
    for i in range(0, num_of_nodi):
        if grafo[indice_secondo][i] == -1:
            counter += counter
    return counter


def conta_uscenti(grafo, num_of_nodi, indice_secondo):
    counter = 0
    for i in range(0, num_of_nodi):
        if grafo[indice_secondo][i] == 1:
            counter += counter
    return counter


def swap(archi_esistenti, grafo, num_of_nodi, tabu_list, nodi, durate, ottimo_candidato_makespan, stampa):
    lista_makespan = []
    lista_task = []
    size = len(archi_esistenti)
    aciclico = False
    temp = Arco(0, 0, 0)
    tabu_temp = Mossa('a', 0, 0, 0, 0, 0)
    grafo_temporaneo = [[0 for x in range(num_of_nodi)] for y in range(num_of_nodi)]
    max = 0
    for i in range(0, 5):
        if durate[i] >= max:
            max = durate[i]
    max_makespan = num_of_nodi * max
    makespan = max_makespan
    makespan_temp = max_makespan
    no_mossa = True

    # per ogni macchina controllo gli archi già esistenti e ne giro il verso
    for i in range(0, 5):
        grafo2 = [[0 for x in range(num_of_nodi)] for y in range(num_of_nodi)]
        grafo2 = copia_grafo(grafo, num_of_nodi)
        for s in range(0, size):
            temp = archi_esistenti[s]
            if temp.visita == i:
                if grafo[temp.primo_estremo][temp.secondo_estremo] == 1:
                    grafo2[temp.primo_estremo][temp.secondo_estremo] = -1
                    grafo2[temp.secondo_estremo][temp.primo_estremo] = 1
                else:
                    grafo2[temp.primo_estremo][temp.secondo_estremo] = 1
                    grafo2[temp.secondo_estremo][temp.primo_estremo] = -1

        ok = True
        # verifico che questa mossa non abbia infranto la condizione che gli archi entranti e gli archi uscenti
        # di ogni nodo devono essere al max 2
        for k in range(1, len(nodi) - 1):
            if conta_uscenti(grafo2, num_of_nodi, k) > 2 or conta_entranti(grafo2, num_of_nodi, k) > 2:
                ok = False
        # se la condizione è rispettata preparo l'oggetto mossa corrispondente e controllo che il grafo sia aciclico
        if ok:
            mossa_temp = Mossa('s', i, 0, 0, 0, 0)

        # controllo se grafo è ok
        aciclico = check_aciclico(grafo2, durate, nodi, max_makespan)

        # se è aciclico calcolo il makespan
        if (aciclico):
            makespan_temp, lista_tot = critical_path(grafo2, nodi, durate, stampa)
            if stampa:
                print("S_Makespan : " + str(makespan_temp))
            lista_makespan.append(makespan_temp)
            lista_task.append(lista_tot)
            # controllo la tabu list
            # se è una mossa tabù controllo se il nuovo makespan è migliore dell'ottimo candidato(criterio di aspirazione)
            if mossa_temp in tabu_list:
                # criterio di aspirazione
                if makespan_temp < ottimo_candidato_makespan:
                    no_mossa = False
                makespan = makespan_temp
                tabu_temp = mossa_temp
                grafo_temporaneo = copia_grafo(grafo2, num_of_nodi)

            # se non è tabù la salvo solo se è migliore delle altre mosse swap calcolate a su questo grafo
            else:
                if makespan_temp < makespan:
                    no_mossa = False
                    makespan = makespan_temp
                    tabu_temp = mossa_temp
                    grafo_temporaneo = copia_grafo(grafo2, num_of_nodi)

    # se nessuna mossa è consentita restituisco il valore massimo del makespan
    if no_mossa:
        makespan = max_makespan

    best_index = lista_makespan.index(makespan)
    lista_task_finale = lista_task[best_index]
    s = Solution(grafo_temporaneo, makespan, tabu_temp, lista_makespan, lista_task_finale)

    return s


def remove(archi_da_decidere, grafo_iniz, num_of_nodi, tabu_list, nodi, durate, ottimo_candidato_makespan, fixed):
    archi_esistenti = []
    archi_da_imporre = []
    lista_makespan = []
    lista_tot = []

    archi_esistenti = trova_archi_esistenti(nodi, num_of_nodi, fixed, archi_da_decidere, grafo_iniz)
    archi_da_imporre = cerca_archi_non_esistenti(archi_da_decidere, grafo_iniz, num_of_nodi, fixed, nodi)

    size = len(archi_esistenti)
    size2 = len(archi_da_imporre)

    max = 0
    for i in range(0, 5):
        if durate[i] >= max:
            max = durate[i]
    max_makespan = num_of_nodi * max
    makespan_temporaneo = 0
    makespan_precedente = max_makespan

    mossa_precedente = Mossa('a', 0, 0, 0, 0, 0)

    grafo_precedente = [[0 for x in range(num_of_nodi)] for y in range(num_of_nodi)]

    nessuna_mossa = True

    # per ogni arco esistente controllo gli archi ancora non esistenti (relativi alla stessa macchina) e verifico se l'eventuale
    # aggiunta dell'arco non esitente non pregiudica la condizione sul massimo di archi entranti e uscenti
    # se la condizione è rispettata allora rimuovo l'arco esistente e aggiungo quello non esistente
    # altrimenti passo ad un altro arco non esistente
    temp1 = []
    temp2 = []
    for i in range(0, size):
        temp1 = archi_esistenti[i]
        for s in range(0, size2):
            mossa = True
            aciclico = False
            temp2 = archi_da_imporre[s]
            grafo_temporaneo = copia_grafo(grafo_iniz, num_of_nodi)
            if temp1.visita == temp2.visita:
                if conta_uscenti(grafo_temporaneo, num_of_nodi, temp2.primo_estemo) < 2 and conta_entranti(
                        grafo_temporaneo, num_of_nodi, temp2.secondo_estemo) < 2:
                    grafo_temporaneo[temp1.primo_estemo][temp1.secondo_estemo] = 0
                    grafo_temporaneo[temp1.secondo_estemo][temp1.primo_estemo] = 0
                    grafo_temporaneo[temp2.primo_estemo][temp2.secondo_estemo] = 1
                    grafo_temporaneo[temp2.secondo_estemo][temp2.primo_estemo] = -1
                elif conta_uscenti(grafo_temporaneo, num_of_nodi, temp2.secondo_estemo) < 2 and conta_entranti(
                        grafo_temporaneo, num_of_nodi, temp2.primo_estemo) < 2:
                    grafo_temporaneo[temp1.primo_estemo][temp1.secondo_estemo] = 0
                    grafo_temporaneo[temp1.secondo_estemo][temp1.primo_estemo] = 0
                    grafo_temporaneo[temp2.primo_estemo][temp2.secondo_estemo] = -1
                    grafo_temporaneo[temp2.secondo_estemo][temp2.primo_estemo] = 1
                else:
                    mossa = False

            # se la mossa è possibile controllo se il grafo è aciclico ed effettuo i controlli sulla tabu list
            # e sul makespan
            # se la mossa è consentita allora aggiorno il boolean nessuna mossa
            if mossa:
                mossa_temp = Mossa('r', temp1.visita, temp1.primo_estremo, temp1.secondo_estemo, temp2.primo_estremo,
                                   temp2.secondo_estemo)
                aciclico = check_aciclico(grafo_temporaneo, durate, nodi, max_makespan)
                if aciclico:
                    makespan_temporaneo, lista_tot = critical_path(grafo_temporaneo, nodi, durate)
                    print("Makespan remove: " + str(makespan_temporaneo))
                    lista_makespan.append(makespan_temporaneo)
                    if makespan_temporaneo < makespan_precedente:
                        if not tabu_list.contains(mossa_temp):
                            nessuna_mossa = False
                            makespan_precedente = makespan_temporaneo
                            mossa_precedente = mossa_temp
                            grafo_precedente = copia_grafo(grafo_temporaneo, num_of_nodi)
                        else:
                            # criterio di aspirazione
                            if makespan_temporaneo < ottimo_candidato_makespan:
                                nessuna_mossa = False
                                makespan_precedente = makespan_temporaneo
                                mossa_precedente = mossa_temp
                                grafo_precedente = copia_grafo(grafo_temporaneo, num_of_nodi)

    # se nessuna mossa è consentita restituisco il massimo makespan
    if nessuna_mossa:
        makespan_precedente = max_makespan

    sol = Solution(grafo_precedente, makespan_precedente, mossa_precedente, lista_makespan, lista_tot)

    return sol


def tabu_search(grafo_candidato, makespan_candidato, grafo_disgiuntivo, nodi, durate, stampa):
    lista_makespan = []  # salvo tutti i makespan trovati
    lista_task = []  # salvo le varie combinazioni di task
    makespan_temp_s = 0
    makespan_temp_r = 0
    makespan_candidato_temp = makespan_candidato
    ottimo_candidato_grafo_temp = copia_grafo(grafo_candidato, len(nodi))

    grafo_partenza = copia_grafo(ottimo_candidato_grafo_temp, len(nodi))

    tabu_list = []
    archi_da_decidere = []

    # archi su cui apporto decisioni
    archi_da_decidere = trova_archi(nodi, len(nodi), grafo_disgiuntivo)

    if stampa:
        for a in archi_da_decidere:
            print("Visita: " + str(a.visita) + " Archi: " + str(a.primo_estremo) + "," + str(a.secondo_estremo))

    capacity = int(len(durate) / 2 + len(archi_da_decidere) / 10)

    # numero massimo di iterazioni della tabu search, volendo possiamo impostarlo noi staticamente
    iterazioni = len(nodi) * len(archi_da_decidere)

    max = 0
    for i in range(0, len(durate)):
        if durate[i] > max:
            max = durate[i]
    max_makespan = max * len(nodi)
    makespan = max_makespan
    #iterazioni = 3
    while iterazioni > 0:
        iterazioni -= iterazioni
        # cerco i possibili altri archi che posso creare
        archi_esistenti = []
        archi_esistenti = trova_archi_esistenti(nodi, len(nodi), grafo_disgiuntivo, archi_da_decidere, grafo_partenza)

        for a in archi_esistenti:
            if stampa:
                print("Visita: " + str(a.visita) + " Archi: " + str(a.primo_estremo) + "," + str(a.secondo_estremo))

            s = swap(archi_esistenti, grafo_partenza, len(nodi), tabu_list, nodi, durate, makespan_candidato_temp,
                     stampa)
            makespan_temp_s = s.makespan
            # add lista dei makespan trovati con lo swap
            lista_makespan = lista_makespan + s.lista_makespan

            lista_task = check_best_lista_task(s.lista_tot, lista_task)

            r = remove(archi_da_decidere, grafo_partenza, len(nodi), tabu_list, nodi, durate, makespan_candidato_temp,
                       grafo_disgiuntivo)
            makespan_temp_r = r.makespan

            # add lista dei makespan trovati con la remove
            # lista_makespan = lista_makespan + r.lista_makespan
            if makespan_temp_r == makespan_temp_s and makespan_temp_r == max_makespan:
                if stampa:
                    print("nessuna mossa disponibile")
                iterazioni = 0
            elif makespan_temp_r < makespan_temp_s:
                makespan = makespan_temp_r
                m = r.Mossa
                inversa = Mossa(m.tipo, m.m, m.pisa, m.sisa, m.pipa, m.sipa)
                grafo_partenza = copia_grafo(r.grafo, len(nodi))

                if not m in tabu_list and not inversa in tabu_list:
                    if len(tabu_list) < capacity:
                        tabu_list.append(inversa)
                    else:
                        tabu_list.remove(tabu_list[0])
                        tabu_list.append(inversa)

                elif m in tabu_list and not inversa in tabu_list:
                    index = tabu_list.index(m)
                    tabu_list.remove(index)
                    tabu_list.append(inversa)
                elif inversa in tabu_list and not m in tabu_list:
                    index = tabu_list.index(inversa)
                    tabu_list.remove(index)
                    tabu_list.append(inversa)

            elif makespan_temp_s <= makespan_temp_s and makespan_temp_s != max_makespan:
                makespan = makespan_temp_s
                grafo_partenza = copia_grafo(s.grafo, len(nodi))

                if not s.Mossa in tabu_list:
                    if len(tabu_list) < capacity:
                        tabu_list.append(s.Mossa)
                    else:
                        tabu_list.remove(tabu_list[0])
                        tabu_list.append(s.Mossa)
                # se la mossa swap è già in tabù list la ricolloco in fondo
                else:
                    index = tabu_list.index(s.Mossa)
                    tabu_list.remove(index)
                    tabu_list.append(s.Mossa)

            # se il risultato appena ottenuto è migliore dell'ottimo candidato allora sostituisco l'ottimo candidato
            if makespan < makespan_candidato_temp:
                makespan_candidato_temp = makespan
                ottimo_candidato_grafo_temp = copia_grafo(grafo_partenza, len(nodi))
                lista_makespan.append(makespan)

        s = Solution(ottimo_candidato_grafo_temp, makespan_candidato_temp, Mossa('f', 0, 0, 0, 0, 0), lista_makespan,
                     lista_task)

        return s


def check_best_lista_task(slista_tot, lista_task):
    if not lista_task: # se la lista è vuota la inizializzo
        lista_task = slista_tot
    elif lista_task:
        m = 0
        for l in slista_tot: # prendo valore del più grande end
            if l.end >= m:
                m = l.end
        p = 0
        for k in lista_task: # prendo valore del più grande end
            if k.end >= p:
                p = k.end
        if p >= m:           # se end della nuova lista è minore o uguale a end della vecchia sostituisco la lista task
            lista_task = slista_tot

    return lista_task


# def greedyrandomizedCostruction():

