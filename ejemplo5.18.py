import cirq
import numpy
V = cirq.Z**0.5
Vadj = cirq.Z**-0.5
CV = V.controlled()
CVadj = Vadj.controlled()
c, d, t = cirq.LineQubit.range(3)
puerta = cirq.Circuit()
puerta.append(CV(d,t))
puerta.append([cirq.CX(c,d), CVadj(d,t), cirq.CX(c,d)])
puerta.append([cirq.SWAP(d,t),CV(c,d), cirq.SWAP(d,t)])
print(puerta)
U = cirq.unitary(puerta)
print(U)
