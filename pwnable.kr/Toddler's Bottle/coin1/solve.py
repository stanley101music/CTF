from pwn import *
import time

r = remote('pwnable.kr', 9007)

r.recvuntil(b'- Ready? starting in 3 sec... -\n\t\n')
for i in range(100):
    N, C = r.recvlineS().strip().split(' ')
    N = int(N.split('=')[-1])
    C = int(C.split('=')[-1])

    start, end = 0, N-1
    while start<=end and C>0:
        mid = (start+end)//2
        query = " ".join([str(j) for j in range(start, mid+1)])
        r.sendline(query.encode(encoding="utf-8"))

        result = int(r.recvlineS().strip())
        if result%10==0:
            start = mid + 1
        else:
            end = mid-1
        C -= 1
    while C>0:
        r.sendline(b'0')
        r.recvline()
        C -= 1
    r.sendline(str(start).encode(encoding="utf-8"))
    r.recvline()
print(r.recv())
r.close()