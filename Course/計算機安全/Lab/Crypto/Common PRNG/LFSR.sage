# Break LFSR key
# Output need not to be consecutive
# m individual output is enough to solve
class LFSR:
    # key: state = s[0]~s[d-1]
    # taps: connected wire
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
        
key = [1,0,1]
taps = [3,2] # Start from right to left, [3,2] implies there are wires on x^0(3) and x^1(2)
rng = LFSR(key,taps)
for _ in range(20):
    rng.getbit()

for _ in range(3):
    print(rng.getbit())

F.<x> = PolynomialRing(GF(2))
P = x^3 + x + 1
C = companion_matrix(P, format='bottom')

# C^19*key = [0,0,1]
# Ax = b
b = vector([0,0,1])
A = C^19
x = A^-1*b
print(x)