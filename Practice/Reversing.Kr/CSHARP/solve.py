import base64
key = [16, 51, 17, 33, 17, 144, 68, 102, 181, 160, 238, 51]
cipher = [74, 70, 87, 77, 44, 241, 29, 49, 226, 238, 163, 117]
index_order = [0, 3, 1, 2, 11, 8, 4, 5, 9, 7, 10, 6]
plain = [0]*12

for c,k,idx in zip(cipher, key, index_order):
    plain[idx] = chr(c^k)

flag = base64.b64decode(''.join(plain))
print(flag)