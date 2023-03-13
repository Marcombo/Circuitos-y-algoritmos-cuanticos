import numpy as np
from numpy import linalg

N = 2
ng = 0
eJ = 50

def resetH(N):
    return np.zeros((2*N+1, 2*N+1))
def setH(N, ng, eJ):
    MH = resetH(N)
    for i in range(2*N+1):
        MH[i,i] = 4*((i-N-ng)**2)
    for i in range(1,2*N+1):
        MH[i-1,i] = -0.5*eJ
    for i in range(2*N):
        MH[i+1,i] = -0.5*eJ
    return MH    

def eigen_vectors(N,ng,eJ):
    M = setH(N,ng,eJ)
    vector_list = linalg.eig(M)[1]
    for i in range(2*N+1):
        V = [vector_list[0,i]]
        for j in range(2*N):
            V = V+[vector_list[j+1,i]]
        P = M@V
        Q = P/V
        print("eigen_vector(",i,")=", V)
        print("eigen_value(",i,")=",Q[0])
        print("================================================================")

eigen_vectors(N,ng,eJ)

v0 = [-0.2253978360612247, -0.49772406702680333, -0.6347701451725904, -0.4977240670268029, -0.2253978360612244]

v1 = [0.4377862056771192, 0.5552866269944118, 8.241172092603234e-18, -0.5552866269944119, -0.4377862056771194]

v2 = [0.5576465182758401, 0.12342013749550008, -0.5895724388324555, 0.12342013749550036, 0.5576465182758404]

v3 = [-0.555286626994412, 0.4377862056771198, -8.300428695993057e-16, -0.43778620567711884, 0.5552866269944116]

v4 = [-0.3717878106578396, 0.486865713275118, -0.4994709222434463, 0.48686571327511957, -0.3717878106578417]

acc = 0
for i in range(5):
    acc = acc + v0[i]**2
print("(v0,v0) = ", acc)

acc = 0
for i in range(5):
    acc = acc + v1[i]**2
print("(v1,v1) = ", acc)

acc = 0
for i in range(5):
    acc = acc + v2[i]**2
print("(v2,v2) = ", acc)

acc = 0
for i in range(5):
    acc = acc + v3[i]**2
print("(v3,v3) = ", acc)

acc = 0
for i in range(5):
    acc = acc + v4[i]**2
print("(v4,v4) = ", acc)

acc = 0
for i in range(5):
    acc = acc + v0[i]*v1[i]
print("(v0,v1) = ", acc)

acc = 0
for i in range(5):
    acc = acc + v0[i]*v2[i]
print("(v0,v2) = ", acc)

acc = 0
for i in range(5):
    acc = acc + v0[i]*v3[i]
print("(v0,v3) = ", acc)

acc = 0
for i in range(5):
    acc = acc + v0[i]*v4[i]
print("(v0,v4) = ", acc)

acc = 0
for i in range(5):
    acc = acc + v1[i]*v2[i]
print("(v1,v2) = ", acc)

acc = 0
for i in range(5):
    acc = acc + v1[i]*v3[i]
print("(v1,v3) = ", acc)

acc = 0
for i in range(5):
    acc = acc + v1[i]*v4[i]
print("(v1,v4) = ", acc)

acc = 0
for i in range(5):
    acc = acc + v2[i]*v3[i]
print("(v2,v3) = ", acc)

acc = 0
for i in range(5):
    acc = 0

for i in range(5):
    acc = acc + v3[i]*v4[i]
print("(v3,v4) = ", acc)

M = np.matrix([v0, v1, v2, v3, v4]).transpose()
print("M = ", M)

print("M@MT = ", M @ M.transpose())

