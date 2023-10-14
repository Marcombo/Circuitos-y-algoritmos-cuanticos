import cirq
###OPERANDOS: x = [x3, x2, x1, x0], y = [y3, y2, y1, y0]
X1 = [1,1,0,0]
X2 = [0,1,0,1]
X3 = [1,0,0,1]
X4 = [1,0,1,1]
X13, X12, X11, X10, X23, X22, X21, X20, X33, X32, X31, X30, X43, X42, X41, X40,   = cirq.LineQubit.range(16)
adder = cirq.Circuit()
###INICIALIZACIÓN###
if X1[0] == 1:
    adder.append(cirq.X(X13))
if X1[1] == 1:
    adder.append(cirq.X(X12))
if X1[2] == 1:
    adder.append(cirq.X(X11))
if X1[3] == 1:
    adder.append(cirq.X(X10))
if X2[0] == 1:
    adder.append(cirq.X(X23))
if X2[1] == 1:
    adder.append(cirq.X(X22))
if X2[2] == 1:
    adder.append(cirq.X(X21))
if X2[3] == 1:
    adder.append(cirq.X(X20))
if X3[0] == 1:
    adder.append(cirq.X(X33))
if X3[1] == 1:
    adder.append(cirq.X(X32))
if X3[2] == 1:
    adder.append(cirq.X(X31))
if X3[3] == 1:
    adder.append(cirq.X(X30))
if X4[0] == 1:
    adder.append(cirq.X(X43))
if X4[1] == 1:
    adder.append(cirq.X(X42))
if X4[2] == 1:
    adder.append(cirq.X(X41))
if X4[3] == 1:
    adder.append(cirq.X(X40))
###QFT###
CRpi_2 = cirq.S.controlled()
CRpi_4 = cirq.T.controlled()
CRpi_8 = (cirq.T**0.5).controlled()   
adder.append([cirq.H(X43),CRpi_2(X42, X43), CRpi_4(X41,X43),CRpi_8(X40,X43)])
adder.append([cirq.H(X42),CRpi_2(X41, X42), CRpi_4(X40,X42)])
adder.append([cirq.H(X41),CRpi_2(X40, X41)])
adder.append([cirq.H(X40)])
###CZ1###
adder.append([cirq.CZ(X33,X43),CRpi_2(X32, X43), CRpi_4(X31,X43),CRpi_8(X30,X43)])
adder.append([cirq.CZ(X32,X42),CRpi_2(X31, X42), CRpi_4(X30,X42)])
adder.append([cirq.CZ(X31,X41),CRpi_2(X30, X41)])
adder.append([cirq.CZ(X30,X40)])
###CZ2###
adder.append([cirq.CZ(X23,X43),CRpi_2(X22, X43), CRpi_4(X21,X43),CRpi_8(X20,X43)])
adder.append([cirq.CZ(X22,X42),CRpi_2(X21, X42), CRpi_4(X20,X42)])
adder.append([cirq.CZ(X21,X41),CRpi_2(X20, X41)])
adder.append([cirq.CZ(X20,X40)])
###CZ3###
adder.append([cirq.CZ(X13,X43),CRpi_2(X12, X43), CRpi_4(X11,X43),CRpi_8(X10,X43)])
adder.append([cirq.CZ(X12,X42),CRpi_2(X11, X42), CRpi_4(X10,X42)])
adder.append([cirq.CZ(X11,X41),CRpi_2(X10, X41)])
adder.append([cirq.CZ(X10,X40)])
###IQFT###
CR_minus_pi_2 = (cirq.Z**(-0.5)).controlled()
CR_minus_pi_4 = (cirq.Z**(-0.25)).controlled()
CR_minus_pi_8 = (cirq.Z**(-0.125)).controlled()
adder.append([cirq.H(X40)])
adder.append([CR_minus_pi_2(X40,X41),cirq.H(X41)])
adder.append([CR_minus_pi_4(X40,X42),CR_minus_pi_2(X41,X42),cirq.H(X42)])
adder.append([CR_minus_pi_8(X40,X43),CR_minus_pi_4(X41,X43),CR_minus_pi_2(X42,X43),cirq.H(X43)])
###MEDICIÓN###
adder.append(cirq.measure(X43,X42,X41,X40,key = 'suma'))
#print(adder)
un_simulador = cirq.Simulator()
resultado = un_simulador.run(adder, repetitions = 1)
print(resultado)
