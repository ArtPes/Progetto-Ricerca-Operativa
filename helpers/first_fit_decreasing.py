""" Partition a list into sublists whose sums don't exceed a maximum
    using a First Fit Decreasing algorithm. See
    http://www.ams.org/new-in-math/cover/bins1.html
    for a simple description of the method.
"""
import math

from helpers.struct_p import Paziente


class Bin(object):
    """ Container for items that keeps a running sum """

    def __init__(self):
        self.items = []
        self.sum = 0

    def append(self, item):
        self.items.append(item)
        self.sum += item

    def __str__(self):
        """ Printable representation """
        return ('Bin(sum=%d, items=%s)' % (self.sum, str(self.items)))


def pack(listp, maxValue):
    values = []
    for i in range(0, len(listp)):
        values.append(Paziente.somma_durata_singolo(listp[i]))

    values = sorted(values, reverse=True)

    bins = []

    for item in values:
        # Try to fit item into a bin
        for bin in bins:
            if bin.sum + item <= maxValue:
                # print 'Adding', item, 'to', bin
                bin.append(item)
                break
        else:
            # item didn't fit into any bin, start a new bin
            bin = Bin()
            bin.append(item)
            bins.append(bin)


    return bins


def packAndShow(listp):
    lista_durate = []

    for i in range(0, len(listp)):
        durata = Paziente.somma_durata_singolo(listp[i])
        # print("Durata tot: " + str(durata))
        lista_durate.append(durata)

    durata_tot = sum(lista_durate)

    # calcolo la durata media per saletta
    durata_sal = durata_tot / 3

    max_durata = math.ceil(durata_sal)

    bins = pack(listp, max_durata)
    d = max_durata
    if len(bins)>3:
        while len(bins)>3:
            bins = pack(listp, d)
            d = d+1

    k = 1

    for bin in bins:
        # print(bin.items)
        for i in range(0, len(bin.items)):
            for j in range(0, len(listp)):
                durata = Paziente.somma_durata_singolo(listp[j])
                if bin.items[i] == durata:
                    listp[j].saletta = k

        k += 1


