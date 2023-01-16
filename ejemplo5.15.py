import cirq
import numpy
J = cirq.MatrixGate(numpy.array([
    [1.0,  1.0],
    [-1.0, 1.0]
    ]) / numpy.sqrt(2)
)
q = cirq.NamedQubit('x')
puerta = cirq.Circuit(J(q))
print(puerta)
