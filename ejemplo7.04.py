import numpy as np
n = 4
N = 2**n
r = N**0.5
def qft_matrix():
    matrix = []
    for j in range(N):
        row = []
        for k in range(N):
            jk = (j*k) % N
            row = row + [np.exp((2*np.pi*1j*jk)/N)/r]
        matrix = matrix + [row]
    return matrix
s = [0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0]
s = np.transpose(np.array(s))
A = np.array(qft_matrix())
B = A @ s
print(B)
