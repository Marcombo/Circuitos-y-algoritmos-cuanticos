#############matriz H truncada################
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
print(setH(2,0.5,1))

    
