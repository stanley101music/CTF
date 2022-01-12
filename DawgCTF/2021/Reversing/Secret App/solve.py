flag = ""
byte_417B50 = "3C190F1F3B2C3E034C0808270B0D084B0A274D4B1B0A1D0C05"
for i in range(0, len(byte_417B50), 2):
    flag += chr(int(byte_417B50[i:i+2], 16) ^ 0x78)
print(flag)