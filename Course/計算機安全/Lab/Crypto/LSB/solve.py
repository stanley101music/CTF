from pwn import *
from Crypto.Util.number import *

r = remote('edu-ctf.csie.org', 42071)

q = r.recvline()
n = int(q[4:])
q = r.recvline()
c = int(q[4:])
e = 65537
# a is modular multiplicative inverse of 3
inv_3 = inverse(3, n)
# counts number of consecutive 0's
cnt = 0
i = 0
b = 0
m = 0

while True:
    # send inv_3 * 0,1,2... * c % n
    # the return value can help us get the least, second least, third least, ... significant bits of m 
    r.sendline(str(pow(inv_3,i*e,n)*c%n).encode())
    q = r.recvline()
    response = int(q.split()[-1])
    mm = (response - (inv_3*b%n)) % 3
    if mm == 0:
        cnt += 1
        if cnt == 10:
            break
    else:
        cnt = 0
    b = (inv_3*b + mm) % n
    m = 3**i*mm+m
    i += 1

print(m)
print(long_to_bytes(m))
# FLAG{fcf8ab2bc7b42bbd00e5be2b3d311ec6e8a89526}