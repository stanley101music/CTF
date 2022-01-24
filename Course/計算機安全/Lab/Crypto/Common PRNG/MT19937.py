# Break MT19937 (Python's default RNG)
# Knowing 624 consecutive 32bits output is enough to break MT19937
def _int32(x):
    return int(0xFFFFFFFF & x)

class MT19937:
    def __init__(self, seed):
        self.mt = [0] * 624 # One state include 624 32bits numbers
        self.mt[0] = seed # Seed saved in state's first number
        self.mti = 0
        for i in range(1, 624):
            self.mt[i] = _int32(1812433253 * (self.mt[i - 1] ^ self.mt[i - 1] >> 30) + i)

    # Output != state
    # Invertible
    def extract_number(self): 
        if self.mti == 0:
            self.twist()
        y = self.mt[self.mti]
        y = y ^ y >> 11
        y = y ^ y << 7 & 2636928640
        y = y ^ y << 15 & 4022730752
        y = y ^ y >> 18
        self.mti = (self.mti + 1) % 624
        return _int32(y)
    
    # Similar to clock in LCG
    # Update 624 numbers once
    # Invertible
    # mt[i+624] = f(mt[i], mt[i+1], mt[i+397])
    def twist(self):
        for i in range(0, 624):
            y = _int32((self.mt[i] & 0x80000000) + (self.mt[(i + 1) % 624] & 0x7fffffff))
            self.mt[i] = (y >> 1) ^ self.mt[(i + 397) % 624]

            if y % 2 != 0:
                self.mt[i] = self.mt[i] ^ 0x9908b0df

# Use rnadcrack to simulate python's rng state and predict
from randcrack import RandCrack
import random
rc = RandCrack()
for _ in range(624):
    rc.submit(random.getrandbits(32))

for _ in range(32):
    print(rc.predict_randrange(2**64))
    print(random.randrange(2**64))
    print()