
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

        test = list(paziente.test_array)

        for t in range(0,5):
            n = int(test[t])
            tot = tot + n * durate[t]

        return tot

class Nodo:

    idN =0
    idP= 0
    visita = 0

    def __init__(self,idNo,idPaz,test):
        self.idN=idNo
        self.idP=idPaz
        self.visita=test





