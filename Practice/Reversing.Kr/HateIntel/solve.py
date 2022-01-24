cipher = [
  0x44, 0xF6, 0xF5, 0x57, 0xF5, 0xC6, 0x96, 0xB6, 0x56, 0xF5, 
  0x14, 0x25, 0xD4, 0xF5, 0x96, 0xE6, 0x37, 0x47, 0x27, 0x57, 
  0x36, 0x47, 0x96, 0x03, 0xE6, 0xF3, 0xA3, 0x92, 0x00
]

def ror(n, l):
    binary = bin(n)[2:].rjust(8,'0')
    return int(binary[-l:]+binary[:l], 2)

flag = ""
for c in cipher:
    flag += chr(ror(c,4))
print(flag)