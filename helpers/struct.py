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
        for t in range(0, 5):
            n = int(test[t])
            tot = tot + n * durate[t]

        return tot


# -------------------------------------------------------------------------------------
class Nodo:
    idN = 0
    idP = 0
    visita = 0

    def __init__(self, idNo, idPaz, test):
        self.idN = idNo
        self.idP = idPaz
        self.visita = test - 1


# -------------------------------------------------------------------------------------
class Schedule:
    s_order = []
    durataTest = [1, 2, 4, 6, 8]
    listp = []

    def __init__(self, pz, sz):
        for p in pz:
            self.listp.append(p)
        for s in sz:
            self.s_order.append(s)

    def stampa_input(self):
        for p in self.listp:
            print('paziente' + str(p))
        for s in self.s_order:
            print('saletta' + str(s))


# -------------------------------------------------------------------------------------
# serve per il critical path
class Node:
    def __init__(self, initdata):
        self.data = initdata
        self.next = None

    def getData(self):
        return self.data

    def getNext(self):
        return self.next

    def setData(self, newdata):
        self.data = newdata

    def setNext(self, newnext):
        self.next = newnext


# -------------------------------------------------------------------------------------
class UnorderedList:
    def __init__(self):
        self.head = None

    def isEmpty(self):
        return self.head == None

    def add(self, item):
        temp = Node(item)
        temp.setNext(self.head)
        self.head = temp

    def size(self):
        current = self.head
        count = 0
        while current != None:
            count = count + 1
            current = current.getNext()

        return count

    def search(self, item):
        current = self.head
        found = False
        while current != None and not found:
            if current.getData() == item:
                found = True
            else:
                current = current.getNext()

        return found

    def remove(self, item):
        current = self.head
        previous = None
        found = False
        while not found:
            if current.getData() == item:
                found = True
            else:
                previous = current
                current = current.getNext()

        if previous == None:
            self.head = current.getNext()
        else:
            previous.setNext(current.getNext())

    def getFirst(self):
        item = self.head
        return item


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
    def __init__(self, grafo, makespan, Mossa):
        self.grafo = grafo
        self.makespan = makespan
        self.Mossa = Mossa
