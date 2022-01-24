dword_403040 = [31, 3, 20, 24, 46, 3, 36, 13, 59, 112, 7, 111, 30, 15, 18, 23, 36, 32, 59, 6, 11, 100, 22, 13, 116, 12, 27, 124, 99, 30, 19, 96, 127, 120, 127, 101, 100, 101, 126, 108, 108, 98, 98, 118, 58]
off_403020 = "YOU_USE_HAIYA_WHEn_YOU'RE_DISAPPOINTED_MMSSGG"
flag = ""
for a,b in zip(dword_403040, off_403020):
	flag += chr(a^ord(b))
print(flag)