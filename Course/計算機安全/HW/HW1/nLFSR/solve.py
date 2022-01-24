# The output of result is used as value of seq in nLFSR.sage
# The manual input is the output of nLFSR.sage
from pwn import *

r = remote('edu-ctf.csie.org', 42069)

prev = 1.2
result = ''
x = 0
predict = ''
idx = 0
while prev:
    if predict:
        x = int(predict[idx])
        idx += 1
    r.recv()
    r.sendline(str(x))
    money = float(r.recvlineS().strip())
    print(money)
    if money>2.4:
        flag = r.recv()
        print(flag)
        break
    if money<prev:
        result += str(1-x)
    else:
        result += str(x)
    if len(result)>=64:
        print(result)
        if not predict:
            predict += input('> ')
    prev = money
# FLAG{2iroO742LwA2ES1Cwewx}