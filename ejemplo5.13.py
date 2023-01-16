import cirq
c, d, t = cirq.LineQubit.range(3)
puerta = cirq.Circuit(cirq.CCX(c, d,t))
print(puerta)

