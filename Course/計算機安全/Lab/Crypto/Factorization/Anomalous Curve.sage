# Anomalous Curve -> G.order() == p
p = 0xaaf4fc08c0a4c43196ac415654e95917
a = 0x471e7a16295fe52d0b802ed6465ca3d8
b = 0x97340d156e5d5eac4306510073709e6f

E = EllipticCurve(GF(p), [a,b])
G = E(0x52cca8dd35776fd16e8ea2d30060568a, 0x19a50c074614504510a35383eec1228a)
assert p==G.order()

# Calculate slope of point P and Q
def spq(P, Q):
    if P[2]==0 or Q[2]==0 or P==-Q:
        return 0
    if P==Q:
        a = P.curve().a4()
        # tangent line
        return (3*P[0]^2+a)/(2*P[1])
    return (P[1]-Q[1])/(P[0]-Q[0])

# Augmented Point Addition
def add_augmented(PP, QQ):
    (P,u), (Q,v) = PP, QQ
    return [P+Q, u+v+spq(P, Q)]

def scalar_mult(n, PP):
    bits = bin(n)[2:]
    TT = PP.copy()
    for bit in bits[1:]:
        TT = add_augmented(TT, TT)
        if bit == '1':
            TT = add_augmented(TT, PP)
    return TT

def solve_ecdlp(P,Q,p):
    R1, alpha = scalar_mult(p, [P,0])
    R1, beta = scalar_mult(p, [Q,0])
    return ZZ(beta*alpha^(-1))

d = randrange(p)
P = d*G
assert solve_ecdlp(G, P, p)==d