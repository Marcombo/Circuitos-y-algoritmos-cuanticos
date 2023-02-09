import random

def gcd(a, b):
    while b != 0:
        ta = a%b
        a = b
        b = ta
    return a
                
def roots(N):
    k = 2
    d1 = N
    d2 = 1
    Found = False
    while (1 == 1):
        s = 2
        if s**k > N:
            break
        else:
            while (1 == 1):
                if s**k > N:
                    break
                elif s**k == N:
                    d1 = s
                    d2 = s**(k-1)
                    Found = True
                    break
                else:
                    s = s+1
        k = k+1
    return Found, d1, d2

def order(a, N): 
    r = 2
    b = (a*a)%N
    while b != 1:
        b = (b*a)%N
        r = r+1
    return r

def divisors(N):
    if N%2 == 0:
        d1 = 2
        d2 = N//2
    else:
        Found, a1, a2 = roots(N)
        if Found:
            d1 = a1
            d2 = a2
        else:
            a = 2
            while 1 == 1:
                b = gcd(a, N)
                if b > 1:
                    d1 = b
                    d2 = N//b
                    break
                else:
                    r = order(a, N)
                    if (r%2 == 0) and ((a**(r//2) + 1)%N != 0):
                        e = a**(r//2)
                        d1 = gcd(e - 1, N)
                        d2 = gcd(e + 1, N)
                        break
                    a = a + 1
    return d1, d2                
    
