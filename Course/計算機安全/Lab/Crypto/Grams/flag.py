import string
import hashlib
from binascii import *

charset = string.ascii_lowercase+string.digits+',. '
charset_idmap = {e: i for i, e in enumerate(charset)}

with open('./output.txt') as f:
    ctx = f.readline().strip()[4:]
    enc = bytes.fromhex(f.readline().strip()[6:])

ksz = 80
key = [24, 23, 30, 21, 12, 11, 12, 33, 9, 15, 37, 25, 20, 17, 36, 1, 26, 31, 35, 17, 20, 7, 2, 22, 15, 28, 25, 8, 4, 31, 29, 21, 25, 24, 19, 14, 32, 19, 16, 34, 27, 0, 28, 8, 21, 24, 21, 10, 21, 28, 4, 2, 6, 32, 20, 33, 11, 10, 36, 34, 31, 30, 28, 12, 10, 2, 19, 27, 38, 7, 0, 20, 29, 38, 27, 2, 21, 17, 1, 28]
k = hashlib.sha512(''.join(charset[k] for k in key).encode('ascii')).digest()
flag = bytes(ci ^ ki for ci, ki in zip(enc.ljust(len(k), b'\0'), k))
print(unhexlify(flag.hex()))
# FLAG{3c7166f852e3eaed71c81875e0c290562eff2c0}