import cirq
import numpy as np
c, t = cirq.LineQubit.range(2)
H_controlado = cirq.Circuit()
H_controlado.append([cirq.rz(0.5*np.pi)(t),cirq.CX(c,t),
                    cirq.rz(-0.5*np.pi)(t),cirq.ry(-0.25*np.pi)(t),cirq.CX(c,t),
                    cirq.ry(0.25*np.pi)(t)])
H_controlado.append(cirq.S(c))
print(H_controlado)
U = cirq.unitary(cirq.Circuit(H_controlado))
print(U)
