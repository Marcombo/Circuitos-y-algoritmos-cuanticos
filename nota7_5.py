import cirq
import numpy as np
q1,q0 = cirq.LineQubit.range(2)
CRpi_2 = cirq.S.controlled()
U = cirq.Circuit()
U.append([cirq.H(q1), CRpi_2(q0,q1), cirq.H(q0)])
U.append(cirq.SWAP(q0,q1))
print(cirq.unitary(U))

