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
#########Adder##########
class ADDER5(cirq.Gate):
    def __init__(self):
        super(ADDER5, self)
    def _num_qubits_(self):
        return 11
    def _decompose_(self, qubits):
        C0,A0,A1,A2,A3,A4,B0,B1,B2,B3,B4 = qubits
        yield cy(C0,A0,B0)
        yield cy(B0,A1,B1)
        yield cy(B1,A2,B2)
        yield cy(B2,A3,B3)
        yield cy(B3,A4,B4)
        yield xor(B3,A4,B4)
        yield xor(B2,A3,B3)
        yield xor(B1,A2,B2)
        yield xor(B0,A1,B1)
        yield xor(C0,A0,B0)
    def _circuit_diagram_info_(self, args):
        return ["ADDER5"] * self.num_qubits()
Adder5 = ADDER5()
########################
class ADDER4(cirq.Gate):
    def __init__(self):
        super(ADDER4, self)
    def _num_qubits_(self):
        return 9
    def _decompose_(self, qubits):
        C0,A0,A1,A2,A3,B0,B1,B2,B3 = qubits
        yield cy(C0,A0,B0)
        yield cy(B0,A1,B1)
        yield cy(B1,A2,B2)
        yield cy(B2,A3,B3)
        yield xor(B2,A3,B3)
        yield xor(B1,A2,B2)
        yield xor(B0,A1,B1)
        yield xor(C0,A0,B0)
    def _circuit_diagram_info_(self, args):
        return ["ADDER4"] * self.num_qubits()
Adder4 = ADDER4()
#########AddSub#########
class ADDSUB(cirq.Gate):
    def __init__(self):
        super(ADDSUB, self)
    def _num_qubits_(self):
        return 12
    def _decompose_(self, qubits):
        C0,A0,A1,A2,A3,A4,B0,B1,B2,B3,B4,AS = qubits
        yield [cirq.CX(AS,A0),cirq.CX(AS,A1),cirq.CX(AS,A2),cirq.CX(AS,A3),cirq.CX(AS,A4)]
        yield Adder5(C0,A0,A1,A2,A3,A4,B0,B1,B2,B3,B4)
        yield [cirq.CX(AS,A0),cirq.CX(AS,A1),cirq.CX(AS,A2),cirq.CX(AS,A3),cirq.CX(AS,A4)]
    def _circuit_diagram_info_(self, args):
        return ["ADDSUB"] * self.num_qubits()
AddSub = ADDSUB()
ContAdder = Adder4.controlled()
########OPERANDOS##########
x = [1,0,1,1]
y = [1,0,1,0]
########CIRCUITO##########
reg = cirq.LineQubit.range(15)
DIV = cirq.Circuit()
for i in range(4):
    if x[i] == 1:
        DIV.append(cirq.X(reg[i]))
    if y[i] == 1:
        DIV.append(cirq.X(reg[i+9]))
DIV.append(cirq.X(reg[8]))
DIV.append(AddSub(reg[14],reg[3],reg[4],reg[5],reg[6],reg[7],reg[9],reg[10],reg[11],reg[12],reg[13],reg[8]))
DIV.append(cirq.X(reg[7]))
DIV.append(AddSub(reg[14],reg[2],reg[3],reg[4],reg[5],reg[6],reg[9],reg[10],reg[11],reg[12],reg[13],reg[7]))
DIV.append(cirq.X(reg[6]))
DIV.append(AddSub(reg[14],reg[1],reg[2],reg[3],reg[4],reg[5],reg[9],reg[10],reg[11],reg[12],reg[13],reg[6]))
DIV.append(cirq.X(reg[5]))
DIV.append(AddSub(reg[14],reg[0],reg[1],reg[2],reg[3],reg[4],reg[9],reg[10],reg[11],reg[12],reg[13],reg[5]))
DIV.append(cirq.CX(reg[4],reg[8]))
DIV.append(ContAdder(reg[4],reg[14],reg[0],reg[1],reg[2],reg[3],reg[9],reg[10],reg[11],reg[12]))
DIV.append(cirq.CX(reg[8],reg[4]))
DIV.append(cirq.measure(reg[3],reg[2],reg[1],reg[0]))
DIV.append(cirq.measure(reg[7],reg[6],reg[5],reg[8]))
#########SIMULACIÓN##########
simulador = cirq.Simulator()
resultado = simulador.run(DIV, repetitions=1)
print(DIV)
print(resultado)
