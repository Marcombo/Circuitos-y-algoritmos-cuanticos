import cirq
import numpy as np
t = 4
T = 2**t
r = T**0.5
n = t
s = t+1
p = 5
tau = 0.25
A = np.array([
    [1, 1j],
    [-1j, -1]
    ])
I = np.array([
    [1, 0],
    [0, 1]
    ])
k = 50
def HamSim(A, tau, k):
    fac = 1
    mat = A
    acc = I
    for n in range(1,k+1,1):
        coef = ((1j*tau)**n)/fac
        acc = acc + coef*mat
        mat = mat@A
        fac = fac*(n+1)
    return acc
B = HamSim(A,tau,k)
B2 = B@B
B4 = B2@B2
B8 = B4@B4
U = cirq.MatrixGate(B)
U2 = cirq.MatrixGate(B2)
U4 = cirq.MatrixGate(B4)
U8 = cirq.MatrixGate(B8)
CU = U.controlled()
CU2 = U2.controlled()
CU4 = U4.controlled()
CU8 = U8.controlled()
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
q1,q2,q3,q4,q,a,y1,y2,y3,y4,y5 = cirq.LineQubit.range(11)
HHL = cirq.Circuit([cirq.H(q1), cirq.H(q2), cirq.H(q3),
                           cirq.H(q4)])

#HHL.append(cirq.X(q))
#HHL.append(cirq.H(q))
HHL.append(cirq.rx(2*np.arccos(0.924))(q))

HHL.append(CU(q4,q))
HHL.append(CU2(q3,q))
HHL.append(CU4(q2,q))
HHL.append(CU8(q1,q))
HHL.append(qft_inv(q1,q2,q3,q4))
####################ROTACIÓN#######################
def ToBin(a,p):
    int_a = a
    bin_a = []
    for i in range(p):
        r = int_a%2
        bin_a = [r] + bin_a
        int_a = int(int_a/2)
    return bin_a
def thetas(t,s):
    lista = [0]
    for i in range(1,2**(t-1),1):
        f = int((2**s)/i)
        x = int((2*np.arcsin(f/(2**(s+1))))*(2**(p-2)))
        lista = lista + [x]
    for i in range(2**(t-1), 2**t,1):
        f = int((2**s)/(i-2**t))
        x = int((2*np.arcsin(f/(2**(s+1))))*(2**(p-2)))+ (2**p)

        lista = lista + [x]
    return lista
def truth_table(t,s,p):
    M = np.zeros((2**t,p))
    for i in range(2**t):
        x = thetas(t,s)[i]
        y = ToBin(x,p)
        M[i] = y
    return M
table = truth_table(t,s,p)
def Uf(t,p):
    N = 2**(t+p)
    matrix = np.zeros((N,N))
    for i in range(N):
        for j in range(N):
            bin_i = ToBin(i,t+p)
            bin_j = ToBin(j,t+p)
            matrix[i][j] = 1
            if (bin_j[:t] != bin_i[:t]):
                matrix[i][j] = 0
            for k in range(p):
                if bin_j[t+k] != (bin_i[t+k] + F(bin_i[:t],k))%2:
                    matrix[i][j] = 0
    return matrix
def F(x,y):
    acc = 0
    for i in range(t):
        acc = acc + x[i]*(2**(t-1-i))
    return table[acc][y]
RC = cirq.MatrixGate(Uf(t,p))
CRY1 = cirq.ry(-2).controlled()
CRY2 = cirq.ry(1).controlled()
CRY3 = cirq.ry(1/2).controlled()
CRY4 = cirq.ry(1/4).controlled()
CRY5 = cirq.ry(1/8).controlled()
HHL.append(RC(q1,q2,q3,q4,y1,y2,y3,y4,y5))
HHL.append(CRY1(y1,a))
HHL.append(CRY2(y2,a))
HHL.append(CRY3(y3,a))
HHL.append(CRY4(y4,a))
HHL.append(CRY5(y5,a))
HHL.append(RC(q1,q2,q3,q4,y1,y2,y3,y4,y5))
###################QPE_INV############################
C = (B.transpose()).conjugate()
C2 = C@C
C4 = C2@C2
C8 = C4@C4
UU = cirq.MatrixGate(C)
UU2 = cirq.MatrixGate(C2)
UU4 = cirq.MatrixGate(C4)
UU8 = cirq.MatrixGate(C8)
CUU = UU.controlled()
CUU2 = UU2.controlled()
CUU4 = UU4.controlled()
CUU8 = UU8.controlled()
def QFT():
    matrix = []
    for j in range(T):
        row = []
        for k in range(T):
            jk = (j*k) % T
            row = row + [np.exp((2*np.pi*1j*jk)/T)/r]
        matrix = matrix + [row]
    return matrix
AA = np.array(QFT())
qft = cirq.MatrixGate(AA)
HHL.append(qft(q1,q2,q3,q4))
HHL.append(CUU8(q1,q))
HHL.append(CUU4(q2,q))
HHL.append(CUU2(q3,q))
HHL.append(CUU(q4,q))
HHL.append([cirq.H(q1), cirq.H(q2), cirq.H(q3),
                           cirq.H(q4)])
HHL.append(cirq.measure(q1,q2,q3,q4,y1,y2,y3,y4,y5,a))
un_simulador = cirq.Simulator()
estado_final = un_simulador.simulate(HHL)
print(estado_final)
