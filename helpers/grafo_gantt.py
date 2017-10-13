import plotly
from helpers.struct_p import *

plotly.tools.set_credentials_file(username='ArtPes', api_key='j4jXzdxLByLHpizcgmIN')
import plotly.plotly as py
import plotly.figure_factory as ff

import main


def grafico_gantt(lista1, lista2, lista3):
    df = []

    for t in lista1:
        start, end = trovaS_E(t)
        a = dict(Task='Sala' + str(t.sala), Start="2017-01-01 " + start + ":00:00",
                 Finish='2017-01-01 ' + end + ":00:00", Resource='Test' + str(t.test))
        df.append(a)

    for t in lista2:
        start, end = trovaS_E(t)
        a = dict(Task='Sala' + str(t.sala), Start="2017-01-01 " + start + ":00:00",
                 Finish='2017-01-01 ' + end + ":00:00", Resource='Test' + str(t.test))
        df.append(a)

    for t in lista3:
        start, end = trovaS_E(t)
        a = dict(Task='Sala' + str(t.sala), Start="2017-01-01 " + start + ":00:00",
                 Finish='2017-01-01 ' + end + ":00:00", Resource='Test' + str(t.test))
        df.append(a)

    colors = dict(Test1='rgb(0, 255, 0)',
                  Test2='rgb(198, 47, 105)',
                  Test4='rgb(0, 204, 204)',
                  Test5='rgb(46, 137, 205)',
                  Test3='rgb(255, 255, 0)')

    fig = ff.create_gantt(df, colors=colors, index_col='Resource', show_colorbar=True, group_tasks=True)
    py.plot(fig, filename='gantt-dictioanry-colors', world_readable=True)

def trovaS_E(t):
    i = 0
    trovatoE = False
    trovatoS = False
    if t.start < 10:
        while i < 10 and not trovatoS:
            if t.start == i:
                start = '0' + str(i)
                trovatoS = True
            i += 1
    elif t.start > 9:
        while not trovatoS:
            if t.start == i:
                start = str(i)
                trovatoS = True
            i += 1
    if t.end < 10:
        while i < 10 and not trovatoE:
            if t.end == i:
                end = '0' + str(i)
                trovatoE = True
            i += 1
    elif t.end > 9:
        while not trovatoE:
            if t.end == i:
                end = str(i)
                trovatoE = True
            i += 1

    return start, end

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

    #sala1, sala2, sala3 = black_box(sala1, sala2, sala3)

    # vincoli start-end tra pazienti della stessa sala
    vincoli_tra_paz_stessa_sala(sala1,0)
    vincoli_tra_paz_stessa_sala(sala2,0)
    vincoli_tra_paz_stessa_sala(sala3,0)

    # vincoli tra pazienti delle 3 salette (test non si sovrappongono)
    vincolo_tra_test_uguali(sala1,sala2,sala3)

    '''
    for i in sala1:
            print("Paziente:" + str(i.paziente) + " Sala:" + str(i.sala) + " Test:" + str(i.test) + " Start:" + str(
                i.start) + " End: " + str(i.end))
    for i in sala2:
            print("Paziente:" + str(i.paziente) + " Sala:" + str(i.sala) + " Test:" + str(i.test) + " Start:" + str(
                i.start) + " End: " + str(i.end))
    for i in sala3:
            print("Paziente:" + str(i.paziente) + " Sala:" + str(i.sala) + " Test:" + str(i.test) + " Start:" + str(
                i.start) + " End: " + str(i.end))
    '''
    return sala1, sala2, sala3

