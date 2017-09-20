from helpers.utils import *
import threading
from helpers.struct import *

if __name__ == "__main__":

    out_lck = threading.Lock()

    while True:
        # Main Menu
        main_menu = loop_menu(out_lck, "Select one of the following actions ('e' to exit): ", ["Pazienti già inseriti","Pazienti Ordinati su Durata test"])

        if main_menu == 1:
            output(out_lck,"1")
            listp = []
            with open('helpers/pazienti.txt','r') as file_p:
                for line in file_p:
                    output(out_lck,line)
                    pz=Paziente(line)
                    output(out_lck, "Paziente :" +str( pz.id) )
                    listp.append(pz)




        elif main_menu == 2:
            output(out_lck,"2")





