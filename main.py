
import threading
from helpers.struct import *

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
                    pz = Paziente(line)
                    listp.append(pz)

            # inserimento nelle sale
            packAndShow(listp)

            sala1, sala2, sala3 = inserimento_sala(listp)

            output(out_lck, "Saletta 1: " + str(sala1))
            output(out_lck, "Saletta 2: " + str(sala2))
            output(out_lck, "Saletta 3: " + str(sala3))
            # show info dei pazienti
            stampa_info_paziente(listp)

            # TODO: vincoli per test di ogni paziente

        elif main_menu == 2:
            listp = []
            with open('helpers/pazienti.txt', 'r') as file_p:
                for line in file_p:
                    pz = Paziente(line)
                    listp.append(pz)

            # inserimento random nelle sale
            sala1, sala2, sala3 = inserimento_random(listp)

            output(out_lck, "Saletta 1: " + str(sala1))
            output(out_lck, "Saletta 2: " + str(sala2))
            output(out_lck, "Saletta 3: " + str(sala3))

            # show info dei pazienti
            stampa_info_paziente(listp)
            # TODO: vincoli per test di ogni paziente


