import cirq
q = cirq.NamedQubit('a')
puerta = cirq.Circuit(cirq.H(q)**0.125)
print(puerta)
