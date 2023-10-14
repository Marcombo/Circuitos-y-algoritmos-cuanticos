import cirq
import numpy as np
phi_div_pi = 1/16
c1,c2,q = cirq.LineQubit.range(3)
ccr = cirq.Circuit()
control = [1,1]
ccr.append([cirq.H(q)])
if control[0] == 1:
    ccr.append(cirq.X(c1))
if control[1] == 1:
    ccr.append(cirq.X(c2))
ccr.append([(cirq.Z**(-phi_div_pi/2))(q),cirq.CCX(c1,c2,q),(cirq.Z**(-phi_div_pi/2))(q),
            cirq.CCX(c1,c2,q),(cirq.Z**phi_div_pi)(q)])
ccr.append([(cirq.Z**(-phi_div_pi/4))(c2),cirq.CX(c1,c2),(cirq.Z**(-phi_div_pi/4))(c2),
            cirq.CX(c1,c2),(cirq.Z**(phi_div_pi/2))(c2)])
ccr.append((cirq.Z**(1/64))(c1))
un_simulador = cirq.Simulator()
estado_final = un_simulador.simulate(ccr)
print(ccr)
print(estado_final)

"""test = (np.exp(1.j*np.pi/16))/(2**0.5)
print("test =", test)""" 
