##########################Uf()###########################3
import numpy as np
def ToBin(a):
    int_a = a
    bin_a = []
    for i in range(n+1):
        r = int_a%2
        bin_a = [r] + bin_a
        int_a = int(int_a/2)
    return bin_a
def Uf():
    matrix = np.zeros((N,N))
    for i in range(N):
        for j in range(N):
            bin_i = ToBin(i)
            bin_j = ToBin(j)
            if (bin_j[:n] == bin_i[:n]) and (bin_j[n] == (bin_i[n] + F(bin_i[:n]))%2):
                matrix[i][j] = 1.
    return matrix
############################Deutsch##################################
import cirq
n = 1
N = 2**(n+1)
truth_table = [0, 1]
def F(x):
    return truth_table[x[0]]
UF = cirq.MatrixGate(Uf())
q0, q1 = cirq.LineQubit.range(2)
circuito = cirq.Circuit([cirq.H(q0), cirq.X(q1), cirq.H(q1),UF(q0, q1), cirq.H(q0)])
circuito.append(cirq.measure(q0))
print(circuito)
un_simulador = cirq.Simulator()
resultado = un_simulador.run(circuito, repetitions=20)
print(resultado)
