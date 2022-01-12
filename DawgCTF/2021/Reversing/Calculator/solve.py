flag = ""
byte_417B30 = "3C190F1F3B2C3E031B4C341B2D494C2C480A274E4C05"
for i in range(0, len(byte_417B30), 2):
    flag += chr(int(byte_417B30[i:i+2], 16) ^ 0x78)
print(flag)