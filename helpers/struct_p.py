# strutture Paziente Saletta Opertore Test


class Paziente:
    id = 0
    durata_tot = 0
    test_array = ''
    saletta = None

    def __init__(self, line):
        self.id = int(line.split(None, 1)[0])
        test = line.split(None, 1)[1]
        self.test_array = self.set_test(test)

    def somma_durata_singolo(paziente):
        # durate di ogni singolo test
        durate = [1, 2, 4, 6, 8]
        tot = 0
        test = paziente.test_array
        for t in test:
            n = t-1
            tot = tot + durate[n]

        return tot

    # data la stringa di test "10101" la trasforma in un array che contiene
    #  i numeri dei test da effetturare es. 01010 = [2,4]
    def set_test(self,listp):
        test = list(listp)
        a = 1
        lista_test = []

        for i in range(0, 5):
            t = int(test[i])
            n = t * a
            lista_test.append(n)
            a += 1

        lista_test = [x for x in lista_test if x != 0]

        return lista_test

# -------------------------------------------------------------------------------------
class Nodo:
    idN = 0
    idP = 0
    visita = 0
    sala = 0

    def __init__(self, idNo, idPaz, test ,sal):
        self.idN = idNo
        self.idP = idPaz
        self.visita = test - 1
        self.sala= sal


# -------------------------------------------------------------------------------------

class Arco:
    visita = 0
    primo_estremo = 0
    secondo_estremo = 0

    def __init__(self, visita, primo_estremo, secondo_estremo):
        self.visita = visita + 1
        self.primo_estremo = primo_estremo
        self.secondo_estremo = secondo_estremo


# ---------------------------------------------------------------------------------------

class Mossa:
    tipo = ''
    macchina = 0
    primo_indice_primo_arco = 0
    secondo_indice_primo_arco = 0
    primo_indice_secondo_arco = 0
    secondo_indice_secondo_arco = 0

    def __init__(self, tipo, m, pipa, sipa, pisa, sisa):
        self.tipo = tipo
        self.macchina = m
        self.primo_indice_primo_arco = pipa
        self.secondo_indice_primo_arco = sipa
        self.primo_indice_secondo_arco = pisa
        self.secondo_indice_secondo_arco = sisa


# -----------------------------------------------------------------------------------------

class Solution:
    def __init__(self, grafo, makespan, Mossa, lista_makespan, lista_tot):
        self.grafo = grafo
        self.makespan = makespan
        self.Mossa = Mossa
        self.lista_makespan = lista_makespan
        self.lista_tot = lista_tot


# ------------------------------------------------------------------------------------------

class Task:
    def __init__(self,paziente,sala,test,start):
        self.paziente = paziente
        self.sala = sala
        self.test = test
        self.start = start
        self.end= start + self.calcola_durata(test)
        self.durata = self.calcola_durata(test)

    def calcola_durata(self,test):
        durate = [1,2,4,6,8]

        for i in range(0,len(durate)):
            if i == test-1:
                return durate[i]

