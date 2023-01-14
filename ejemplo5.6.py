import cirq
q = cirq.NamedQubit('a')
puerta = cirq.Circuit(cirq.X(q))
print(puerta)
