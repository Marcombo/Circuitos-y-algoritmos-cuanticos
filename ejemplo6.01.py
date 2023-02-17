##########################Sec.6.1.1###########################3
import numpy as np
def ToBin(a):
    int_a = a
    bin_a = []
    for i in range(n+1):
        r = int_a%2
        bin_a = [r] + bin_a
        int_a = int(int_a/2)
    return bin_a
def Uf(n):
    N = 2**(n+1)
    matrix = np.zeros((N,N))
    for i in range(N):
        for j in range(N):
            bin_i = ToBin(i)
            bin_j = ToBin(j)
            if (bin_j[:n] == bin_i[:n]) and (bin_j[n] == (bin_i[n] + F(bin_i[:n]))%2):
                matrix[i][j] = 1.
    return matrix
n = 2
truth_table = [1,0,1,1]
def F(x):
    return truth_table[2*x[0] + x[1]]
print(Uf(n))
