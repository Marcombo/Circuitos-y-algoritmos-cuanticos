import cirq
import numpy as np
###OPERANDOS: x = [x1, x0], y = [y3, y2, y1, y0], a = [a1, a0], OPERACIÓN = a·x + y
x = [1,1]
y = [0,0,1,1]
a = [1,1]
y0, y1, y2, y3, x0, x1, a0, a1 = cirq.LineQubit.range(8)
adder = cirq.Circuit()
###INICIALIZACIÓN###
if y[2] == 1:
    adder.append(cirq.X(y1))
if y[3] == 1:
    adder.append(cirq.X(y0))
if x[0] == 1:
    adder.append(cirq.X(x1))
if x[1] == 1:
    adder.append(cirq.X(x0))
if a[0] == 1:
    adder.append(cirq.X(a1))
if a[1] == 1:
    adder.append(cirq.X(a0))
###QFT###
CR1 = (cirq.Z**0.5).controlled()
CR2 = (cirq.Z**0.25).controlled()
CR3 = (cirq.Z**0.125).controlled()
adder.append([cirq.H(y3),CR1(y2, y3),CR2(y1,y3),CR3(y0,y3)])
adder.append([cirq.H(y2),CR1(y1, y2),CR2(y0,y2)])
adder.append([cirq.H(y1),CR1(y0, y1)])
adder.append([cirq.H(y0)])
###CZ###
CR0 = cirq.CZ
CCR0 = CR0.controlled()
CCR1 = CR1.controlled()
CCR2 = CR2.controlled()
CCR3 = CR3.controlled()
adder.append([CCR2(a0,x1,y3),CCR1(a1,x1,y3),CCR3(a0,x0,y3),CCR2(a1,x0,y3)])
adder.append([CCR1(a0,x1,y2),CCR0(a1,x1,y2),CCR2(a0,x0,y2),CCR1(a1,x0,y2)])
adder.append([CCR0(a0,x1,y1),CCR1(a0,x0,y1),CCR0(a1,x0,y1)])
adder.append([CCR0(a0,x0,y0)])
###IQFT###
CR_minus_1 = (cirq.Z**(-0.5)).controlled()
CR_minus_2 = (cirq.Z**(-0.25)).controlled()
CR_minus_3 = (cirq.Z**(-0.125)).controlled()
adder.append([cirq.H(y0)])
adder.append([CR_minus_1(y0,y1),cirq.H(y1)])
adder.append([CR_minus_2(y0,y2),CR_minus_1(y1,y2),cirq.H(y2)])
adder.append([CR_minus_3(y0,y3),CR_minus_2(y1,y3),CR_minus_1(y2, y3),cirq.H(y3)])
###MEDICIÓN###
adder.append(cirq.measure(y3,y2,y1,y0,key = 'suma'))
#print(adder)
un_simulador = cirq.Simulator()
resultado = un_simulador.run(adder, repetitions = 1)
print(resultado)
