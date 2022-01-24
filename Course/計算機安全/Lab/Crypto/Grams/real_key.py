import string

charset = string.ascii_lowercase+string.digits+',. '
charset_idmap = {e: i for i, e in enumerate(charset)}

with open('./output.txt') as f:
    ctx = f.readline().strip()[4:]
    enc = bytes.fromhex(f.readline().strip()[6:])
ctx = [charset_idmap[c] for c in ctx]

with open('./plain.txt') as f:
    ptx = f.readline().strip()
ptx = [charset_idmap[c] for c in ptx]

N = len(charset)
keys = []
for i in range(80):
    keys.append((ctx[i] - ptx[i]) % N)
print(keys)