import cirq
###OPERANDOS: x = [x3, x2, x1, x0], y = [y3, y2, y1, y0]
x = [1,1,0,0]
y = [1,0,0,1]
y4,y3,y2,y1,y0,x3,x2,x1,x0  = cirq.LineQubit.range(9)
adder = cirq.Circuit()
###INICIALIZACIÓN###
if y[0] == 1:
    adder.append(cirq.X(y3))
if y[1] == 1:
    adder.append(cirq.X(y2))
if y[2] == 1:
    adder.append(cirq.X(y1))
if y[3] == 1:
    adder.append(cirq.X(y0))
if x[0] == 1:
    adder.append(cirq.X(x3))
if x[1] == 1:
    adder.append(cirq.X(x2))
if x[2] == 1:
    adder.append(cirq.X(x1))
if x[3] == 1:
    adder.append(cirq.X(x0))
###QFT###
CRpi_2 = cirq.S.controlled()
CRpi_4 = cirq.T.controlled()
CRpi_8 = (cirq.T**0.5).controlled()
CRpi_16 = (cirq.T**0.25).controlled()
adder.append([cirq.H(y4),CRpi_2(y3,y4),CRpi_4(y2,y4),CRpi_8(y1,y4),CRpi_16(y0,y4)])
adder.append([cirq.H(y3),CRpi_2(y2,y3),CRpi_4(y1,y3),CRpi_8(y0,y3)])
adder.append([cirq.H(y2),CRpi_2(y1,y2),CRpi_4(y0,y2)])
adder.append([cirq.H(y1),CRpi_2(y0,y1)])
adder.append([cirq.H(y0)])
###CZ###
adder.append([CRpi_2(x3,y4),CRpi_4(x2,y4),CRpi_8(x1,y4),CRpi_16(x0,y4)])
adder.append([cirq.CZ(x3,y3),CRpi_2(x2,y3),CRpi_4(x1,y3),CRpi_8(x0,y3)])
adder.append([cirq.CZ(x2,y2),CRpi_2(x1,y2),CRpi_4(x0,y2)])
adder.append([cirq.CZ(x1,y1),CRpi_2(x0,y1)])
adder.append([cirq.CZ(x0,y0)])
###IQFT###
CR_minus_pi_2 = (cirq.Z**(-0.5)).controlled()
CR_minus_pi_4 = (cirq.Z**(-0.25)).controlled()
CR_minus_pi_8 = (cirq.Z**(-0.125)).controlled()
CR_minus_pi_16 = (cirq.Z**(-0.0625)).controlled()
adder.append([cirq.H(y0)])
adder.append([CR_minus_pi_2(y0,y1),cirq.H(y1)])
adder.append([CR_minus_pi_4(y0,y2),CR_minus_pi_2(y1,y2),cirq.H(y2)])
adder.append([CR_minus_pi_8(y0,y3),CR_minus_pi_4(y1,y3),CR_minus_pi_2(y2,y3),cirq.H(y3)])
adder.append([CR_minus_pi_16(y0,y4),CR_minus_pi_8(y1,y4),CR_minus_pi_4(y2,y4),CR_minus_pi_2(y3,y4),cirq.H(y4)])
###MEDICIÓN###
adder.append(cirq.measure(y4,y3,y2,y1,y0,key = 'suma'))
#print(adder)
un_simulador = cirq.Simulator()
resultado = un_simulador.run(adder, repetitions = 1)
print(resultado)
