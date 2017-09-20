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

        test = paziente.test_array

        for t in test:
            n = int(t)
            if i<5:
                tot = tot + n * durate[i]
                i += 1
            else :
                break
        return tot



    #def somma_durate_all(self, lista_durate,durata_media):

