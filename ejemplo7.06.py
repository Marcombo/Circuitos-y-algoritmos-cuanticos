import cirq
import numpy as np
n = 3
N = 2**n
r = N**0.5
a = np.exp(2*np.pi*1j*0.625)
U = cirq.MatrixGate(np.array([
    [a, 0, 0, 0],
    [0, 0, 1, 0],
    [0, 1, 0, 0],
    [0, 0, 0, a],
    ]) 
)
CU = U.controlled()
def QFT_inv():
    matrix = []
    for j in range(N):
        row = []
        for k in range(N):
            jk = (j*k) % N
            row = row + [np.exp((-2*np.pi*1j*jk)/N)/r]
        matrix = matrix + [row]
    return matrix
A = np.array(QFT_inv())
qft_inv = cirq.MatrixGate(A)
q1,q2,q3,q4,q5 = cirq.LineQubit.range(5)
fase_estim = cirq.Circuit([cirq.H(q1), cirq.H(q2), cirq.H(q3)])
fase_estim.append([cirq.H(q4)])
fase_estim.append([cirq.H(q5)])
fase_estim.append(CU(q3,q4,q5))
fase_estim.append([CU(q2,q4,q5), CU(q2,q4,q5)])
fase_estim.append([CU(q1,q4,q5), CU(q1,q4,q5),CU(q1,q4,q5),CU(q1,q4,q5)])
fase_estim.append(qft_inv(q1,q2,q3))
un_simulador = cirq.Simulator()
estado_final = un_simulador.simulate(fase_estim)
print(estado_final)
