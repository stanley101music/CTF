# Coppersmith’s Method on RSA
p = random_prime(2^512)
q = random_prime(2^512)
n=p*q
x0 = randrange(1, 2^128)
pad = randrange(1, 2^888)
m = (pad << 128) + x0
assert m<n
c = pow(m, 3, n)
print(pad, c)

R = 2^128
a = (pad << 128)
L = matrix(ZZ, [[R^3, 3*a*R^2, 3*a^2*R, a^3-c], [0, n*R^2, 0, 0], [0, 0, n*R, 0], [0, 0, 0, n]])
v = L.LLL()[0]
print(v)

F.<x> = PolynomialRing(ZZ)
Q = v[0]//R^3*x^3 + v[1]//R^2*x^2 + v[2]//R*x + v[3]
print(Q)
assert Q.roots()[0][0] == x0

# Use built-in function
G.<y> = PolynomialRing(Zmod(n))
g = (a+y)^3-c
# X is the upper bound = R
assert g.small_roots(X=2^128)[0] == x0

# Calculate value of p if knowing some high bits of p
a = (p>>200)<<200
x0 = p%(2^200)
F.<x> = PolynomialRing(Zmod(n))
f = a+x
# beta = beta in Howgrave-Graham
# Originally it should be 0.5, but maybe p is smaller than q
# So need to be fine-grained
assert f.small_roots(X=2^200, beta=0.4) == x0