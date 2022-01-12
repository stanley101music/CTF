flag = ""
flag_section = "3C190F1F3B2C3E034D4B1B0C1117160B595905"
for i in range(0, len(flag_section), 2):
    flag += chr(int(flag_section[i:i+2], 16) ^ 0x78)
print(flag)