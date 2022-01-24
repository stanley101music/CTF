import itertools
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random.random import getrandbits

class LFSR:
    def __init__(self, key, taps):
        d = max(taps)
        assert len(key) == d, "Error: key of wrong size."
        self._s = key
        self._t = [d - t for t in taps]

    def _sum(self, L):
        s = 0
        for x in L:
            s ^= x
        return s

    def _clock(self):
        b = self._s[0]
        self._s = self._s[1:] + [self._sum(self._s[p] for p in self._t)]
        return b

    def getbit(self):
        return self._clock()

class Geffe:
    def __init__(self, key):
        #assert key.bit_length() <= 19 + 23 + 27 # shard up 69+ bit key for 3 separate lfsrs
        #key = [int(i) for i in list("{:069b}".format(key))] # convert int to list of bits
        self.LFSR = [
            LFSR(key[:19], [19, 18, 17, 14]),
            LFSR(key[19:46], [27, 26, 25, 22]),
            LFSR(key[46:], [23, 22, 20, 18]),
        ]

    def getbit(self):
        b = [lfsr.getbit() for lfsr in self.LFSR]
        return b[1] if b[0] else b[2]

stream = [0, 1, 1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1, 1, 0, 0, 1, 0, 1, 1, 0, 0, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 1, 0, 0, 1, 0, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 0, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0, 1, 0, 1, 1, 0, 0, 0, 1, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1]
# First, break LFSR(key[19:46], [27, 26, 25, 22])
key_len = 27
# b represents how many bits to be modified
find = False
for b in range(key_len):
    # Use combinations to decide which b bits are modified
    for c in itertools.combinations(range(key_len), b):
        key_candidate = [1 - stream[i] if i in c else stream[i] for i in range(key_len)]
        lfsr = LFSR(key_candidate, [27,26,25,22])
        # s is the output of key_candidate
        s = [lfsr.getbit() for _ in range(256)]
        matches = sum(a==b for a,b in zip(stream, s))
        if matches >= 180: # 256*0.75 (approximately)
            b1 = key_candidate
            find = True
            break
    if find:
        break
# [0, 1, 1, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 1, 0, 1]

# Second, break LFSR(key[46:], [23, 22, 20, 18])
key_len = 23
# b represents how many bits to be modified
find = False
for b in range(key_len):
    # Use combinations to decide which b bits are modified
    for c in itertools.combinations(range(key_len), b):
        key_candidate = [1 - stream[i] if i in c else stream[i] for i in range(key_len)]
        lfsr = LFSR(key_candidate, [23, 22, 20, 18])
        # s is the output of key_candidate
        s = [lfsr.getbit() for _ in range(256)]
        matches = sum(a==b for a,b in zip(stream, s))
        if matches >= 180: # 256*0.75 (approximately)
            b2 = key_candidate
            find = True
            break
    if find:
        break
# [0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1]

# b1 = [0, 1, 1, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 1, 0, 1]
# b2 = [0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1]
# Brute force b0
for i in range(0,2**19):
    tmp = bin(i)[2:].rjust(19, '0')
    b0 = [int(c) for c in tmp]
    key = b0 + b1 + b2
    J = Geffe(key)
    test = [J.getbit() for _ in range(256)]
    if test == stream:
        print("Success:",key)
        break
# Success: [1, 0, 0, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1]

# Convert key to integer from bits
#key = [1, 0, 0, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1]
key = int(''.join(str(c) for c in key), 2)
# AES decryption
def decrypt_flag(key, ct):
    sha1 = hashlib.sha1()
    sha1.update(str(key).encode('ascii'))
    key = sha1.digest()[:16]
    iv = bytes.fromhex('cd2832f408d1d973be28b66b133a0b5f')
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = unpad(cipher.decrypt(ct), 16)
    
    return plaintext

ct = bytes.fromhex('1e3c272c4d9693580659218739e9adace2c5daf98062cf892cf6a9d0fc465671f8cd70a139b384836637c131217643c1')
print(decrypt_flag(key, ct))
# FLAG{941ae21eb8823b73973fc67ccbf89ce9fb4cd38c}