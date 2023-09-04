import numpy as np
import cirq
n = 3
m = 4
truth_table = [[1,1,0,1],
               [0,1,1,1],
               [1,0,1,1],
               [0,1,1,0],
               [1,1,1,1],
               [0,1,1,1],
               [0,1,1,1],
               [1,0,1,1]]
def ToBin(a,p):
    int_a = a
    bin_a = []
    for i in range(p):
        r = int_a%2
        bin_a = [r] + bin_a
        int_a = int(int_a/2)
    return bin_a
def Uf(n,m):
    N = 2**(n+m)
    matrix = np.zeros((N,N))
    for i in range(N):
        for j in range(N):
            bin_i = ToBin(i,n+m)
            bin_j = ToBin(j,n+m)
            matrix[i][j] = 1
            if (bin_j[:n] != bin_i[:n]):
                matrix[i][j] = 0
            for k in range(m):
                if bin_j[n+k] != (bin_i[n+k] + F(bin_i[:n],k))%2:
                    matrix[i][j] = 0
    return matrix
def F(x,y):
    acc = 0
    for i in range(n):
        acc = acc + x[i]*(2**(n-i-1))
    return truth_table[acc][y]
URAM = cirq.MatrixGate(Uf(n,m))
###############QDAC#############
p = 5
def thetas(m,p):
    lista = [1]
    for i in range(2**m):
        x = round((2**(p-2))*2*np.arcsin(i/2**m))
        lista = lista + [x]
    return lista
A = thetas(m,p)
def truth_table(m,p):
    M = np.zeros((2**m,p))
    for i in range(2**m):
        x = thetas(m,p)[i]
        y = ToBin(x,p)
        M[i] = y
    return M
truth_table = truth_table(m,p)
def Uf2(m,p):
    N = 2**(m+p)
    matrix = np.zeros((N,N))
    for i in range(N):
        for j in range(N):
            bin_i = ToBin(i,m+p)
            bin_j = ToBin(j,m+p)
            matrix[i][j] = 1
            if (bin_j[:m] != bin_i[:m]):
                matrix[i][j] = 0
            for k in range(p):
                if bin_j[m+k] != (bin_i[m+k] + F2(bin_i[:m],k))%2:
                    matrix[i][j] = 0
    return matrix
def F2(x,y):
    acc = 0
    for i in range(m):
        acc = acc + x[i]*(2**(m-i-1))
    return truth_table[acc][y]
UDAC = cirq.MatrixGate(Uf2(m,p))
CRY1 = cirq.ry(2).controlled()
CRY2 = cirq.ry(1).controlled()
CRY3 = cirq.ry(1/2).controlled()
CRY4 = cirq.ry(1/4).controlled()
CRY5 = cirq.ry(1/8).controlled()
aux,a0,a1,a2,d0,d1,d2,d3,fi0,fi1,fi2,fi3,fi4 = cirq.LineQubit.range(13)
QRAMDAC = cirq.Circuit()
QRAMDAC.append([cirq.H(a0),cirq.H(a1),cirq.H(a2)])
QRAMDAC.append([URAM(a0,a1,a2,d0,d1,d2,d3), UDAC(d0,d1,d2,d3,fi0,fi1,fi2,fi3,fi4)])
QRAMDAC.append([CRY1(fi0,aux),CRY2(fi1,aux),CRY3(fi2,aux),CRY4(fi3,aux),CRY5(fi4,aux)])
QRAMDAC.append([UDAC(d0,d1,d2,d3,fi0,fi1,fi2,fi3,fi4),URAM(a0,a1,a2,d0,d1,d2,d3)])
QRAMDAC.append(cirq.measure(aux,d0,d1,d2,d3,fi0,fi1,fi2,fi3,fi4))
un_simulador = cirq.Simulator()
estado_final = un_simulador.simulate(QRAMDAC)
print(estado_final)

