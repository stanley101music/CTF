from math import ceil, sqrt
import gmpy2
from Crypto.Util.number import isPrime, getPrime, inverse
from Crypto.PublicKey import RSA
from fractions import gcd

def genkey():
    # choose p, q, e
    p, e = getPrime(32), 65537
    q = p + 1000
    while True:
        q += 1
        if isPrime(q):
            break
    # calculate d
    n = p * q
    phi = (p - 1) * (q - 1)
    d = inverse(e, phi)
    # return publicKey, privateKey
    return (n, e), (n, d)

def enc(m, public):
    n, e = public
    return pow(m, e, n)

def dec(c, private):
    n, d = private
    print(c, d, n)
    return pow(c, d, n)

# transform flag to cipherText
with open('flag', 'r') as data:
    flag = data.read()
mes = ''
for i in flag:
    mes += hex(ord(i))[2:]

pub, pri = genkey()
cipher = [enc(int(mes[i*16 : (i+1)*16], 16), pub) for i in range(4)]

# store cipherText
with open('cipher', 'w') as data:
    for c in cipher:
        data.write(str(c) + '\n')
        
# store publicKey
public = RSA.construct((pub[0], pub[1]))
with open('pub.pem', 'wb') as data:
    data.write(public.exportKey('PEM'))
