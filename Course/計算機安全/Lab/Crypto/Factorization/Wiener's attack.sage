# d too small
from Crypto.Util.number import *
from math import *
import gmpy2

p = getPrime(256)
q = getPrime(256)
n = p*q
phi = (p-1)*(q-1)
d = randrange(math.isqrt(math.isqrt(n))/3)
e = inverse(d, phi)
f = continued_fraction(e/n)
for i in range(len(f)):
    k, d = f.numerator(i+1), f.denominator(i+1)
    phi = (e*d-1)//k
    # x^2 - (n-phi+1)*x + n = 0
    # x = p or q
    # p+q = n-phi+1
    # p*q = n
    det = (n-phi+1)^2 - 4*n
    if isqrt(det)**2 == det:
        break
print(k, d)

p = ((n-phi+1) - isqrt(det))//2
q = n//p
print(p, q)