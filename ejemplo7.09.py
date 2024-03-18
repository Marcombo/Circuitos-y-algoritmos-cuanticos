def fun(a, N, Q):
    f = [1]
    for i in range(Q-1):
        f = f + [(f[i]*a)%N]
    return f
def Prob(y, z, f, N, Q):
    omega = cos(2*pi/Q) + 1j*sin(2*pi/Q)
    s = 0 + 0j
    for x in range(Q):
        if f[x] == z:
            s = s + omega**(x*y)
    norm = s * complex.conjugate(s)
    return norm.real/(Q**2)
def Euclidean(a, b):
    fractions = []
    while b != 0:
        fractions.append(a // b)
        tA = a % b
        a = b
        b = tA
    return fractions
def cf(y, Q, N):
    fractions = Euclidean(y, Q)
    if len(fractions) == 1:
        return 0, 1 
    else:
        depth = 2
        def partial(fractions, depth):
            c = 0
            r = 1
            for i in reversed(range(depth)):
                tR = fractions[i] * r + c
                c = r
                r = tR
            return r, c
        r = 0
        num = 0
        for d in range(depth, len(fractions) + 1):
            tnum, tR = partial(fractions, d)
            if tR == r or tR >= N:
                return num, r
            else:
                r = tR
                num = tnum
        return num, r
######################################
import cirq
import numpy as np
n = 6
M = 2**n
N = 45
a = 29
def u():
    matrix = []
    for i in range(N):
        row = []
        for j in range(N):
            if (a*j)%N == i:
                row = row + [1]
            else:
                row = row + [0]
        for j in range (M-N):
                row = row + [0]        
        matrix = matrix + [row]
    for i in range(M-N):
        row = []
        for j in range(M):
            if j == i+N:
                row = row + [1]
            else:
                row = row + [0]
        matrix = matrix + [row]
    return matrix
B = np.array(u())
B2 = B@B
B4 = B2@B2
B8 = B4@B4
B16 = B8@B8
B32 = B16@B16
B64 = B32@B32
B128 = B64@B64

U = cirq.MatrixGate(B)
U2 = cirq.MatrixGate(B2)
U4 = cirq.MatrixGate(B4)
U8 = cirq.MatrixGate(B8)
U16 = cirq.MatrixGate(B16)
U32 = cirq.MatrixGate(B32)
U64 = cirq.MatrixGate(B64)
U128 = cirq.MatrixGate(B128)

CU = U.controlled()
CU2 = U2.controlled()
CU4 = U4.controlled()
CU8 = U8.controlled()
CU16 = U16.controlled()
CU32 = U32.controlled()
CU64 = U64.controlled()
CU128 = U128.controlled()

t = 8
T = 2**t
r = T**0.5

def QFT_inv():
    matrix = []
    for j in range(T):
        row = []
        for k in range(T):
            jk = (j*k) % T
            row = row + [np.exp((-2*np.pi*1j*jk)/T)/r]
        matrix = matrix + [row]
    return matrix
A = np.array(QFT_inv())
qft_inv = cirq.MatrixGate(A)

q1,q2,q3,q4,q5,q6,q7,q8,p1,p2,p3,p4,p5,p6 = cirq.LineQubit.range(14)

fase_estim = cirq.Circuit([cirq.H(q1), cirq.H(q2), cirq.H(q3),
                           cirq.H(q4), cirq.H(q5), cirq.H(q6),
                           cirq.H(q7), cirq.H(q8), cirq.X(p6)])

fase_estim.append(CU(q8,p1,p2,p3,p4,p5,p6))
fase_estim.append(CU2(q7,p1,p2,p3,p4,p5,p6))
fase_estim.append(CU4(q6,p1,p2,p3,p4,p5,p6))
fase_estim.append(CU8(q5,p1,p2,p3,p4,p5,p6))
fase_estim.append(CU16(q4,p1,p2,p3,p4,p5,p6))
fase_estim.append(CU32(q3,p1,p2,p3,p4,p5,p6))
fase_estim.append(CU64(q2,p1,p2,p3,p4,p5,p6))
fase_estim.append(CU128(q1,p1,p2,p3,p4,p5,p6))

fase_estim.append(qft_inv(q1,q2,q3,q4,q5,q6,q7,q8))

fase_estim.append(cirq.measure(q1,q2,q3,q4,q5,q6,q7,q8,key = 'mediciones'))

un_simulador = cirq.Simulator()
resultado = un_simulador.run(fase_estim, repetitions=100)
print(resultado.histogram(key='mediciones'))
