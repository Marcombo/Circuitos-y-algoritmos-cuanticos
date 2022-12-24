########################valores propios###############
import numpy as np
from numpy import linalg
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
def eigen(N,ng,eJ):
    M = setH(N,ng,eJ)
    return linalg.eigvals(M)
def main(N):
    for eJ in [1,50]:
        for ng in [-1,-0.5,0,0.5,1]:
            print("eJ =", eJ, "ng =", ng)
            values = eigen(N,ng,eJ)
            values.sort()
            print(values[0:4])
main(5)
