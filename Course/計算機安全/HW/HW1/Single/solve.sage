from collections import namedtuple
from Crypto.Util.number import inverse, bytes_to_long
import hashlib
import random

Point = namedtuple("Point", "x y")
O = 'INFINITY'

def is_on_curve(P):
    if P == O:
        return True
    else:
        return (P.y**2 - (P.x**3 + a*P.x + b)) % p == 0 and 0 <= P.x < p and 0 <= P.y < p

def point_inverse(P):
    if P == O:
        return P
    return Point(P.x, -P.y % p)

def point_addition(P, Q):
    if P == O:
        return Q
    elif Q == O:
        return P
    elif Q == point_inverse(P):
        return O
    else:
        if P == Q:
            s = (3*P.x**2 + a)*inverse(2*P.y, p) % p
        else:
            s = (Q.y - P.y) * inverse((Q.x - P.x), p) % p
    Rx = (s**2 - P.x - Q.x) % p
    Ry = (s*(P.x - Rx) - P.y) % p
    R = Point(Rx, Ry)
    assert is_on_curve(R)
    return R

def point_multiply(P, d):
    bits = bin(d)[2:]
    Q = O
    for bit in bits:
        Q = point_addition(Q, Q)
        if bit == '1':
            Q = point_addition(Q, P)
    assert is_on_curve(Q)
    return Q

def is_singular(a,b,p):
    if (-16*(4*(a^3)+27*(b^2)))%p==0:
        return True
    return False

p = 9631668579539701602760432524602953084395033948174466686285759025897298205383
x1 = 3829488417236560785272607696709023677752676859512573328792921651640651429215
y1 = 7947434117984861166834877190207950006170738405923358235762824894524937052000
x2 = 9587224500151531060103223864145463144550060225196219072827570145340119297428
y2 = 2527809441042103520997737454058469252175392602635610992457770946515371529908
gx = 5664314881801362353989790109530444623032842167510027140490832957430741393367
gy = 3735011281298930501441332016708219762942193860515094934964869027614672869355
G = (gx, gy)

# Solve ECC parameters a and b
F = GF(p)
R.<a,b> = PolynomialRing(F)
Id = Ideal(y1^2-x1^3-a*x1-b, y2^2-x2^3-a*x2-b)
a, b = Id.variety()[0]['a'], Id.variety()[0]['b']

# Check singular curve
assert is_singular(a, b, p)

# Convert ECC to Node
P.<x> = GF(p)[]
f = x^3 + a*x + b
A = (x1, y1)
B = (x2, y2)
print(f.factor()) 
# (x + 1706485822346415641443806104662801825943914230110363749830437374602647864828) * (x + 8778425668366493782038529472271552171423076833119284811370540338595974272969)^2
alpha = -8778425668366493782038529472271552171423076833119284811370540338595974272969
beta = -1706485822346415641443806104662801825943914230110363749830437374602647864828
f_ = f.subs(x=x+alpha)
print(f_.factor())
# (x + 2559728733519623462165709156994202738915871345165545624745656061903971797242) * x^2
G_ = (G[0] - alpha, G[1])
A_ = (A[0] - alpha, A[1])
B_ = (B[0] - alpha, B[1])
t = GF(p)(2559728733519623462165709156994202738915871345165545624745656061903971797242).square_root()
u = (G_[1] + t*G_[0])/(G_[1] - t*G_[0]) % p
v = (A_[1] + t*A_[0])/(A_[1] - t*A_[0]) % p
w = (B_[1] + t*B_[0])/(B_[1] - t*B_[0]) % p
dA = v.log(u)
dB = w.log(u)

# Decryption
A = Point(x=x1, y=y1)
B = Point(x=x2, y=y2)
k = point_multiply(B, dA).x
k = hashlib.sha512(str(k).encode('ascii')).digest()
ENC = bytes.fromhex('1536c5b019bd24ddf9fc50de28828f727190ff121b709a6c63c4f823ec31780ad30d219f07a8c419c7afcdce900b6e89b37b18b6daede22e5445eb98f3ca2e40')
flag = bytes(ci ^ ki for ci, ki in zip(ENC.ljust(len(k), b'\0'), k))
print('flag =', flag)
# FLAG{adbffefdb46a99fad0042dd3c10fdc414fadd25c}