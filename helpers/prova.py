from operator import index


class Operatore:
    occupato = 0
    start = 0
    durata = 0

    def __init__(self, o, s, d):
        self.occupato = o
        self.start = s
        self.durata = d


# da mettere a posto perche funziona solo con 3 vettori da due elementi
def start(paz1, paz2, paz3):
    for i in range(0, len(paz1)):
        if paz1[i] == paz2[i] or paz1[i] == paz3[i]:
            a = paz1.index(paz1[i])
            b = paz1.index(paz1[i + 1])
            paz1[b], paz1[a] = paz1[a], paz1[b]

        elif paz2[i] == paz3[i]:
            a = paz2.index(paz2[i])
            b = paz2.index(paz2[i + 1])
            paz2[b], paz2[a] = paz2[a], paz2[b]

    return paz1, paz2, paz3


def machine(paz1, paz2, paz3, operator):
    for i in paz1:
        for j in paz2:
            for k in paz3:
                t1 = i - 1
                t2 = j - 1
                t3 = k - 1
                if operator[t1].occupato == 0:
                    # operatore libero lo uso
                    operator[t1].occupato = 1
                else:
                    continue
                if operator[t2].occupato == 0:
                    # operatore libero lo uso
                    operator[t2].occupato = 1
                else:
                    continue
                if operator[t3].occupato == 0:
                    # operatore libero lo uso
                    operator[t3].occupato = 1
                else:
                    continue

    for i in range(0, 5):
        print(operator[i].occupato)


if __name__ == '__main__':

    paz1 = [2, 4]
    paz2 = [1, 3]
    paz3 = [1, 2]

    paz1, paz2, paz3 = start(paz1, paz2, paz3)

    print(paz1)
    print(paz2)
    print(paz3)

    listO = []
    k = 1
    for i in range(0, 5):
        o = Operatore(0, 0, k)
        listO.append(o)
        k += 1

    machine(paz1, paz2, paz3, listO)
