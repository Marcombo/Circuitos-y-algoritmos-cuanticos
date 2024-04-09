###################stat#####CIRCUITOS CUÁNTICOS##########################

import numpy as np

n = 5

### DEFINITION OF AN N-QUBIT QUANTUM STATE REGISTER INITIALLY IN GROUND STATE ###
state = [1]
for i in range(2**n-1):
    state = state + [0]

### GENERIC UNARY OPERATOR [Uij] ON QUBIT NUMBER K###
def U(k,u00,u01,u10,u11):
    m = 2**(n-k-1)
    p = 2**k
    for j in range (p):
        for i in range (2*m*j,(2*j+1)*m):
            a = u00*state[i] + u01*state[m+i]
            state[m+i] = u10*state[i] + u11*state[m+i]
            state[i] = a

### HADAMARD OPERATOR ON QUBIT NUMBER K ###
def H(k):
    U(k,1/(2**0.5),1/(2**0.5),1/(2**0.5),-1/(2**0.5))
    
### X OPERATOR ON QUBIT NUMBER K ###
def X(k):
    U(k,0,1,1,0)
    
### Rphi OPERATOR ON QUBIT NUMBER K ###
def Rphi(k,phi):
    U(k,1,0,0,np.exp(1j*phi))

### NATURAL TO BINARY CONVERSION ###
def ToBin(a,n):
    int_a = a
    bin_a = []
    for i in range(n):
        r = int_a%2
        bin_a = [r] + bin_a
        int_a = int((int_a-r)/2)
    return bin_a

### GENERIC CONTROLLED UNARY OPERATOR [Uij] ON QUBIT NUMBER K###
def CU(l,k,u00,u01,u10,u11):
    m = 2**(n-k-1)
    p = 2**k
    for j in range (p):
        for i in range (2*m*j,(2*j+1)*m):
            bin = ToBin(i,n)
            if bin[l] == 1:
                a = u00*state[i] + u01*state[m+i]
                state[m+i] = u10*state[i] + u11*state[m+i]
                state[i] = a

### OPERATOR CX ON QUBIT NUMBER L CONTROLLED BY QUBIT NUMBER K ###
def CX(k,l):
    CU(k,l,0,1,1,0)

### OPERATOR CRphi ON QUBIT NUMBER L CONTROLLED BY QUBIT NUMBER K ###
def CRphi(k,l,phi):
    CU(k,l,1,0,0,np.exp(1j*phi))

### OPERATOR SWAP(K,L) ###
def SWAP(k,l):
    CX(k,l)
    CX(l,k)
    CX(k,l)

###EXAMPLE 1 ###
"""print(state,"\n")
X(1)
H(1)
Rphi(1,np.pi/2)
print(state,"\n")"""

###EXAMPLE 2 ###
"""print(state,"\n")
X(1)
X(2)
CX(1,2)
X(3)
CRphi(1,3,np.pi/4)
print(state,"\n")"""
    
###EXAMPLE 3: QFT ON QUBITS 1 TO 4 ###
X(2)
X(4)
print(state,"\n")
H(1)
CRphi(2,1,np.pi/2)
CRphi(3,1,np.pi/4)
CRphi(4,1,np.pi/8)
H(2)
CRphi(3,2,np.pi/2)
CRphi(4,2,np.pi/4)
H(3)
CRphi(4,3,np.pi/2)
H(4)
SWAP(1,2)
SWAP(3,4)
SWAP(2,3)
SWAP(1,2)
SWAP(3,4)
SWAP(2,3)
print(state,"\n")




