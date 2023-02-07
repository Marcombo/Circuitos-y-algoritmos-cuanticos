import cirq
#print("0101")
j = [0,1,0,1]
j1, j2, j3, j4 = cirq.LineQubit.range(4)
qft = cirq.Circuit()
if j[0] == 1:
    qft.append(cirq.X(j1))
if j[1] == 1:
    qft.append(cirq.X(j2))
if j[2] == 1:
    qft.append(cirq.X(j3))
if j[3] == 1:
    qft.append(cirq.X(j4))
CRpi_2 = cirq.S.controlled()
CRpi_4 = cirq.T.controlled()
CRpi_8 = (cirq.T**0.5).controlled()   
qft.append([cirq.H(j1),CRpi_2(j2, j1), CRpi_4(j3,j1),CRpi_8(j4,j1)])
qft.append([cirq.H(j2),CRpi_2(j3, j2), CRpi_4(j4,j2)])
qft.append([cirq.H(j3),CRpi_2(j4, j3)])
qft.append([cirq.H(j4)])
qft.append([cirq.SWAP(j1,j2), cirq.SWAP(j3,j4), cirq.SWAP(j2,j3),
cirq.SWAP(j1,j2), cirq.SWAP(j3,j4), cirq.SWAP(j2,j3)])
#print(qft)
un_simulador = cirq.Simulator()
estado_final = un_simulador.simulate(qft)
print(estado_final)
