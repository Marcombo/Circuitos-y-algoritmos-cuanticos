#######CLASE QFA##########
import cirq
class QFA(cirq.Gate):
    def __init__(self):
        super(QFA, self)
    def _num_qubits_(self):
        return 4
    def _decompose_(self, qubits):
        I, A, B, O = qubits
        yield cirq.CCX(A, B, O)
        yield cirq.CX(A, B)
        yield cirq.CCX(I, B, O)
        yield cirq.CX(I, B)
    def _circuit_diagram_info_(self, args):
        return ["QFA"] * self.num_qubits()
qfa = QFA()
########OPERANDOS##########
n = 4
c = 1
x = [0,1,0,1]
y = [1,0,1,1]
#########CIRCUITOS#########
reg = cirq.LineQubit.range(3*n+1)
circuito = cirq.Circuit()
if c == 1:
    circuito.append(cirq.X(reg[0]))
for i in range(n):
    if x[i] == 1:
        circuito.append(cirq.X(reg[3*i+1]))
    if y[i] == 1:
        circuito.append(cirq.X(reg[3*i+2])) 
    circuito.append(qfa(reg[3*i],reg[3*i+1],reg[3*i+2],reg[3*i+3]))
###########RESULTADO########
circuito.append(cirq.measure(reg[2],reg[5],reg[8],reg[11],reg[12],key = 'suma'))
print(circuito)
simulador = cirq.Simulator()
resultado = simulador.run(circuito, repetitions=1)
print(resultado)
