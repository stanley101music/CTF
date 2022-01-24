from math import *

# p-1's biggest prime factor <= B
# p-1 | B! = 1*2*...*B
# 2**(B!) = 2**(k(p-1)) = 1 (mod p)
# GCD(2**(B!) - 1, n) > 1
def Pollard(n):
    a = 2
    b = 2
    while True:
        a = pow(a, b, n)
        d = gcd(a-1, n)
        if 1<d<n: return d  # p = d
        b += 1