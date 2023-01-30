import numpy as np
def estimation(alpha, delta):
    a = (np.cos(np.pi/8))**2
    gama = 2*np.arccos(a)
    #alpha = 2.956
    #emax = 0.1
    m = int(2*np.pi/gama)
    n = int(alpha/gama)
    estim = n*gama
    error = alpha - estim
    while abs(error) > delta:
        if error > 0:
            n = n + m +1
        else:
            n = n + m
        if int(n*gama/(2*np.pi)) > 0:
            estim = n*gama - int(n*gama/(2*np.pi))*2*np.pi
        error = alpha - estim
    return n


