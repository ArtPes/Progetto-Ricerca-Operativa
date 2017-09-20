from helpers.utils import *
import threading
from helpers.struct import *

if __name__ == "__main__":

    out_lck = threading.Lock()

    while True:
        # Main Menu
        main_menu = loop_menu(out_lck, "\nSelect one of the following actions ('e' to exit): ", ["Pazienti Ordinati su Durata test","Pazienti già inseriti"])

        if main_menu == 1:
            listp = []
            with open('helpers/pazienti.txt','r') as file_p:
                for line in file_p:
                    #output(out_lck,line)
                    pz=Paziente(line)
                    output(out_lck, "Paziente: " +str( pz.id) + "  Test: "+ pz.test_array)
                    listp.append(pz)

            lista_durate = []
            for i in range(0,len(listp)):
                durata = Paziente.somma_durata_singolo(listp[i])
                output(out_lck,"Durata tot: "+ str(durata))
                lista_durate.append(durata)

            durata_tot = sum(lista_durate)
            output(out_lck,"Durata totale test: "+ str(durata_tot))

            #calcolo la durata media per saletta
            durata_sal = durata_tot/3
            output(out_lck, "Durata media per saletta: " + str(durata_sal))



        elif main_menu == 2:
            listp = []
            with open('helpers/pazienti.txt','r') as file_p:
                for line in file_p:
                    #output(out_lck,line)
                    pz=Paziente(line)
                    output(out_lck, "Paziente: " +str( pz.id) + "  Test: "+ pz.test_array)
                    listp.append(pz)





