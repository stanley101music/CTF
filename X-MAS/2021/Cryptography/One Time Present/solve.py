from pwn import *

r = remote("challs.xmas.htsp.ro", 1037)
r.recvuntil(b"Awaiting your input: ")
flag = ""
byte_sets = [set() for _ in range(0x4d)]

while not all(len(b) == 255 for b in byte_sets):
    r.sendline(b'')
    c = r.recvuntil(b"Awaiting your input: ").decode().split("\n")[0]
    for i, byte in enumerate(bytes.fromhex(c)):
        byte_sets[i].add(byte)


all_possible_bytes = set(range(256))
for b in byte_sets:
    missing_byte = list(all_possible_bytes -  b)
    flag += chr(missing_byte[0])

print(flag)