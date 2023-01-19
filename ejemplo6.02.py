import cirq
q0, q1, q2, q3, q4, q5, q6 = cirq.LineQubit.range(7)
multiplexor = cirq.Circuit()
multiplexor.append([cirq.H(q0), cirq.H(q2), cirq.H(q4)])
multiplexor.append([cirq.X(q3),cirq.X(q5),cirq.X(q6),
                    cirq.CX(q0, q1),
                    cirq.X(q0), cirq.CCX(q1, q4, q5),
                    cirq.CCX(q0, q2, q3),
                    cirq.CCX(q3, q5, q6)])
multiplexor.append(cirq.measure(q0, q1, q2, q4, q6))
print(multiplexor)
un_simulador = cirq.Simulator()
resultado = un_simulador.run(multiplexor, repetitions=20)
print(resultado)
