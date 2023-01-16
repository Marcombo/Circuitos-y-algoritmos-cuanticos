import cirq
CH = cirq.H.controlled()
CCH = CH.controlled()
c, d, t = cirq.LineQubit.range(3)
U = cirq.unitary(cirq.Circuit(CCH(c, d, t)))
print(U)
