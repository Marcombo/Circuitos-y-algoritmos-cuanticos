import numpy as np
U = np.array([[0,-1j/np.sqrt(2), 0, -1j/np.sqrt(2)],
             [1j/np.sqrt(2),0, 1j/np.sqrt(2), 0],
             [0,-1j/np.sqrt(2), 0, 1j/np.sqrt(2)],
             [1j/np.sqrt(2),0, -1j/np.sqrt(2), 0]])

A1 = np.array([[0,-1j, 0, 0],
             [1j, 0, 0, 0],
             [0, 0, 1, 0],
             [0, 0, 0, 1]])

A2 = np.array([[1/np.sqrt(2), 0, 0, -1j/np.sqrt(2)],
             [0, 1, 0, 0],
             [0, 0, 1, 0],
             [1j/np.sqrt(2), 0, 0, -1/np.sqrt(2)]])

A3 = np.array([[1, 0, 0, 0],
             [0, 1/np.sqrt(2), 1j/np.sqrt(2), 0],
             [0, -1j/np.sqrt(2), -1/np.sqrt(2), 0],
             [0, 0, 0, 1]])

A4 = np.array([[1, 0, 0, 0],
             [0, 1, 0, 0],
             [0, 0, 0, -1j],
             [0, 0, 1j, 0]])

M = A1 @ A2 @ A3 @ A4

print(M)