def vincolo_tra_test_uguali(lista1, lista2, lista3):

    occupato1 = True
    occupato2 = True
    occupato3 = True
    occupato4 = True
    occupato5 = True
    bool = [occupato1, occupato2, occupato3, occupato4, occupato5]

    for t in range(0, 1000):  # ciclo ogni istante del grafo
        for i in range(0,100):
            if i<len(lista1): #se non sono oltre la fine della lista
                if lista1[i].start == t and bool[lista1[i].test-1]: # se lo start è a t e operatore libero
                    bool[lista1[i].test-1] = False # metto a false il test n-esimo
                elif lista1[i].end == t and not bool[lista1[i].test-1]: # se sono al termine del task
                    bool[lista1[i].test - 1] = True
                elif lista1[i].start == t and not bool[lista1[i].test-1]: # se mi serve l'operatore ma è già occupato
                    shift_list(lista1,1,i) # shifto in avanti tutti i test di solo 1 cosi al prossimo ciclo faccio il check

            if i < len(lista2): #se non sono oltre la fine della lista
                if lista2[i].start == t and bool[lista2[i].test-1]: # se lo start è a t e operatore libero
                    bool[lista2[i].test-1] = False # metto a false il test n-esimo
                elif lista2[i].end == t and not bool[lista2[i].test-1]: # se sono al termine del task
                    bool[lista2[i].test - 1] = True
                elif lista2[i].start == t and not bool[lista2[i].test-1]: # se mi serve l'operatore ma è già occupato
                    shift_list(lista2,1,i) # shifto in avanti tutti i test di solo 1 cosi al prossimo ciclo faccio il check

            if i < len(lista3): #se non sono oltre la fine della lista
                if lista3[i].start == t and bool[lista3[i].test-1]: # se lo start è a t e operatore libero
                    bool[lista3[i].test-1] = False # metto a false il test n-esimo
                elif lista3[i].end == t and not bool[lista3[i].test-1]: # se sono al termine del task
                    bool[lista3[i].test - 1] = True
                elif lista3[i].start == t and not bool[lista3[i].test-1]: # se mi serve l'operatore ma è già occupato
                    shift_list(lista3,1,i) # shifto in avanti tutti i test di solo 1 cosi al prossimo ciclo faccio il check
    return lista1,lista2,lista3

def shift_list(list, shift, index):
    # shift dall'indice i-esimo in poi, nno tutti i task della lista
    for i in range(index, len(list)):
        list[i].start = list[i].start + shift
        list[i].end = list[i].end + shift

def vincoli_tra_paz_stessa_sala(sala, index):
    for i in range(index, len(sala)):  # parto da i-esimo elemento perchè non devo sempre settare tutta la lista
        if not i == len(sala)-1:  # se non sono arrivato all'ultimo task
            if sala[i + 1].start < sala[i].end:
                    sala[i + 1].start = sala[i].end
                    sala[i+1].end = sala[i+1].start+sala[i+1].durata
            elif sala[i + 1].start >= sala[i].end:
                sala[i + 1].start = sala[i].end
                sala[i + 1].end = sala[i + 1].start + sala[i + 1].durata

def insert_task_da_nodo(nodo):
    list_task = []
    # creo il task relativo a ogni paziente
    for i in range(1, len(nodo)-1):
        task = crea_task_da_nodo(nodo[i])
        #print("Paz: " + str(task.paziente) + " Sala: " + str(task.sala) + " Test: " + str(task.test) + " Start: " + str(
            #task.start))
        list_task.append(task)
    return list_task

def crea_task_da_nodo(nodo):
    task = Task(nodo.idP, nodo.sala, int(nodo.visita),0)
    return task

def elimina_nodi(tasks):
    for t in tasks:
        if t.sala == 0: #nei nodi start-end la sala è impostata a 0
            tasks.remove(t)

