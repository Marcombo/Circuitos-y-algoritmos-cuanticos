import cirq
import numpy as np
v = cirq.MatrixGate(np.array([
             [(2**0.5)/2, 0.5+0.5j],
             [-0.5+0.5j,(2**0.5)/2]
]))
a = (-np.exp(-np.pi*1j/8)-np.exp(3*np.pi*1j/8))/2
b = (np.exp(np.pi*1j/8)+np.exp(-3*np.pi*1j/8))/2
w = cirq.MatrixGate(np.array([
    [a, -a],
    [b, b]
]))
vv = cirq.MatrixGate(np.array([
             [(2**0.5)/2, ((2**0.5)/2)*1j],
             [((2**0.5)/2)*1j,(2**0.5)/2]
])) 
ww = cirq.MatrixGate(
    np.array([
             [ 0.5-0.5j,((2**0.5)/2)*1j],
             [-0.5-0.5j,-(2**0.5)/2]
]))
q1,q0 = cirq.LineQubit.range(2)
U = cirq.Circuit()
U.append(ww(q0))
U.append([cirq.rz(-np.pi/2)(q1), cirq.CX(q0,q1),cirq.rz(np.pi/2)(q1),cirq.CX(q0,q1)])
U.append(vv(q0))
U.append([cirq.ry(np.pi/2)(q1), cirq.CX(q0,q1),cirq.ry(-np.pi/4)(q1),cirq.CX(q0,q1)])
U.append(w(q0))
U.append([cirq.rz(-np.pi/2)(q1), cirq.CX(q0,q1),cirq.rz(-np.pi/2)(q1),cirq.CX(q0,q1)])
U.append(v(q0))
print(cirq.unitary(U))
