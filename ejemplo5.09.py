import cirq
import numpy as np
q = cirq.NamedQubit('a')
puerta = cirq.Circuit(cirq.Z(q)**0.0625)
print(puerta)
