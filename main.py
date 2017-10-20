import threading
import random
from helpers.prova import *
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
                              ["Pazienti Ordinati First Fit Decreasing", "Pazienti inseriti con ordine di arrivo", "Swap Ordine Pazienti"])

        if main_menu == 1:

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
            stampa = True
            sol = process(lists, listp, durataTest,stampa)

            print("\nGrafo finale: ")
            stampa3(sol.grafo)
            print("\nMAKESPAN FINALE: " + str(sol.makespan))

            for i in sol.lista_tot:
                    print("Paziente:" + str(i.paziente) + " Sala:" + str(i.sala) + " Test:" + str(i.test) + " Start:" + str(i.start) + " End: " + str(i.end))


            # stampa un grafo con tutti i makespan trovati
            # grafo_makespan(sol.lista_makespan,sol.makespan,makespan)


        elif main_menu == 2:
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
            stampa = True
            sol = process(lists, listp, durataTest, stampa)

            print("\nGrafo finale: ")
            stampa3(sol.grafo)
            print("\nMAKESPAN FINALE: " + str(sol.makespan))

            for i in sol.lista_tot:
                    print("Paziente:" + str(i.paziente) + " Sala:" + str(i.sala) + " Test:" + str(i.test) + " Start:" + str(i.start) + " End: " + str(i.end))

            # stampa un grafo con tutti i makespan trovati
            # grafo_makespan(sol.lista_makespan,sol.makespan,makespan)


        elif main_menu == 3:
            listp = []
            ltemp=[]
            lista_soluzioni = []
            with open('helpers/pazienti.txt', 'r') as file_p:
                for line in file_p:
                    pz = Paziente(line)
                    listp.append(pz)
                    ltemp.append(pz)

            lists = []

            # inserimento random nelle sale volendo da ottimizzare con un'euristica
            # anche solo andando a modificare in modo random la disposizione dei pazienti nelle sale il makespan migliora
            n=0

            stampa = False
            while n <5:
                progress = ProgressBar(10, fmt=ProgressBar.FULL)
                for x in range(progress.total):
                    progress.current += 1
                    progress()
                    r = random.random()
                    random.shuffle(listp, lambda: r)
                    sala1, sala2, sala3 = inserimento_ordine_arrivo(listp)
                    for i in range(0, 3):
                        if i == 0:
                            lists.append(sala1)
                        if i == 1:
                            lists.append(sala2)
                        if i == 2:
                            lists.append(sala3)

                    #stampa_info_paziente(listp)
                    sol = process(lists, listp, durataTest, stampa)
                    lista_soluzioni.append(sol)
                    listp = ltemp
                    lists = []
                    n = n + 1
                progress.done()

            max = 1000
            index = 0
            for i in lista_soluzioni:
                if i.makespan < max:
                    max = i.makespan
                    index = lista_soluzioni.index(i)

            sol = lista_soluzioni[index]

            lista_sol_migliori = []
            for i in lista_soluzioni:
                if i.makespan== sol.makespan:
                    lista_sol_migliori.append(i)

            for i in lista_sol_migliori:
                print(i.makespan)

            for i in range(0, len(lista_sol_migliori)):
                if i<len(lista_sol_migliori)-1:
                    if lista_sol_migliori[i].lista_tot == lista_sol_migliori[i+1].lista_tot:
                        print("Uguali")
                    else:
                        print("Diversi"+str(i))

            #print("\nGrafo Migliore finale: ")
            #stampa3(sol.grafo)
            #print("\nMAKESPAN MIGLIORE FINALE: " + str(sol.makespan))

            # stampa un grafo con tutti i makespan trovati
            # grafo_makespan(sol.lista_makespan,sol.makespan,makespan)


