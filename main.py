import math
import threading
from helpers.struct import *
import random
from helpers.utils import *
from helpers.first_fit_decreasing import *

if __name__ == "__main__":

    out_lck = threading.Lock()

    while True:
        # Main Menu
        main_menu = loop_menu(out_lck, "\nSelect one of the following actions ('e' to exit): ",
                              ["Pazienti Ordinati su Durata test", "Pazienti già inseriti"])

        if main_menu == 1:
            listp = []
            with open('helpers/pazienti.txt', 'r') as file_p:
                for line in file_p:
                    # output(out_lck,line)
                    pz = Paziente(line)
                    # output(out_lck, "Paziente: " + str(pz.id) + "  Test: " + pz.test_array)
                    listp.append(pz)

            lista_durate = []

            for i in range(0, len(listp)):
                durata = Paziente.somma_durata_singolo(listp[i])
                # output(out_lck, "Durata tot: " + str(durata))
                lista_durate.append(durata)

            durata_tot = sum(lista_durate)
            # output(out_lck, "Durata totale test: " + str(durata_tot))

            # calcolo la durata media per saletta
            durata_sal = durata_tot / 3
            # output(out_lck, "Durata media per saletta: " + str(durata_sal))

            max_durata = math.ceil(durata_sal)
            packAndShow(lista_durate, max_durata)
            # TODO: tener traccia degli id relativi alle durate e inserire pazienti nelle 3 salette

            # TODO: vincoli per test di ogni paziente

        elif main_menu == 2:
            listp = []
            with open('helpers/pazienti.txt', 'r') as file_p:
                for line in file_p:
                    # output(out_lck,line)
                    pz = Paziente(line)
                    # output(out_lck, "Paziente: " + str(pz.id) + "  Test: " + pz.test_array)
                    listp.append(pz)

                # inserimento random nelle sale
                sala1, sala2, sala3 = inserimento_random(listp)

                output(out_lck, "Saletta 1: " + str(sala1))
                output(out_lck, "Saletta 2: " + str(sala2))
                output(out_lck, "Saletta 3: " + str(sala3))

                # TODO: vincoli per test di ogni paziente
