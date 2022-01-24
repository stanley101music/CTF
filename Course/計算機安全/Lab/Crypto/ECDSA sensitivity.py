from ecdsa import SECP256k1
from ecdsa.ecdsa import *
from random import *

E = SECP256k1
G, n = E.generator, E.order
d = randrange(1, n)
pubkey = Public_key(G, d*G)
prikey = Private_key(pubkey, d)

h1 = 1
h2 = 2
k = randrange(1, n)
# Use same k
sig1 = prikey.sign(h1, k)
sig2 = prikey.sign(h2, k)
r1, s1 = sig1.r, sig1.s
r2, s2 = sig2.r, sig2.s
print(r1,s1)
print(r2,s2)

# s1*k1 = h1 + d*r1
# s2*k2 = h2 + d*r2
# k1 = k2 = k
# s1/s2 = (h1 + d*r1) / (h2 + d*r2)
# s1*h2 + d(s1*r2) = s2*h1 + d(s2*r1)
# d = (s1*h2 - s2*h1) / (s2*r1-s1*r2)
d_ans = (s1*h2 - s2*h1) * inverse_mod(s2*r1 - s1*r2, n) % n
print(d_ans, d)