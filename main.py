import threading
import random
from math import *

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
        main_menu = loop_menu(out_lck, "\nSelect one of the following actions ('e' to exit): ",
                              ["Pazienti Ordinati First Fit Decreasing", "Pazienti inseriti con ordine di arrivo",
                               "Swap Ordine Pazienti"])

        if main_menu == 1:
            print("Stampa di tutte le info? 1 Si   2 No")
            a = input()
            if int(a) == 1:
                stampa = True
            elif int(a) == 2:
                stampa = False
            listp = []
            with open('helpers/pazienti.txt', 'r') as file_p:
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
            with open('helpers/pazienti.txt', 'r') as file_p:
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
            lista_soluzioni = []
            with open('helpers/pazienti.txt', 'r') as file_p:
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
            cicli = 100
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

                    sol = process(lists, listp, durataTest, stampa)
                    lista_soluzioni.append(sol)
                listp = ltemp
                lists = []
                n = n + 1

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



