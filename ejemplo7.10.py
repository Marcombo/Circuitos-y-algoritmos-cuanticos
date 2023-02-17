import numpy as np
def ToBin(a):
    int_a = a
    bin_a = []
    for i in range(n+1):
        r = int_a%2
        bin_a = [r] + bin_a
        int_a = int(int_a/2)
    return bin_a
############################Grove##################################
import cirq
import numpy as np
n = 4
N = 2**n
P = 2**(n+1)
#truth_table = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0]
#R = 3
truth_table = [0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0]
R = 1
def F(x):
    acc = 0
    for i in range(n):
        acc = acc + x[i]*(2**(n-i-1))
    return truth_table[acc]
def Uf():
    matrix = np.zeros((P,P))
    for i in range(P):
        for j in range(P):
            bin_i = ToBin(i)
            bin_j = ToBin(j)
            if (bin_j[:n] == bin_i[:n]) and (bin_j[n] == (bin_i[n] + F(bin_i[:n]))%2):
                matrix[i][j] = 1.
    return matrix    
uf = cirq.MatrixGate(np.array(Uf()))
def MA():
    matrix = np.zeros((N,N),dtype=complex)
    for k in range(N):
        if k == 0:
            matrix[k][k] = 1.0
        else:
            matrix[k][k] = -1.0
    return matrix
ma = cirq.MatrixGate(np.array(MA()))
CCCX = cirq.CCX.controlled()
CX = cirq.X.controlled()
CCX = CX.controlled()
CCCX = CCX.controlled()
class MA(cirq.Gate):
    def __init__(self):
        super(MA, self)
    def _num_qubits_(self):
        return 4
    def _decompose_(self, qubits):
        q0, q1, q2, q3 = qubits
        yield cirq.X(q0)
        yield cirq.X(q1)
        yield cirq.X(q2)
        yield cirq.X(q3)
        yield cirq.H(q3)
        yield CCCX(q0, q1, q2, q3)
        yield cirq.H(q3)
        yield cirq.X(q0)
        yield cirq.X(q1)
        yield cirq.X(q2)
        yield cirq.X(q3)
    def _circuit_diagram_info_(self, args):
        return ["A"] * self.num_qubits()
ma = MA()
class GC(cirq.Gate):
    def __init__(self):
        super(GC, self)
    def _num_qubits_(self):
        return 5
    def _decompose_(self, qubits):
        q0, q1, q2, q3, q4 = qubits
        yield uf(q0, q1, q2, q3, q4)
        yield cirq.H(q0)
        yield cirq.H(q1)
        yield cirq.H(q2)
        yield cirq.H(q3)
        yield ma(q0, q1, q2, q3)
        yield cirq.H(q0)
        yield cirq.H(q1)
        yield cirq.H(q2)
        yield cirq.H(q3)
    def _circuit_diagram_info_(self, args):
        return ["G"] * self.num_qubits()
G = GC()
reg = cirq.LineQubit.range(5)
circuito = cirq.Circuit()
circuito.append([cirq.H(reg[0]),cirq.H(reg[1]),cirq.H(reg[2]),cirq.H(reg[3])])
circuito.append([cirq.X(reg[4]),cirq.H(reg[4])])                                                      
for i in range(R):
    circuito.append(G(*reg))
circuito.append(cirq.measure(reg[0],reg[1],reg[2],reg[3],key='result'))                      
print(circuito)
simulador = cirq.Simulator()
#estado_final = simulador.simulate(circuito)
#print(estado_final)
resultado = simulador.run(circuito, repetitions=100)
print(resultado.histogram(key='result'))
