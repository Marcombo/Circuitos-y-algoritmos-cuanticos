import numpy as np
import scipy
U = np.array([
             [0.5, 0.5, 0.5, 0.5],
             [0.5, 0.5j, -0.5, -0.5j],
             [0.5, -0.5, 0.5, -0.5],
             [0.5, -0.5j, -0.5, 0.5j]
])
UCSVB = scipy.linalg.cossin(U,p=2,q=2,separate = True,compute_u = True, compute_vh = True)
V0 = UCSVB[2][0]
V1 = UCSVB[2][1]
V1_adj = V1.conjugate().transpose()
V0_V1 = V0@V1_adj
###DIAGONALIZE WITH SYMPY 
from sympy import *
V, Delta = Matrix(V0_V1).diagonalize()
print("V = ", V, "\n")
print("Delta = ", Delta, "\n")
#####################
V = np.array([
    [(2**0.5)/2, ((2**0.5)/2)*1j],
    [((2**0.5)/2)*1j,(2**0.5)/2]
])
V_adj = V.conjugate().transpose()
D = np.array([
    [1,0],
    [0, 1j]
])
W = D@V_adj@V1
print("W = ", W, "\n")
#####################
VV = np.array([
             [(2**0.5)/2, ((2**0.5)/2)*1j, 0, 0],
             [((2**0.5)/2)*1j,(2**0.5)/2, 0, 0],
             [0, 0, (2**0.5)/2, ((2**0.5)/2)*1j],
             [0, 0, ((2**0.5)/2)*1j,(2**0.5)/2]
])
    
DDadj = np.array([
             [1, 0, 0, 0],
             [0, 1j, 0, 0],
             [0, 0, 1, 0],
             [0, 0, 0, -1j]
])

WW = np.array([
             [ 0.5-0.5j,((2**0.5)/2)*1j, 0, 0],
             [-0.5-0.5j,-(2**0.5)/2, 0, 0],
             [0, 0, 0.5-0.5j,((2**0.5)/2)*1j],
             [0, 0, -0.5-0.5j,-(2**0.5)/2]
])


