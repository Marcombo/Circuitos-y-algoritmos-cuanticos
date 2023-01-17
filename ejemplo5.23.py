import cirq
class Bell(cirq.Gate):
    def __init__(self):
        super(Bell, self)
    def _num_qubits_(self):
        return 2
    def _decompose_(self, qubits):
        q0, q1 = qubits
        yield cirq.H(q0)
        yield cirq.CX(q0,q1)
    def _circuit_diagram_info_(self, args):
        return ["Bell"] * self.num_qubits()
bell = Bell()
x, y, z, w = cirq.LineQubit.range(4)
dos_estados = cirq.Circuit(bell(x,y), cirq.X(z), cirq.X(w), bell(z,w))
dos_estados.append(cirq.measure(x, y, z, w, key = 'mediciones'))
un_simulador = cirq.Simulator()
resultado = un_simulador.run(dos_estados, repetitions=10000)
print(resultado.histogram(key='mediciones'))



