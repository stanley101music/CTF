import os

os.system('rm -f bait.txt.enc')

bait = open("./bait.txt", 'wb')
bait.write(2370 * b'\x00')
bait.close()

os.system('wannaSleep.exe bait.txt')

f_random = open('./bait.txt.enc', 'rb')
rand_table = f_random.read()

# read encrypted flag except last four bytes
f = open('./wannasleeeeeeep.txt.enc', 'rb')
flag_enc = f.read()
f.close()

# Decrypt
flag = ""
for i in range(len(flag_enc)):
    tmp = (flag_enc[i] ^ rand_table[i]) % 255
    flag += chr(tmp)

print(flag)
#FLAG{S0M3_PE0P13_WaNNaCry_3uT_1_JUsT_waNNaSl33p_aNd_waTCh_A_gr3aT_M0v13}