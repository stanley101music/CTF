import random
import string
import hashlib

with open('plain.txt') as f:
    plain = f.read().strip()

charset = string.ascii_lowercase+string.digits+',. '
charset_idmap = {e: i for i, e in enumerate(charset)}
assert all(c in charset for c in plain)

ksz = 80
plain = [charset_idmap[c] for c in plain]
key = [24, 23, 30, 21, 12, 11, 12, 33, 9, 15, 37, 25, 20, 17, 36, 1, 26, 31, 35, 17, 20, 7, 2, 22, 15, 28, 25, 8, 4, 31, 29, 21, 25, 24, 19, 14, 32, 19, 16, 34, 27, 0, 28, 8, 21, 24, 21, 10, 21, 28, 4, 2, 6, 32, 20, 33, 11, 10, 36, 34, 31, 30, 28, 12, 10, 2, 19, 27, 38, 7, 0, 20, 29, 38, 27, 2, 21, 17, 1, 28]

def encrypt(plain, key):
    N, ksz = len(charset), len(key)
    return ''.join(charset[(c + key[i % ksz]) % N] for i, c in enumerate(plain))

enc = encrypt(plain, key)
y = "45d6ukumip,ppi9c8loq9lt89iz1mgdu22.w 6u.0tdhv02szkibnb0bk2b,mi,58bc9so 1.f8b,vs7 bdvznq6jrpa 99bz6n5ukbapc5mdg8ub9t7.77hg.1qbx32u4ytx,7nw89df3g04pw01goz2s8gu4jhewc3ss5qnxe6aq slhp50yc.w,1htje430 l5 x 0sjj76a23drbih7mt2qdf,10pbtb.hua,dbv3tbi203zzn3sy8ga7q,o349qwy0.8d5zeh,31x0ol0pain413 8iu,rbza2mkz,k9izl6gs6nju 2nbbbyf145d6ukocywcdrqti87dq9lt13g.0d5kb6267bvqo5d1m80 8,imqt5dc4r98kjdosc 5cgduj z"

if enc==y:
    print(True)
    print("real key:", key)