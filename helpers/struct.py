from helpers.utils import  *
# strutture Paziente Saletta Opertore Test

class Paziente:

    id = 0
    durata_tot = 0
    test_array = ''

    def __init__(self, line ):

        self.id = int(line.split(None,1)[0])
        test = line.split(None,1)[1]
        self.test_array=test




    def somma_durata_singolo(self,Paziente):

        #durate di ogni singolo test
        durate = [1,2,3,4,5]
        tot = 0

        test = Paziente.test_array.split()

        for t in test:
            for i in range(0,4):
                n = int(t)
                tot = tot + n*durate[i]
                i += 1

        print("Tot durate singolo paziente: ",tot)

    def somma_durate_all(self,Durate):

        for i in range(0,len(Durate)):
                tot = tot + Durate[i]
                i += 1

        print("Totae durate all pazienti: ",tot)


