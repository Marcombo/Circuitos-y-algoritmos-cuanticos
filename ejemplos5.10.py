import cirq
c, t = cirq.LineQubit.range(2)
puerta = cirq.Circuit(cirq.CZ(c, t))
print(puerta)

import cirq
t, u = cirq.LineQubit.range(2)
puerta = cirq.Circuit(cirq.SWAP(t, u))
print(puerta)
