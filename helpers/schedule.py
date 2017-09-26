from helpers.utils import *
from helpers.struct import *
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

def list_to_array(list):
    return list

def list_to_mat(list):
    mat = []
    for i in range (0,len(list)):
        mat.append(list_to_array(list[i]))
    return mat
def set_the_mat(lists,listp):
        matrixs = []  #matrice per le salette
        matrixp = []  #matrice per i pazienti
        newlistp = []
        for i in range(0,len(lists)):
            matrixs.append(list_to_mat(lists[i]))


        for i in range(0, len(listp)):
            id = listp[i].id
            test = set_test(listp[i].test_array)
            sala = listp[i].saletta
            newlistp.append(test)

        for j in range (0,len (newlistp)):
            matrixp.append(list_to_mat(newlistp[j]))
        #print(matrixp)
        return (matrixp,matrixs)

def stampa_matrici(mat,typ1,typ2):
    for i in range(0,len(mat)):
        print(str(typ1) + str(i) )
        for j in range(0,len(mat[i])):
            print(str(typ2) +" " +str(j)+" " + str(mat[i][j]))
def stampa_matrici2(mat):
    for i in range(0,len(mat)):
        for j in range(0,len(mat[i])):
            print(str(i) + str(mat[i][j]))

def crea_nodo(mp):
    #creo nodo da lista pazienti (paz,visita)
    nodi =[]
    numn= 0
    ns=Nodo(0,0,0)
    nodi.append(ns)
    for i in range(0,len(mp)):
        for j in range(0,len(mp[i])):
            numn+=1
            nd = Nodo(numn,i+1,mp[i][j])
            nodi.append(nd)
    nd=Nodo(numn+1,0,0)
    nodi.append(nd)
    for i in range(0,len(nodi)):
        print("nodo  "+ str( i) +" :idp "+ str(nodi[i].idP) + " idN: "+str(nodi[i].idN) + " visita: "+str(nodi[i].visita) )

    return nodi,numn



def dur_t(test):
    durataTest = [1, 2, 4, 6, 8]
    i=0
    while i<4:
        if test== i:
            dt=durataTest[i]

    return dt

def stampa3(matr):
    for i in range(0, len(matr)):
        print(str(i)+str(matr[i]))


def create_mat(nodi):
    mat = []
    dim=len(nodi)
    mat = [[0 for i in range (0,dim)]for j in range (0,dim)]
    return mat
def create_mat_bool(nodi):
    mat = []
    mat = [[False for i in range(0,len(nodi))] for j in range(0,len(nodi))]
    return mat

#matp e' la matrice start
#nodi e' la lista dei nodi
#mats e' la lista delle salette che mi serve per capire chi inizia e finisce le op

def create_initial_sol(matp,nodi,mats):
    #1 per uscenti dal nodo, -1 per entranti
    st_op=[] #start operation
    last_op=[] #last operation
    #metto a 0 le celle con righe=colonne
    """for i in range(0,len(matp)):
        for j in range(0,len(matp[i])):
            if i == j:
                    matp[i][j]=0"""
    #cerco operazioni iniziali nodo 0
    for i in range (0,len(mats)):
        st_op.append(mats[i][0])
    print(st_op)
    for i in range(0,len(st_op)):
        for j in range (0,len(matp)):
            if nodi[j].idP == st_op[i]:
                matp[0][j]=1
                matp[j][0]=-1
    stampa3(matp)
    #stessa cosa per nodo finale
    for i in range(0,len(mats)):
        last_op.append(mats[i][len(mats[i])-1])
    print(last_op)
    for i in range(0,len(last_op)):
        for j in range (0,len(matp)):
            if nodi[j].idP == last_op[i]:
                matp[len(matp[j])-1][j]=-1
                matp[j][len(matp[j])-1]=1
    stampa3(matp)
    #inserisco i nodi successivi
    """ciclo i e j mi serve per prendere i pazienti da ogni saletta 
        in seguito ciclo con z su la lunghezza di nodi (indice di riga matrice)
        (in nodi ho la lista dei nodi con id nodo, id paziente e quale visita)
        se trovo che l idP(id paziente di Nodo) è lo stesso del paziente estratto dalla lista delle salette
        ciclo sulle colonne della nostra matrice mstart che viene passata come matp sempre di dimensione nodo
        quando trovo che l id del paziente e' presente in altri nodi all interno della lista [[per es P1= {n1=(1,2),n2={1,4)}]]
        vado a mettere 1 nella cella a cui deve seguire quel nodo (vedi 1 per uscenti)
        ---SE NON HAI CAPITO , CAZZI TUOI ;) 
        ora mi sa che bisogna fare la stessa cosa per la matrice booleana, bisogna stare attenti sul nodo terminatore a fare del casino
    """
    for i in range (0,len(mats)):
        for j in range(0,len(mats[i])):
            for z in range(1,len(nodi)-1):
                if nodi[z].idP==mats[i][j]:

                    for k in range(1,len(matp[z])-1):
                        print ("primo if, nodiz vale: " +str(nodi[z].idN) + " i vale "+ str (i) +" j vale " +str(j)+ " k vale : "+str(k)  )
                        if nodi[z].idP == nodi[k].idP :
                            matp[z][k]=1
                            matp[k][z]=1
                            if z == k:
                                matp[z][k] = 0
    stampa3(matp)

def process(lists,listp):

    ms= []
    mp= []
    mp,ms = set_the_mat(lists,listp)
    durataTest = [1, 2, 4, 6, 8]
    #stampa_matrici(mp,"paziente","visita")
    stampa_matrici(ms,"saletta","paziente")

    nodi = []
    nodi,numn =crea_nodo(mp)
    mstart=create_mat(nodi)
    stampa3(mstart)
    mstartbool=create_mat_bool(nodi)
    stampa3(mstartbool)
    create_initial_sol(mstart,nodi,ms)

