from pwn import *
from random import randint
from Crypto.Util.number import *
from hashlib import sha256
from ecdsa import SECP256k1
from ecdsa.ecdsa import Public_key, Private_key, Signature
from ecdsa.ellipticcurve import PointJacobi


r = remote('edu-ctf.csie.org', 42072)
#r = process('./server.py')
x,y = r.recvlineS().strip().split('=')[-1].split(',')
x = int(x[2:])
y = int(y[1:-1])

# Prepare Curve
E = SECP256k1
G, n = E.generator, E.order

h1 = '1'
h2 = '2'
# Send first chosen plaintext
r.recv()
r.sendline('1')
r.recv()
r.sendline(h1)
r1,s1 = r.recvlineS().strip().split('=')[-1].split(',')
r1 = int(r1[2:])
s1 = int(s1[1:-1])
# Send second chosen plaintext
r.recv()
r.sendline('1')
r.recv()
r.sendline(h2)
r2,s2 = r.recvlineS().strip().split('=')[-1].split(',')
r2 = int(r2[2:])
s2 = int(s2[1:-1])

# Calculate private key d (reuse of same key k)
# s1*k1 = h1 + d*r1
# s2*k2 = h2 + d*r2
# k2 = k1 * 1337 % n
# s2*k2 = s2*k1*1337
# s1/(s2*1337) = (h1 + d*r1) / (h2 + d*r2)
# s1*h2 + d(s1*r2) = s2*1337*h1 + d(s2*1337*r1)
# d = (s1*h2 - s2*1337*h1) / (s2*1337*r1-s1*r2)
h1 = bytes_to_long(sha256(h1.encode()).digest())
h2 = bytes_to_long(sha256(h2.encode()).digest())
d = (s1*h2 - s2*1337*h1) * inverse_mod(s2*1337*r1 - s1*r2, n) % n
# Calculate k1, k2 and verify
k1 = (h1 + d*r1) * inverse_mod(s1, n) % n
k2 = (h2 + d*r2) * inverse_mod(s2, n) % n
assert k2==k1*1337%n

# Prepare public and private key
pubkey = Public_key(G, d*G)
prikey = Private_key(pubkey, d)

# Calculate signature of input 'Kuruwa'
msg = 'Kuruwa'
h = sha256(msg.encode()).digest()
k = k2 * 1337 % n
sig = prikey.sign(bytes_to_long(h), k)

# Send Answer
r.recv()
r.sendline('2')
r.recv()
r.sendline('Kuruwa')
r.recv()
r.sendline(str(sig.r))
r.recv()
r.sendline(str(sig.s))
flag = r.recv()
print(flag)
# FLAG{fcf8ab2bc7b42bbd00e5be2b3d311ec6e8a89526}