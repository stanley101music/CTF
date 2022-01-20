import math
from pwn import *

def isPerfectSquare(n):
    sqrt = int(math.sqrt(n))
    return sqrt**2 == n

def isFibonacci(n):
    return isPerfectSquare(5*(n**2) + 4) or isPerfectSquare(5*(n**2) - 4)

r = remote('umbccd.io', 6000)

while 1:
    try:
        r.recvuntil(b'[')
        arr = r.recvlineS().strip('\n').strip(']')
        nums = arr.split(',')
        for n in nums:
            if isFibonacci(int(n)):
                r.sendline(str(n))
                break
        r.recv()
    except:
        print(r.recv())
r.close()