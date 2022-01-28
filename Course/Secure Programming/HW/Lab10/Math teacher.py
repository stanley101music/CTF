from z3 import *
from pwn import *

ip = "ctf.balqs.nctu.me"
port = 9001
r = remote(ip,port)
a = r.recvline()
while a[0]!='f':
    a = a.replace('=', "==")
    b = r.recvline().replace('=', "==")

    x = Int('x')
    y = Int('y')
    s = Solver()
    s.add(eval(b))
    s.add(eval(a))
    assert s.check()==sat
    X = s.model()[x]
    Y = s.model()[y]

    print(X,Y)

    r.recvuntil(" = ")
    r.sendline(str(X))
    r.recvuntil(" = ")
    r.sendline(str(Y))
    a = r.recvline()

flag = a
print(flag)
#flag{y0u_93t_l0o_!n_m4th5}
