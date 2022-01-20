flag = ""
byte_417B40 = "274C35554B014B470507"
byte_417B30 = "3C190F1F3B2C3E03102D"
for i in range(0, len(byte_417B30), 2):
    flag += chr(int(byte_417B30[i:i+2], 16) ^ 0x78)
for i in range(0, len(byte_417B40), 2):
    flag += chr(int(byte_417B40[i:i+2], 16) ^ 0x78)
print(flag)