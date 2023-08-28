##########################Sec.6.1.1###########################3
import numpy as np
n = 2
m = 2
truth_table = [[1,0],
               [1,1],
               [0,0],
               [0,1]]
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
import cirq
U = cirq.MatrixGate(Uf(n,m))
x0,x1,y0,y1 = cirq.LineQubit.range(4)
F = cirq.Circuit()
F.append([U(x0,x1,y0,y1)])
print(F)