# ---------------------------------------------------------------------
def black_box(ts1, ts2, ts3):
    ttot = 0  # tempo totale esecuzione
    # #tempi totali per ogni saletta
    tt1 = 0
    tt2 = 0
    tt3 = 0
    check_box = False
    ## tempi per rilascio evitare la sovrapposizione di job
    tmp1 = 110
    tmp2 = 110
    tmp3 = 110
    # variabile per evitare il sovrapporsi di op
    test_before = []
    # lock per test -->mutua esclusione
    t1 = False
    t2 = False
    t3 = False
    t4 = False
    t5 = False
    lock = []  # a che saletta do il lock  -->a chi do la mutua esclusione
    # contatori 3 salette
    c1 = 0
    c2 = 0
    c3 = 0
    # contatori 3 salette temporanei
    c1t = 0
    c2t = 0
    c3t = 0
    # setto una variabile per ogni saletta se sta facendo un test in maniera
    # da poter incrementare il tempo di uno puramente nel caso sia in idle
    idles1 = False
    idles2 = False
    idles3 = False
    # Inizializzo i lock
    for i in range(0, 5):
        lock.append('')
    # Inizializzo variabili test prec
    for i in range(0, 3):
        test_before.append(0)

    # idles1,idles2,idles3=False
    while check_box is False:
        # check_box variabile che mi serve per ciclare(finche' tutti e 3 gli indici son stati esauriti rimane a false)
        # controllo per lunghezza task ts1

        #                          ----------- SALA 1 --------
        if c1 < len(ts1):

            # ------------          test 1 per task sala 1      -------
            if ts1[c1t].test == 1:
                if t1 == True and lock[0] != "s1" and idles1 == False:
                    tt1 += 1

                if t1 == True and lock[0] == "s1":
                    if tt1 >= ts1[c1t].end:
                        lock[0] = ''
                        t1 = False
                        tmp1 = tt1
                        test_before[0] = 1
                        c1 += 1
                        idles1 = False
                    else:
                        tt1 += 1
                elif t1 == False and (test_before[1] != 1 and test_before[2] != 1):
                    if ts1[
                        c1t].test == 1:  # and (test_before[1]!=1 or test_before[2]!=1 ): #reinserisco il controllo perchè mi rifarebbe la stessa visita
                        ts1[c1t].start = tt1
                        ts1[c1t].end = tt1 + 1
                        tt1 += 1
                        t1 = True
                        lock[0] = "s1"
                        idles1 = True

                        # else:
                        # tt1+=1
            # ------------          test 2 per task sala 1      -------
            if ts1[c1t].test == 2:
                if t2 == True and lock[1] != "s1" and idles1 == False:
                    tt1 += 1

                if t2 == True and lock[1] == "s1":
                    if tt1 >= ts1[c1t].end:
                        lock[1] = ''
                        t2 = False
                        c1 += 1
                        tmp1 = tt1
                        test_before[0] = 2
                        idles1 = False
                    else:
                        tt1 += 1
                elif t2 == False and (test_before[1] != 2 and test_before[2] != 2):
                    if ts1[c1t].test == 2:  # and (test_before[1]!=2 or test_before[2]!=2 ):
                        ts1[c1t].start = tt1
                        ts1[c1t].end = tt1 + 2
                        tt1 += 1
                        t2 = True
                        lock[1] = "s1"
                        idles1 = True

                        # else:
                        # tt1+=1
            # ------------          test 3 per task sala 1      -------
            if ts1[c1t].test == 3:
                if t3 == True and lock[2] != "s1" and idles1 == False:
                    tt1 += 1

                if t3 == True and lock[2] == "s1":
                    if tt1 >= ts1[c1t].end:
                        lock[2] = ''
                        t3 = False
                        tmp1 = tt1
                        test_before[0] = 3
                        c1 += 1
                        idles1 = False
                    else:
                        tt1 += 1
                elif t3 == False and (test_before[1] != 3 and test_before[2] != 3):
                    if ts1[c1t].test == 3:
                        ts1[c1t].start = tt1
                        ts1[c1t].end = tt1 + 4
                        tt1 += 1
                        t3 = True
                        lock[2] = "s1"
                        idles1 = True

                        # else:
                        # tt1+=1
            # ------------          test 4 per task sala 1      -------
            if ts1[c1t].test == 4:
                if t4 == True and lock[3] != "s1" and idles1 == False:
                    tt1 += 1

                # se i tempi vengono sballati di uno bisogna invertire queste due condizioni
                if t4 == True and lock[3] == "s1":
                    if tt1 >= ts1[c1t].end:
                        lock[3] = ''
                        t4 = False
                        c1 += 1
                        test_before[0] = 4
                        tmp1 = tt1
                        idles1 = False
                    else:
                        tt1 += 1
                elif t4 == False and (test_before[1] != 4 and test_before[2] != 4):
                    if ts1[c1t].test == 4:
                        ts1[c1t].start = tt1
                        ts1[c1t].end = tt1 + 6
                        tt1 += 1
                        t4 = True
                        lock[3] = "s1"
                        idles1 = True

                        # else:
                        # tt1+1
            # ------------          test 5 per task sala 1      -------
            if ts1[c1t].test == 5:
                if t5 == True and lock[4] != "s1" and idles1 == False:  # and (test_before[1]==5 or test_before[2]==5 ):
                    tt1 += 1

                # se i tempi vengono sballati di uno bisogna invertire queste due condizioni
                if t5 == True and lock[4] == "s1":
                    if tt1 >= ts1[c1t].end:
                        lock[4] = ''
                        t5 = False
                        c1 += 1
                        test_before[0] = 5
                        tmp1 = tt1
                        idles1 = False
                    else:
                        tt1 += 1
                elif t5 == False and (test_before[1] != 5 and test_before[2] != 5):
                    if ts1[c1t].test == 5:
                        ts1[c1t].start = tt1
                        ts1[c1t].end = tt1 + 8
                        tt1 += 1
                        t5 = True
                        lock[4] = "s1"
                        idles1 = True

                        # else:
                        # tt1+=1
        # ----------- SALA 2 --------
        if c2 < len(ts2):

            # tt2+=1
            # ------------          test 1 per task sala 2      -------
            if ts2[c2t].test == 1:
                if t1 == True and lock[0] != "s2" and idles2 == False:  # and (test_before[0]==1 or test_before[2]==1 ):
                    tt2 += 1

                if t1 == True and lock[0] == "s2":
                    if tt2 >= ts2[c2t].end:
                        lock[0] = ''
                        t1 = False
                        c2 += 1
                        test_before[1] = 1
                        tmp2 = tt2
                        idles2 = False
                    else:
                        tt2 += 1
                elif t1 == False and (test_before[0] != 1 and test_before[2] != 1):
                    if ts2[c2t].test == 1:
                        # reinserisco il controllo perchè mi rifarebbe la stessa visita
                        ts2[c2t].start = tt2
                        ts2[c2t].end = tt2 + 1
                        tt2 += 1
                        t1 = True
                        lock[0] = "s2"
                        idles2 = True
                elif t1 == False and (test_before[0] == 1 or test_before[2] == 1):
                    if (test_before[0] == 1):
                        tt2 = ts1[c1t].end

                        # else:
                        # tt2+=1
            # ------------          test 2 per task sala 2      -------
            if ts2[c2t].test == 2:
                if t2 == True and lock[1] != "s2" and idles2 == False:  # and (test_before[0]==2 or test_before[2]==2 ):
                    tt2 += 1

                if t2 == True and lock[1] == "s2":
                    if tt2 >= ts2[c2t].end:
                        lock[1] = ''
                        t2 = False
                        c2 += 1
                        test_before[1] = 2
                        tmp2 = tt2
                        idles2 = False
                    else:
                        tt2 += 1
                elif t2 == False and (test_before[0] != 2 and test_before[2] != 2):
                    if ts2[c2t].test == 2:
                        ts2[c2t].start = tt2
                        ts2[c2t].end = tt2 + 2
                        tt2 += 1
                        t2 = True
                        lock[1] = "s2"
                        idles2 = True
                elif t2 == False and (test_before[0] == 2 or test_before[2] == 2):
                    if (test_before[0] == 2):
                        tt2 = ts1[c1t].end
                        # else:
                        # tt2+=1
            # ------------          test 3 per task sala 2      -------
            if ts2[c2t].test == 3:
                if t3 == True and lock[2] != "s2" and idles2 == False:  # and (test_before[0]==3 or test_before[2]==3 ):
                    tt2 += 1

                if t3 == True and lock[2] == "s2":
                    if tt2 >= ts2[c2t].end:
                        lock[2] = ''
                        t3 = False
                        c2 += 1
                        tmp2 = tt2
                        test_before[1] = 3
                        idles2 = False
                    else:
                        tt2 += 1
                elif t3 == False and (test_before[0] != 3 and test_before[2] != 3):
                    if ts2[c2t].test == 3:
                        ts2[c2t].start = tt2
                        ts2[c2t].end = tt2 + 4
                        tt2 += 1
                        t3 = True
                        lock[2] = "s2"
                        idles2 = True
                elif t3 == False and (test_before[0] == 3 or test_before[2] == 3):
                    if (test_before[0] == 3):
                        tt2 = ts1[c1t].end
                        # else:
                        # tt2+=1
            # ------------          test 4 per task sala 2      -------
            if ts2[c2t].test == 4:
                if t4 == True and lock[3] != "s2" and idles2 == False:  # and (test_before[0]==4 or test_before[2]==4 ):
                    tt2 += 1

                # se i tempi vengono sballati di uno bisogna invertire queste due condizioni
                if t4 == True and lock[3] == "s2":
                    if tt2 >= ts2[c2t].end:
                        lock[3] = ''
                        t4 = False
                        c2 += 1
                        test_before[1] = 4
                        tmp2 = tt2
                        idles2 = False
                    else:
                        tt2 += 1
                elif t4 == False and (test_before[0] != 4 and test_before[2] != 4):
                    if ts2[c2t].test == 4:
                        ts2[c2t].start = tt2
                        ts2[c2t].end = tt2 + 6
                        tt2 += 1
                        t4 = True
                        lock[3] = "s2"
                        idles2 = True
                elif t4 == False and (test_before[0] == 4 or test_before[2] == 4):
                    if (test_before[0] == 4):
                        tt2 = ts1[c1t].end
                        # else:
                        # tt2+=1
            # ------------          test 5 per task sala 2      -------
            if ts2[c2t].test == 5:
                if t5 == True and lock[4] != "s2" and idles2 == False:  # and (test_before[0]==5 or test_before[2]==5 ):
                    tt2 += 1

                # se i tempi vengono sballati di uno bisogna invertire queste due condizioni
                if t5 == True and lock[4] == "s2":
                    if tt2 >= ts2[c2t].end:
                        lock[4] = ''
                        t5 = False
                        c2 += 1
                        test_before[1] = 5
                        tmp2 = tt2
                        idles2 = False
                    else:
                        tt2 += 1
                elif t5 == False and (test_before[0] != 5 and test_before[2] != 5):
                    if ts2[c2t].test == 5:
                        ts2[c2t].start = tt2
                        ts2[c2t].end = tt2 + 8
                        tt2 += 1
                        t5 = True
                        lock[4] = "s2"
                        idles2 = True
                elif t5 == False and (test_before[0] == 5 or test_before[2] == 5):
                    if (test_before[0] == 5):
                        tt2 = ts1[c1t].end
                        # else:
                        # tt2+=1
        # ----------- SALA 3--------
        if c3 < len(ts3):

            # ------------          test 1 per task sala 3      -------
            # tt3+=1
            if ts3[c3t].test == 1:
                if t1 == True and lock[0] != "s3" and idles3 == False:  # and (test_before[0]==1 or test_before[1]==1 ):
                    tt3 += 1

                if t1 == True and lock[0] == "s3":
                    if tt3 >= ts3[c3t].end:
                        lock[0] = ''
                        t1 = False
                        c3 += 1
                        test_before[2] = 1
                        tmp3 = tt3
                        idles3 = False
                    else:
                        tt3 += 1
                elif t1 == False and (test_before[0] != 1 and test_before[1] != 1):
                    if ts3[c3t].test == 1:
                        # reinserisco il controllo perchè mi rifarebbe la stessa visita
                        ts3[c3t].start = tt3
                        ts3[c3t].end = tt3 + 1
                        tt3 += 1
                        t1 = True
                        lock[0] = "s3"
                        idles3 = True
                elif t1 == False and (test_before[0] == 1 or test_before[1] == 1):
                    if test_before[0] == 1:
                        tt3 = ts1[c1t].end
                    elif test_before[1] == 1:
                        tt3 = ts2[c2t].end
                        # else:
                        # tt3+=1
            # ------------          test 2 per task sala 3      -------
            if ts3[c3t].test == 2:
                if t2 == True and lock[1] != "s3" and idles3 == False:  # and (test_before[0]==2 or test_before[1]==2 ):
                    tt3 += 1

                if t2 == True and lock[1] == "s3":
                    if tt3 >= ts3[c3t].end:
                        lock[1] = ''
                        t2 = False
                        c3 += 1
                        test_before[2] = 2
                        tmp3 = tt3
                        idles3 = False
                    else:
                        tt3 += 1
                elif t2 == False and test_before[0] != 2 and test_before[1] != 2:
                    if ts3[c3t].test == 2:
                        ts3[c3t].start = tt3
                        ts3[c3t].end = tt3 + 2
                        tt3 += 1
                        t2 = True
                        lock[1] = "s3"
                        idles3 = True
                elif t2 == False and (test_before[0] == 2 or test_before[1] == 2):
                    if test_before[0] == 2:
                        tt3 = ts1[c1t].end
                    elif test_before[1] == 2:
                        tt3 = ts2[c2t].end
                        # else:
                        # tt3+=1
            # ------------          test 3 per task sala 3      -------
            if ts3[c3t].test == 3:
                if t3 == True and lock[2] != "s3" and idles3 == False:  # and (test_before[0]==3 or test_before[1]==3 ):
                    tt3 += 1

                if t3 == True and lock[2] == "s3":
                    if tt3 >= ts3[c3t].end:
                        lock[2] = ''
                        t3 = False
                        c3 += 1
                        test_before[2] = 3
                        tmp3 = tt3
                        idles3 = False
                    else:
                        tt3 += 1
                elif t3 == False and test_before[0] != 3 and test_before[1] != 3:
                    if ts3[c3t].test == 3:
                        ts3[c3t].start = tt3
                        ts3[c3t].end = tt3 + 4
                        tt3 += 1
                        t3 = True
                        lock[2] = "s3"
                        idles3 = True
                elif t3 == False and (test_before[0] == 3 or test_before[1] == 3):
                    if test_before[0] == 3:
                        tt3 = ts1[c1t].end
                    elif test_before[1] == 3:
                        tt3 = ts2[c2t].end
                        # else:
                        # tt3+=1

            # ------------          test 4 per task sala 3      -------
            if ts3[c3t].test == 4:
                if t4 == True and lock[3] != "s3" and idles3 == False:  # and (test_before[0]==4 or test_before[1]==4 ):
                    tt3 += 1

                # se i tempi vengono sballati di uno bisogna invertire queste due condizioni
                if t4 == True and lock[3] == "s3":
                    if tt3 >= ts3[c3t].end:
                        lock[3] = ''
                        t4 = False
                        c3 += 1
                        test_before[2] = 4
                        tmp3 = tt3
                        idles3 = False
                    else:
                        tt3 += 1
                elif t4 == False and (test_before[0] != 4 and test_before[1] != 4):
                    if ts3[c3t].test == 4:
                        ts3[c3t].start = tt3
                        ts3[c3t].end = tt3 + 6
                        tt3 += 1
                        t4 = True
                        lock[3] = "s3"
                        idles3 = True
                elif t4 == False and (test_before[0] == 4 or test_before[1] == 4):
                    if test_before[0] == 4:
                        tt3 = ts1[c1t].end
                    elif test_before[1] == 4:
                        tt3 = ts2[c2t].end
                        # else:
                        # tt3+=1
            # ------------          test 5 per task sala 3      -------
            if ts3[c3t].test == 5:
                if t5 == True and lock[4] != "s3" and idles3 == False:  # and (test_before[0]==5 or test_before[1]==5 ):
                    tt3 += 1

                # se i tempi vengono sballati di uno bisogna invertire queste due condizioni
                if t5 == True and lock[4] == "s3":
                    if tt3 >= ts3[c3t].end:
                        lock[4] = ''
                        t5 = False
                        c3 += 1
                        test_before[2] = 5
                        tmp3 = tt3
                        idles3 = False
                    else:
                        tt3 += 1
                elif t5 == False and test_before[0] != 5 and test_before[1] != 5:
                    if ts3[c3t].test == 5:
                        ts3[c3t].start = tt3
                        ts3[c3t].end = tt3 + 8
                        tt3 += 1
                        t5 = True
                        lock[4] = "s3"
                        idles3 = True
                elif t5 == False and (test_before[0] == 5 or test_before[1] == 5):
                    if test_before[0] == 5:
                        tt3 = ts1[c1t].end
                    elif test_before[1] == 5:
                        tt3 = ts2[c2t].end
                        # else:
                        # tt3+=1
        if tmp1 == tt1:
            test_before[0] = 0
        if tmp2 == tt2:
            test_before[1] = 0
        if tmp3 == tt3:
            test_before[2] = 0
        ttot += 1

        c1t = c1
        c2t = c2
        c3t = c3
        a = len(ts1)
        b = len(ts2)
        c = len(ts3)
        if c1 == a and c2 == b and c3 == c:
            check_box = True;

    print("\ntt1\n" + str(tt1))
    print("\n tt2 \n" + str(tt2))
    print("\ntt3\n" + str(tt3))
    return ts1, ts2, ts3