from math import *

# n = p*q = ((p+q)/2)**2 - ((p-q)/2)**2
# if |p-q| is small, then ((p-q)/2)**2 -> 0, and thus ((p+q)/2)**2 -> n
# (p+q)/2 -> sqrt(n)
# Guess (p+q)/2 start from ceil(sqrt(n)) until ((p-q)/2) is an integer
# a = (p+q)/2
# b2 = ((p-q)/2)**2 (True when isqrt(b2)**2 == b2)
def FermatFactor(n):
    a = ceil(sqrt((n)))
    b2 = a*a-n
    while not isqrt(b2)**2 == b2:
        a = a+1
        b2 = a*a-n
    # p, q
    return a+isqrt(b2), a-isqrt(b2)