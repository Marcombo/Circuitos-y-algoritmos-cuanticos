import numpy as np
import scipy
U = np.array([
             [0.5, 0.5, 0.5, 0.5],
             [0.5, 0.5j, -0.5, -0.5j],
             [0.5, -0.5, 0.5, -0.5],
             [0.5, -0.5j, -0.5, 0.5j]
])
UCSVB = scipy.linalg.cossin(U,p=2,q=2,separate = True,compute_u = True, compute_vh = True)
U0 = UCSVB[0][0]
U1 = UCSVB[0][1]
U1_adj = U1.conjugate().transpose()
U0_U1 = U0@U1_adj
###DIAGONALIZE WITH SYMPY 
from sympy import *
V, Delta = Matrix(U0_U1).diagonalize()
print("V = ", V, "\n")
print("Delta = ", Delta, "\n")
#####################
V = np.array([
    [(2**0.5)/2, 0.5+0.5j],
    [-0.5+0.5j,(2**0.5)/2]
])
V_adj = V.conjugate().transpose()
D = np.array([
    [1j,0],
    [0, 1]
])
W = D@V_adj@U1
print("W = ", W, "\n")
#####################
VV = np.array([
             [(2**0.5)/2, 0.5+0.5j, 0, 0],
             [-0.5+0.5j,(2**0.5)/2, 0, 0],
             [0, 0, (2**0.5)/2, 0.5+0.5j],
             [0, 0, -0.5+0.5j,(2**0.5)/2]
])
DDadj = np.array([
             [1j, 0, 0, 0],
             [0, 1, 0, 0],
             [0, 0, -1j, 0],
             [0, 0, 0, 1]
])
a = (-np.exp(-np.pi*1j/8)-np.exp(3*np.pi*1j/8))/2
b = (np.exp(np.pi*1j/8)+np.exp(-3*np.pi*1j/8))/2
WW = ([
    [a, -a, 0, 0],
    [b, b, 0, 0],
    [0, 0, a, -a],
    [0, 0, b, b]
])
XX = VV@DDadj@WW 
print("VV´·DDadj·WW =", XX, "\n")


