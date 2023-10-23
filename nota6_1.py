import cirq
###OPERANDOS: a = [a3, a2, a1, a0], z = [z3, z2, z1, z0], x = [x3, x2, x1, x0], OPERACIÓN = a·z + x mod 16
a = [1,1,0,0]
z = [0,1,1,1]
x = [1,0,0,1]
###COMPONENTES
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
class ADDER(cirq.Gate):
    def __init__(self):
        super(ADDER, self)
    def _num_qubits_(self):
        return 9
    def _decompose_(self, qubits):
        c0,x0,y0,x1,y1,x2,y2,x3,y3 = qubits
        yield cy(c0,x0,y0)
        yield cy(y0,x1,y1)
        yield cy(y1,x2,y2)
        yield cy(y2,x3,y3)
        yield xor(y2,x3,y3)
        yield xor(y1,x2,y2)
        yield xor(y0,x1,y1)
        yield xor(c0,x0,y0)
    def _circuit_diagram_info_(self, args):
        return ["ADDER"] * self.num_qubits()
adder = ADDER()
###CIRCUITO
a0,a1,a2,a3,z0,z1,z2,z3,c0,x0,y0,x1,y1,x2,y2,x3,y3 = cirq.LineQubit.range(17)
circuito = cirq.Circuit()
if a[0] == 1:
    circuito.append(cirq.X(a3))
if a[1] == 1:
    circuito.append(cirq.X(a2))
if a[2] == 1:
    circuito.append(cirq.X(a1))
if a[3] == 1:
    circuito.append(cirq.X(a0))
if x[0] == 1:
    circuito.append(cirq.X(x3))
if x[1] == 1:
    circuito.append(cirq.X(x2))
if x[2] == 1:
    circuito.append(cirq.X(x1))
if x[3] == 1:
    circuito.append(cirq.X(x0))
if z[0] == 1:
    circuito.append(cirq.X(z3))
if z[1] == 1:
    circuito.append(cirq.X(z2))
if z[2] == 1:
    circuito.append(cirq.X(z1))
if z[3] == 1:
    circuito.append(cirq.X(z0))
#etapa_0
circuito.append([cirq.CCX(a0,z0,y0), cirq.CCX(a0,z1,y1), cirq.CCX(a0,z2,y2), cirq.CCX(a0,z3,y3)])
circuito.append(adder(c0,x0,y0,x1,y1,x2,y2,x3,y3))
circuito.append([cirq.CCX(a0,z0,y0), cirq.CCX(a0,z1,y1), cirq.CCX(a0,z2,y2), cirq.CCX(a0,z3,y3)])
#etapa_1
circuito.append([cirq.CCX(a1,z0,y1), cirq.CCX(a1,z1,y2), cirq.CCX(a1,z2,y3)])
circuito.append(adder(c0,x0,y0,x1,y1,x2,y2,x3,y3))
circuito.append([cirq.CCX(a1,z0,y1), cirq.CCX(a1,z1,y2), cirq.CCX(a1,z2,y3)])
#etapa_2
circuito.append([cirq.CCX(a2,z0,y2), cirq.CCX(a2,z1,y3)])
circuito.append(adder(c0,x0,y0,x1,y1,x2,y2,x3,y3))
circuito.append([cirq.CCX(a2,z0,y2), cirq.CCX(a2,z1,y3)])
#etapa_3
circuito.append([cirq.CCX(a3,z0,y3)])
circuito.append(adder(c0,x0,y0,x1,y1,x2,y2,x3,y3))
circuito.append([cirq.CCX(a3,z0,y3)])
###MEDICIÓN
circuito.append(cirq.measure(x3,x2,x1,x0))
#print(circuito)
simulador = cirq.Simulator()
resultado = simulador.run(circuito, repetitions=1)
print(resultado)
