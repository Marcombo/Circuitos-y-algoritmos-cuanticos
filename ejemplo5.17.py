import cirq
import numpy
V = cirq.Z**0.5
Vadj = cirq.Z**-0.5
CV = V.controlled()
CVadj = Vadj.controlled()
c, d, t = cirq.LineQubit.range(3)
puerta = cirq.Circuit(CV(d,t), cirq.CX(c,d), CVadj(d,t), cirq.CX(c,d), CV(c,t))
print(puerta)
U = cirq.unitary(puerta)
print(U)
############################
import cirq
import numpy
V = cirq.Z**0.5
Vadj = cirq.Z**-0.5
CV = V.controlled()
CVadj = Vadj.controlled()
c, d, t = cirq.LineQubit.range(3)
puerta = cirq.Circuit(CV(d,t), cirq.CX(c,d), CVadj(d,t), cirq.CX(c,d), cirq.SWAP(d,t),CV(c,d), cirq.SWAP(d,t))
print(puerta)
U = cirq.unitary(puerta)
print(U)
