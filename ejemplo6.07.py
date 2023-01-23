import cirq
CH = cirq.H.controlled()
CCH = CH.controlled()
q0, q1, q2 = cirq.LineQubit.range(3)
operador_dos_niveles = cirq.Circuit()
operador_dos_niveles.append([cirq.X(q0),cirq.CCX(q0,q2,q1),cirq.X(q0),cirq.CCX(q1,q2,q0)])
operador_dos_niveles.append(CCH(q0, q1,q2))
operador_dos_niveles.append([cirq.CCX(q1,q2,q0),cirq.X(q0),cirq.CCX(q0,q2,q1),cirq.X(q0)])                     
print(operador_dos_niveles)
U = cirq.unitary(cirq.Circuit(operador_dos_niveles))
print(U)
