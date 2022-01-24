from Crypto.Util.number import *

# Generate public/private key
p = getPrime(256)
q = getPrime(256)
n = p*q
phi = (p-1)*(q-1)
e = 65537
d = inverse(e, phi)
print(e, n)
print(d)

# Encryption
m = 69420
c = pow(m, e, n)
print(c)

# Decryption
m = pow(c, d, n)
print(m)