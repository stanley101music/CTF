# e is small
# m2 = f(m1) for some linear polynomial f = a*x +b

from Crypto.Util.number import *
p = getPrime(256)
q = getPrime(256)
n = p*q
e = 11

m1 = 69420
a = randrange(n)
b = randrange(n)
m2 = (a*m1+b)%n

c1 = pow(m1, e, n)
c2 = pow(m2, e, n)

F.<x> = PolynomialRing(Zmod(n))

# m1 is a root of g1(x)
g1 = x^e - c1
# m1 is a root of g2(x)
g2 = (a*x+b)^e - c2

# (x-m1) divides both g1, g2
# GCD(g1, g2) = x-m1
while g2!=0:
    g1 -= (g1//g2)*g2
    g1, g2 = g2, g1
# monic(): Return this polynomial divided by its leading coefficient
# Make the leading coefficient = 1
g1 = g1.monic()
# g1[i]: The coefficient of i-th term, so g1[0] = coefficient of x^0 = the value of constant
m = -g1[0]%n    # m = m1