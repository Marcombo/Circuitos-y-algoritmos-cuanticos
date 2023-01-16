import cirq
q = cirq.NamedQubit('a')
circuito = cirq.Circuit()
for i in range(3):
    circuito.append(cirq.Z(q)**0.125)
print(circuito)
