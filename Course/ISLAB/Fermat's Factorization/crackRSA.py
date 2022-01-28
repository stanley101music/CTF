from math import ceil, sqrt
import gmpy2
from Crypto.Util.number import isPrime, getPrime, inverse
from Crypto.PublicKey import RSA
from fractions import gcd
import base64

def fermat(n):
	a = ceil(sqrt(n))
	b2 = a * a - n
	while not gmpy2.iroot(b2, 2)[1]:
		a = a + 1
		b2 = a * a -n
	b = gmpy2.iroot(b2, 2)[0]
	return [a + b, a - b]

if __name__ == "__main__":
    
    #file = open("pub.pem", "rb")
    #data = file.read()
    #file.close()
    
    public = RSA.importKey(open('pub.pem').read())
    N = public.n

    (p, q) = fermat(N)
    print("p = %d, q = %d"%(p, q))
