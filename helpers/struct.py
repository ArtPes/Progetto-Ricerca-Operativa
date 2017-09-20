from helpers.utils import *


# strutture Paziente Saletta Opertore Test

class Paziente:
    id = 0
    durata_tot = 0
    test_array = ''
    saletta = None

    def __init__(self, line):

        self.id = int(line.split(None, 1)[0])
        test = line.split(None, 1)[1]
        self.test_array = test

    def somma_durata_singolo(paziente):

        # durate di ogni singolo test
        durate = [1, 2, 4, 6, 8]
        tot = 0
        i = 0

        #test = paziente.test_array
        test = list(paziente.test_array)
        #print(test)

        for t in range(0,5):
            n = int(test[t])
            tot = tot + n * durate[t]

        return tot



    #def somma_durate_all(self, lista_durate,durata_media):

