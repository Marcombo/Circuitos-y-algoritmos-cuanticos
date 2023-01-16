import cirq
CH = cirq.H.controlled()
CCH = CH.controlled()
c, d, t = cirq.LineQubit.range(3)
puerta = cirq.Circuit(CCH(c, d,t))
print(puerta)
