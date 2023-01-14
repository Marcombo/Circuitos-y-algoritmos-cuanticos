import cirq
import numpy as np
q = cirq.NamedQubit('a')
puerta = cirq.Circuit(cirq.rz(0.5*np.pi)(q))
print(puerta)
