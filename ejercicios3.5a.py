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

