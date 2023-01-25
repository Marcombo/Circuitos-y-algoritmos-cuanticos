########################CV##################
import cirq
import numpy as np
class CV(cirq.Gate):
    def __init__(self):
        super(CV, self)
    def _num_qubits_(self):
        return 2
    def _decompose_(self, qubits):
        c,t = qubits
        yield cirq.rz(0.5*np.pi)(t)
        yield cirq.CX(c,t)
        yield cirq.ry(-0.25*np.pi)(t)
        yield cirq.CX(c,t)
        yield cirq.ry(0.25*np.pi)(t)
        yield cirq.rz(-0.5*np.pi)(t)
        yield cirq.T(c)      
    def _circuit_diagram_info_(self, args):
        return ["CV"] * self.num_qubits()
cv = CV()
c, t = cirq.LineQubit.range(2)
V_controlado = cirq.Circuit()
V_controlado.append(cv(c,t))
print(V_controlado)
U = cirq.unitary(cirq.Circuit(V_controlado))
print("CV = ", U)

########################CV_adj##################
import cirq
import numpy as np
T_adj = cirq.MatrixGate(np.array([
    [1.0,  0.0],
    [0.0, np.exp(-0.25j*np.pi)]
    ])
)
class CV_adj(cirq.Gate):
    def __init__(self):
        super(CV_adj, self)
    def _num_qubits_(self):
        return 2
    def _decompose_(self, qubits):
        c,t = qubits
        yield cirq.rz(-0.5*np.pi)(t)
        yield cirq.CX(c,t)
        yield cirq.ry(-0.25*np.pi)(t)
        yield cirq.CX(c,t)
        yield cirq.ry(0.25*np.pi)(t)
        yield cirq.rz(0.5*np.pi)(t)
        yield T_adj(c)      
    def _circuit_diagram_info_(self, args):
        return ["CV_adj"] * self.num_qubits()
cv_adj = CV_adj()
c, t = cirq.LineQubit.range(2)
Vadj_controlado = cirq.Circuit()
Vadj_controlado.append(cv_adj(c,t))
U = cirq.unitary(cirq.Circuit(Vadj_controlado))
print("CVadj = ", U)

########################Toffoli1########################
c,d,t = cirq.LineQubit.range(3)
Toffoli1 = cirq.Circuit()
Toffoli1.append([cv(d,t),cirq.CX(c,d),cv_adj(d,t),cirq.CX(c,d),cv(c,t)])
U = cirq.unitary(cirq.Circuit(Toffoli1))
print("CCX = ", U)

