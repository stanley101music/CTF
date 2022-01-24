import os

# Delete encrypted file, otherwise the encryptor won't work
os.system('rm -f bait.txt.enc')

# Create bait file with keyword = Tene
# length = 1565(length of ciphertext) - 4(length of "Tene")
bait = open("./bait.txt", 'wb')
bait.write(b"Tene")
for i in range(1565-4-4):
    bait.write(b'\x00')
bait.close()

# Utilize the encryptor to encrypt our bait file
# It'll generate the encrypted file named as bait.txt.enc
os.system('wannaSleep_revenge.exe bait.txt')

# Calculate the random value 
# c[i] = f(rand_395) ^ f(rand_0x656E6554) ^  (p[i] + 0x20)
# f(rand_395) ^ f(rand_0x656E6554) = c[i] ^ (p[i] + 0x20)
f_plain = open('./bait.txt', 'rb')
plain = f_plain.read()

f_cipher = open('./bait.txt.enc', 'rb')
cipher = f_cipher.read()

rand_table = []
for i in range(len(plain)):
    tmp = cipher[i] ^ (plain[i] + 0x20)
    rand_table.append(tmp)

# read encrypted flag except last four bytes
f = open('./wannasleeeeeeep.txt.enc', 'rb')
flag_enc = f.read()[:-4]
f.close()

# Decrypt
flag = ""
for i in range(len(flag_enc)):
    tmp = (flag_enc[i] ^ rand_table[i]) % 255 - 0x20
    flag += chr(tmp)

print(flag)
#FLAG{Oh____x0r_RaNs0mwAr3?_Th1s_mAn_mUst_Rea11y_wAnnAsl33p_QQ}