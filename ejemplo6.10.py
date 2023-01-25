############THTH############
import cirq
import numpy as np
a = cirq.NamedQubit('a')
THTH = cirq.Circuit(cirq.H(a),cirq.T(a),cirq.H(a),cirq.T(a))
R = (cirq.unitary(THTH))*np.exp(-0.25j*np.pi)
ROTthth = cirq.MatrixGate(np.array(R))
q1 = cirq.NamedQubit('q1')
rot1 = cirq.Circuit(ROTthth(q1))
print("THTH = ", rot1)
########################rotacion Rn(gama)###########
nx = np.cos(np.pi/8)/np.sqrt(1+(np.cos(np.pi/8))**2)
ny = np.sin(np.pi/8)/np.sqrt(1+(np.cos(np.pi/8))**2)
a = (np.cos(np.pi/8))**2
gama = 2*np.arccos(a)
n00 = np.cos(gama/2) - 1j*nx*np.sin(gama/2)
n01 = - (ny+1j*nx)*np.sin(gama/2)
n10 = (ny-1j*nx)*np.sin(gama/2)
n11 = np.cos(gama/2) + 1j*nx*np.sin(gama/2)
ROTgama = cirq.MatrixGate(np.array([
    [n00, n01],
    [n10, n11]
    ]) 
)
q2 = cirq.NamedQubit('q2')
rot2 = cirq.Circuit(ROTgama(q2))
print("ROT = ", rot2)
