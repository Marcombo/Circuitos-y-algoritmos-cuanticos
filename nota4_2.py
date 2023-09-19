import cirq
class CY(cirq.Gate):
    def __init__(self):
        super(CY, self)
    def _num_qubits_(self):
        return 3
    def _decompose_(self, qubits):
        I, A, B = qubits
        yield cirq.CX(B, A)
        yield cirq.CX(B, I)
        yield cirq.CCX(I, A, B)
    def _circuit_diagram_info_(self, args):
        return ["CY"] * self.num_qubits()
cy = CY()
class XOR(cirq.Gate):
    def __init__(self):
        super(XOR, self)
    def _num_qubits_(self):
        return 3
    def _decompose_(self, qubits):
        I, A, B = qubits
        yield cirq.CCX(I, A, B)
        yield cirq.CX(B, I)
        yield cirq.CX(I, A)
    def _circuit_diagram_info_(self, args):
        return ["XOR"] * self.num_qubits()
xor = XOR()
########OPERANDOS##########
n = 5
c = 1
x = [0,1,0,0,1]
y = [1,0,0,1,1]
#########CIRCUITO#########
reg = cirq.LineQubit.range(2*n+2)
circuito = cirq.Circuit()
if c == 1:
    circuito.append(cirq.X(reg[0]))
for i in range(n):
    if x[i] == 1:
        circuito.append(cirq.X(reg[2*i+1]))
    if y[i] == 1:
        circuito.append(cirq.X(reg[2*i+2])) 
    circuito.append(cy(reg[2*i],reg[2*i+1],reg[2*i+2]))
circuito.append(cirq.CX(reg[2*n],reg[2*n+1]))
for i in range(n):
    circuito.append(xor(reg[2*(n-1-i)],reg[2*(n-1-i)+1],reg[2*(n-1-i)+2]))
###########MEDICIONES########
for i in range(n+1):
    circuito.append(cirq.measure(reg[2*i+1]))
print(circuito)
simulador = cirq.Simulator()
resultado = simulador.run(circuito, repetitions=1)
print(resultado)

