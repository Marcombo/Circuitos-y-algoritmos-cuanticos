#######CLASE QFA##########
import cirq
class QCC(cirq.Gate):
    def __init__(self):
        super(QCC, self)
    def _num_qubits_(self):
        return 4
    def _decompose_(self, qubits):
        I, A, B, O = qubits
        yield cirq.CCX(A, B, O)
        yield cirq.CX(A, B)
        yield cirq.CCX(I, B, O)
    def _circuit_diagram_info_(self, args):
        return ["QCC"] * self.num_qubits()
qcc = QCC()
class QCCAd(cirq.Gate):
    def __init__(self):
        super(QCCAd, self)
    def _num_qubits_(self):
        return 4
    def _decompose_(self, qubits):
        I, A, B, O = qubits
        yield cirq.CCX(I, B, O)
        yield cirq.CX(A, B)
        yield cirq.CCX(A, B, O)
    def _circuit_diagram_info_(self, args):
        return ["QCCAd"] * self.num_qubits()
qccAd = QCCAd()
class QS(cirq.Gate):
    def __init__(self):
        super(QS, self)
    def _num_qubits_(self):
        return 3
    def _decompose_(self, qubits):
        I, A, B = qubits
        yield cirq.CX(I, B)
        yield cirq.CX(A, B)
    def _circuit_diagram_info_(self, args):
        return ["QS"] * self.num_qubits()
qs = QS()
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
    circuito.append(qcc(reg[3*i],reg[3*i+1],reg[3*i+2],reg[3*i+3]))
circuito.append(cirq.CX(reg[3*(n-1)+1],reg[3*(n-1)+2]))
for i in range(n-1):
    circuito.append(qs(reg[3*(n-1-i)],reg[3*(n-1-i)+1],reg[3*(n-1-i)+2]))
    circuito.append(qccAd(reg[3*(n-2-i)],reg[3*(n-2-i)+1],reg[3*(n-2-i)+2],reg[3*(n-2-i)+3]))
circuito.append(qs(reg[0],reg[1],reg[2]))

###########RESULTADO########
for i in range(n-1):
    circuito.append(cirq.measure(reg[3*i+3]))
for i in range(n):
    circuito.append(cirq.measure(reg[3*i+2]))
circuito.append(cirq.measure(reg[3*n]))
print(circuito)
simulador = cirq.Simulator()
resultado = simulador.run(circuito, repetitions=1)
print(resultado)

