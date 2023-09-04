import cirq
import numpy as np
A = np.array([
    [1, 1j],
    [-1j, -1]
    ])
I = np.array([
    [1, 0],
    [0, 1]
    ])
tau = 0.25
k = 50
def HamSim(A, tau, k):
    fac = 1
    mat = A
    acc = I
    for n in range(1,k+1,1):
        coef = ((1j*tau)**n)/fac
        acc = acc + coef*mat
        mat = mat@A
        fac = fac*(n+1)
    return acc
print(HamSim(A, tau, k))
