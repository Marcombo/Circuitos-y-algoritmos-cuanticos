import cirq
j = [1,0,1]
j1, j2, j3 = cirq.LineQubit.range(3)
qft = cirq.Circuit()
if j[0] == 1:
    qft.append(cirq.X(j1))
if j[1] == 1:
    qft.append(cirq.X(j2))
if j[2] == 1:
    qft.append(cirq.X(j3))
CRpi_2 = cirq.S.controlled()
CRpi_4 = cirq.T.controlled()   
qft.append([cirq.H(j1),CRpi_2(j2, j1), CRpi_4(j3,j1)])
qft.append([cirq.H(j2),CRpi_2(j3, j2)])
qft.append([cirq.H(j3)])
#print(qft)
un_simulador = cirq.Simulator()
estado_final = un_simulador.simulate(qft)
print(estado_final)
