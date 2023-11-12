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
THETA = UCSVB[1]
cos_theta0 = np.cos(THETA[0])
cos_theta1 = np.cos(THETA[1])
sin_theta0 = np.sin(THETA[0])
sin_theta1 = np.sin(THETA[1])
V0adj = UCSVB[2][0]
V1adj = UCSVB[2][1]
print("U0 = ", U0, "\n")
print("U1 = ", U1, "\n")
print("THETA = ", THETA, "\n")
print("cos_theta0 = ", cos_theta0)
print("cos_theta1 = ", cos_theta1)
print("sin_theta0 = ", sin_theta0)
print("sin_theta1 = ", sin_theta1, "\n")
print("V0+ = ", V0adj, "\n")
print("V1+ = ", V1adj, "\n")
#######################
UCSVB = scipy.linalg.cossin(U,p=2,q=2,separate = False,compute_u = True, compute_vh = True)
U0U1 = UCSVB[0]
CS = UCSVB[1]
V0V1adj = UCSVB[2]
XX = (U0U1@CS)@V0V1adj
#print("U0U1 = ", U0U1, "\n")
#print("V0V1+ = ", V0V1adj, "\n")
#print("CS = ", CS, "\n")
print("U0U1·CS·V0V1+ = ", XX)





