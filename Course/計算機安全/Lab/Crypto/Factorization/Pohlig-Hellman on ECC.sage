# Pohlig-Hellman on ECC
from sage.groups.generic import bsgs

p = 0x33f572d89d3f3321fe9e8f7598b77397
a = 0x2154f22abc2c979dc891974c4f4b32a8
b = 0x14a02aa038a24f27bd100bb701188be2
gx = 0x30712985d4dca5dbf45b44c9d1e3d95b
gy = 0x08bd79a5b13f1e710e6c4765c36f68a6

E = EllipticCurve(GF(p), [a,b])
G = E(gx, gy)
d = randrange(p)
P = d*G
# G.order() ~= p
# 2293304381 * 2397946457 * 2968041289 * 4231431697 -> smooth order
f = factor(G.order())
f = [fi[0] for fi in f]

# Given G and P, solve d
n = G.order()
d = []
for fi in f:
    Gi = (n//fi) * G
    Pi = (n//fi) * P
    # Built-in package for calculating discrete log
    # di = discrete_log(Pi, Gi, operation='+')
    di = bsgs(Gi, Pi, operation='+', bounds=(0, fi))
    d.append(di)
d = crt(d, f)
print(P, d*G)