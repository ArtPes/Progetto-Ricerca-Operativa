import threading
import random
import copy

import time

from helpers.schedule import *
from helpers.utils import *
from helpers.first_fit_decreasing import *
from tqdm import tqdm

if __name__ == "__main__":

    out_lck = threading.Lock()
    # da settare qui le durate e nel file struct_p.py
    durataTest = [1, 2, 4, 6, 8]

    while True:
        # Main Menu
        ListPaz = []
        i = 1
        print("\n")
        for file in os.listdir("helpers"):
            if file.endswith(".txt"):
                print(i, file)
                ListPaz.append(str(file))
                i += 1
        nfile = loop_int_input(out_lck, "Scegliere un file file")
        nf = int(nfile) - 1
        filename = copy.copy(ListPaz[nf])

        main_menu = loop_menu(out_lck, "\nSelect one of the following actions ('e' to exit): ",
                              ["Pazienti Ordinati First Fit Decreasing + Tabu Search", "Pazienti inseriti con ordine di arrivo + Tabu Search",
                               "Random Search + Path Relinking"])

        if main_menu == 1:
            print("Stampa di tutte le info? 1 Si   2 No")
            a = input()
            if int(a) == 1:
                stampa = True
            elif int(a) == 2:
                stampa = False
            listp = []
            with open("helpers/"+filename, 'r') as file_p:
                for line in file_p:
                    pz = Paziente(line)
                    listp.append(pz)

            # inserimento nelle sale
            packAndShow(listp)

            sala1, sala2, sala3 = inserimento_sala(listp)
            lists = []
            for i in range(0, 3):
                if i == 0:
                    lists.append(sala1)
                if i == 1:
                    lists.append(sala2)
                if i == 2:
                    lists.append(sala3)
            # può capitare che metta solo pazienti in due sale
            if not sala1 or not sala2 or not sala3:
                print("Errore, no pazienti in una sala!!")
                stampa_info_paziente(listp)
                break

            stampa_info_paziente(listp)
            sol = process(lists, listp, durataTest, stampa)


            print("\nMAKESPAN FINALE: " + str(sol.makespan))
            if stampa:
                print("\nGrafo finale: ")
                stampa3(sol.grafo)
                for i in sol.lista_tot:
                    print("Paziente:" + str(i.paziente) + " Sala:" + str(i.sala) + " Test:" + str(i.test) + " Start:" + str(
                        i.start) + " End: " + str(i.end))

        elif main_menu == 2:
            print("Stampa di tutte le info? 1 Si   2 No")
            a = input()
            if int(a) == 1:
                stampa = True
            elif int(a) == 2:
                stampa = False
            listp = []
            with open("helpers/"+filename, 'r') as file_p:
                for line in file_p:
                    pz = Paziente(line)
                    listp.append(pz)
            lists = []
            # inserimento random nelle sale
            sala1, sala2, sala3 = inserimento_ordine_arrivo(listp)
            for i in range(0, 3):
                if i == 0:
                    lists.append(sala1)
                if i == 1:
                    lists.append(sala2)
                if i == 2:
                    lists.append(sala3)

            stampa_info_paziente(listp)
            sol = process(lists, listp, durataTest, stampa)


            print("\nMAKESPAN FINALE: " + str(sol.makespan))
            if stampa:
                print("\nGrafo finale: ")
                stampa3(sol.grafo)

                for i in sol.lista_tot:
                    print("Paziente:" + str(i.paziente) + " Sala:" + str(i.sala) + " Test:" + str(i.test) + " Start:" + str(
                        i.start) + " End: " + str(i.end))

        elif main_menu == 3:
            stampa = False
            listp = []
            lista_soluzioni = [] #lista di strutture soluzione
            lista_tot = [] # lista di ogni singolo task
            lista_m = [] # lista dei vari makespan
            lista_task = [] # lista di liste di ogni singolo task
            lista_pazienti_struc = [] # lista dei paz come struct
            with open("helpers/"+filename, 'r') as file_p:
                for line in file_p:
                    pz = Paziente(line)
                    listp.append(pz)

            lists = []
            lista_sale = []
            # inserimento random nelle sale con check di non inserire gli stessi pazienti nelle stesse posizioni
            # e check finale del miglior makespan trovato
            n = 0
            # !!!!NUMERO DI CICLI!!!!
            '''Numero di clicli è la combinazione di n pazienti in 3 salette
            k = math.ceil(len(listp)/3)
            cicli = int(factorial(len(listp))/factorial(k)*factorial(k-1))
            print(cicli)
            '''
            cicli = 10
            lista_pazienti = [] # lista di liste pazienti
            for n in tqdm(range(cicli)):
                uguale = False
                r = random.random()
                lst = []
                random.shuffle(listp, lambda: r)
                sala1, sala2, sala3 = inserimento_ordine_arrivo(listp)
                lst = copy.copy(listp) # copia di una lista di object
                lista_pazienti_struc.append(lst)  # lista con strutture paziente
                listaP = []  # singola lista pazienti trovata
                for i in range(0,len(listp)):
                    listaP.append(listp[i].id)
                # check se lista è uguale a quelle prima testate
                lista_pazienti.append(listaP)
                '''
                if not lista_pazienti:# se lista di liste paz è vuota la riempio con primo elemento
                    lista_pazienti.append(listaP) # lista con id paziente in ordine
                else:
                    for lp in lista_pazienti: # check in ogni lista
                        if lp == listaP:
                            n = n - 1   # aggiungo un giro di ciclo
                            uguale = True
                lista_pazienti.append(listaP) # lista con id paziente in ordine

                if not uguale: # se la lista è gia presente non sto ad elaborarla
                    for i in range(0, 3):
                        if i == 0:
                            lists.append(sala1)
                        if i == 1:
                            lists.append(sala2)
                        if i == 2:
                            lists.append(sala3)
                '''

                for j in range(0, 3):
                    if j == 0:
                        lists.append(sala1)
                    if j == 1:
                        lists.append(sala2)
                    if j == 2:
                        lists.append(sala3)

                makespan, lista_tot = greedy(lists, listp, durataTest, stampa)
                lista_m.append(makespan) # lista con i makespan trovati
                lt = copy.copy(lista_tot)# copia di una lista di object
                lista_task.append(lt) # lista con strutture task elaborate
                lista_sale.append(lists)
                lists = []
                lt = []

                n = n + 1
            time.sleep(2)
            print("\nStart Path Relinking \n")
            time.sleep(2)

            g = 0
            for g in tqdm(range(10)):
                time.sleep(0.1)

            best = min(lista_m)# miglior makespan
            index_best = lista_m.index(best)
            sol_best = lista_task[index_best]


            candidate = find_min(lista_m,best) # prendo secondo miglior makespan
            print("Miglior Makespan trovato: "+str(best))
            print("Makespan candidato scelto: "+str(candidate))
            index_cand = choose_el(lista_m,candidate)
            sol_best_id = lista_pazienti[index_best] #lista con id paz sol best
            sol_candidate_id = lista_pazienti[index_cand]#lista con id paz  sol candidate
            list_pazienti_st = []
            k = 0
            array_makespan = []
            array_task = []
            array_task_p = []
            array_list_id = []
            ap = []
            while k < len(sol_best_id):
                # faccio swap pazienti e creo lista paz e salette nuova
                lists_new, list_pazienti_st = path_relinking(lista_pazienti_struc[index_cand], sol_best_id, sol_candidate_id, k)
                makespan, lista_tot = greedy(lists_new, list_pazienti_st, durataTest, stampa)
                array_makespan.append(makespan)
                ap = copy.copy(lista_tot)
                array_task.append(ap)
                ap = []
                at = copy.copy(list_pazienti_st)
                array_task_p.append(at)
                at = []
                array_list_id.append(lists_new)
                k = k + 1

            #makespan, lista_tot = greedy(lists_new, list_pazienti_st, durataTest, stampa)
            migliore = min(array_makespan)
            index_migliore = array_makespan.index(migliore)

            #for i in array_task[index_migliore]:
            #    print("Paziente:" + str(i.paziente) + " Sala:" + str(i.sala) + " Test:" + str(i.test) + " Start:" + str(
            #       i.start) + " End: " + str(i.end))
            #print(array_list_id[index_migliore])
            print("Makespan rielaborato da candidato: "+str(array_makespan[index_migliore]))
            print("\n Affinamento soluzione con Tabu Search...")
            #for x in array_task_p[index_migliore]:
            #    print(x.id)

            sol = process(array_list_id[index_migliore],array_task_p[index_migliore], durataTest, stampa)
            for i in sol.lista_tot:
                print("Paziente:" + str(i.paziente) + " Sala:" + str(i.sala) + " Test:" + str(i.test) + " Start:" + str(
                    i.start) + " End: " + str(i.end))
            print("\nMakespan finale della Path Relinking: "+str(sol.makespan))

            #print(sol_best_id)
            #print(sol_candidate_id)
            #print(lists_new) # lista immissione sale
            #print("Makespan best: "+str(makespan))



