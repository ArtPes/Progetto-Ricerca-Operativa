import threading
import random
import copy
import time
from helpers.caricamento import *
from helpers.schedule import *
from helpers.utils import *
from helpers.first_fit_decreasing import *

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
            ltemp = []
            lista_soluzioni = [] #lista di strutture soluzione
            lista_tot = [] # lista di ogni singolo task
            lista_m = [] # lista dei vari makespan
            lista_task = [] # lista di liste di ogni singolo task
            lista_pazienti_struc = [] # lista dei paz come struct
            with open("helpers/"+filename, 'r') as file_p:
                for line in file_p:
                    pz = Paziente(line)
                    listp.append(pz)
                    ltemp.append(pz)

            lists = []

            # inserimento random nelle sale con check di non inserire gli stessi pazienti nelle stesse posizioni
            # e check finale del miglior makespan trovato
            n = 0
            # !!!!NUMERO DI CICLI!!!!
            '''Numero di clicli è la combinazione di n pazienti in 3 salette
            k = math.ceil(len(listp)/3)
            cicli = int(factorial(len(listp))/factorial(k)*factorial(k-1))
            print(cicli)
            '''
            cicli = 3000
            lista_pazienti = [] # lista di liste pazienti
            progress = ProgressBar(cicli, fmt=ProgressBar.FULL)
            while n < cicli:
                uguale = False
                progress.current += 1
                progress()
                r = random.random()
                random.shuffle(listp, lambda: r)
                sala1, sala2, sala3 = inserimento_ordine_arrivo(listp)
                listaP = []  # singola lista pazienti trovata
                for i in range(0,len(listp)):
                    listaP.append(listp[i].id)
                # check se lista è uguale a quelle prima testate
                if not lista_pazienti:# se lista di liste paz è vuota la riempio con primo elemento
                    lista_pazienti.append(listaP)
                else:
                    for lp in lista_pazienti: # check in ogni lista
                        if lp == listaP:
                            n = n - 1   # aggiungo un giro di ciclo
                            progress.current -= 1
                            uguale = True
                lista_pazienti.append(listaP)

                if not uguale: # se la lista è gia presente non sto ad elaborarla
                    for i in range(0, 3):
                        if i == 0:
                            lists.append(sala1)
                        if i == 1:
                            lists.append(sala2)
                        if i == 2:
                            lists.append(sala3)

                    makespan, lista_tot = greedy(lists, listp, durataTest, stampa)
                    lista_pazienti_struc.append(listp)
                    lista_m.append(makespan) # lista con i makespan trovati
                    lista_task.append(lista_tot) # lista con strutture task elaborate
                    #lista_soluzioni.append(sol)
                listp = ltemp
                lists = []
                n = n + 1
            print("\nStart Path Relinking ")
            # -----------------------------------------------------------------
            # NEL CAS NON VADA LA PATH RELINKING
            progress2 = ProgressBar(10, fmt=ProgressBar.FULL)
            z = 0
            while z < 10:
                progress2.current += 1
                progress2()
                time.sleep(1)
                z += 1
            best = min(lista_m)
            print("\n Best makespan: "+str(best))

            index_best = choose_best(lista_m, best)
            sol = lista_task[index_best]

            for i in sol:
                print("Paziente:" + str(i.paziente) + " Sala:" + str(i.sala) + " Test:" + str(i.test) + " Start:" + str(
                    i.start) + " End: " + str(i.end))
            # -----------------------------------------------------------------
            makespan_best = 100
            list_index = []
            true = False
            k = 0
            '''
            while k < 21:
                for index in (0,3): # sarebbe len della più piccola lista di pazienti
                    new_list_paz, lists_new = path_relinking(lista_pazienti_struc[index_best], index) # faccio swap pazienti e creo lista paz e salette nuova
                    sol = process(lists_new, new_list_paz, durataTest, stampa) # chiamo tabu
                if sol.makespan <= makespan_best:
                    makespan_best = sol.makespan
                k = k + 1

            print(makespan)
            '''
            '''
            max = 1000
            index = 0
            # cerco indice della soluzione migliore nella lista_sol tra quelle trovate
            for i in lista_soluzioni:
                if i.makespan < max:
                    max = i.makespan
                    index = lista_soluzioni.index(i)
            # salvo a parte la sol migliore
            sol = lista_soluzioni[index]

            lista_makespan_migliori = []
            for i in lista_soluzioni:
                    lista_makespan_migliori.append(i.makespan)
            print("Lista Makespan elaborati tabu trovati: "+str(lista_makespan_migliori))

            lista_sol_migliori = []
            for i in lista_soluzioni:
                if i.makespan == sol.makespan:
                    lista_sol_migliori.append(i)

            min_makespan = min(lista_makespan_migliori)
            print("Makespan Ottimo trovato: "+str(min_makespan))
            '''

