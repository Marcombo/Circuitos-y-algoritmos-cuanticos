import cirq
CY = cirq.Y.controlled()
c, t = cirq.LineQubit.range(2)
puerta = cirq.Circuit(CY(c, t))
print(puerta)
