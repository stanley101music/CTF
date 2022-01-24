# The value of sigs are retrieved from solve.py
sigs = [
    (101592270260074658145623977883237672418190742501267920277876600330346018052321, 97583727553230797999500070790669919467950681294550164580851959821439923558681),
    (48410193469424499912842702267115557488850551082462840389713387039845191734023, 54005573389643090552674798105558022419666849188353643532574771895074168574318)
]
E = SECP256k1
G, n = E.generator, E.order

h1 = '0'
h2 = '1'
h1 = bytes_to_long(sha256(h1.encode()).digest())
h2 = bytes_to_long(sha256(h2.encode()).digest())
r1, s1, r2, s2 = sigs[0][0], sigs[0][1], sigs[1][0], sigs[1][1]
pad = int(md5(b'secret').hexdigest(), 16)
R = 2^128
prefix = (pad << 128)
inv_s1 = pow(s1,-1,n)
inv_r2 = pow(r2,-1,n)
t = (-inv_s1*s2*r1*inv_r2) % n
u = (inv_s1*r1*h2*inv_r2-inv_s1*h1+prefix-inv_s1*s2*r1*inv_r2*prefix) % n

L = matrix(QQ, [[n, 0, 0], [t, 1, 0], [u, 0, R]])
for i,(x,y,z) in enumerate(L.LLL()):
    if z == R:
        v = L.LLL()[i]
        break

k1 = -v[0]+prefix
k2 = v[1]+prefix
inv_r1 = pow(r1,-1,n)
d1 = (s1*k1-h1)*inverse_mod(r1,n) % n
d2 = (s2*k2-h2)*inverse_mod(r2,n) % n
assert d1==d2
d = int(d1)

pubkey = Public_key(G, d*G)
prikey = Private_key(pubkey, d)
msg = 'Kuruwa'
h = sha256(msg.encode()).digest()
k = int(md5(b'secret').hexdigest() + md5(long_to_bytes(d) + h).hexdigest(), 16)
# Check whether point P is equal to the value received from server
# If not then failed, reconnect to server and try next time
# Since this solution is not determined, the value calculated isn't always correct
# But the value has high probability to be correct, so just try out more
print(f'P = ({pubkey.point.x()}, {pubkey.point.y()})')
sig = prikey.sign(bytes_to_long(h), k)
print(f'({sig.r}, {sig.s})')
# FLAG{adfc9b68bd6ec6dbf6b3c9ddd46aafaea06a97ee}