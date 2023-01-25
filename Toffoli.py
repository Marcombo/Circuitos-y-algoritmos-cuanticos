import cirq
import numpy as np
T_adj = cirq.T**-1
c,d,t = cirq.LineQubit.range(3)
Toffoli2 = cirq.Circuit()
Toffoli2.append([cirq.H(t),cirq.CX(d,t),T_adj(t), cirq.CX(c,t)])
Toffoli2.append([cirq.T(t),cirq.CX(d,t),T_adj(t), cirq.CX(c,t)])
Toffoli2.append([T_adj(d),cirq.T(t),cirq.CX(c,d),cirq.H(t),T_adj(d),cirq.CX(c,d)])
Toffoli2.append([cirq.T(c),cirq.S(d)])
U = cirq.unitary(cirq.Circuit(Toffoli2))
print(U)
