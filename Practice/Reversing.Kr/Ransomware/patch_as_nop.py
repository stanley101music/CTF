import idautils
NOP = 0x90
start = 0x4135E6
end = 0x44A775
for ins in range(start, end, 1):
    patch_byte(ins, NOP)