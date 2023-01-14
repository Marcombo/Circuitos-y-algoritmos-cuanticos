import cirq
c, t = cirq.LineQubit.range(2)
puerta = cirq.Circuit(cirq.CX(c, t)**0.125)
print(puerta)
