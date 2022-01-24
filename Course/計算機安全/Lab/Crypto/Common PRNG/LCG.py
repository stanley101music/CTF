# Break LCG
import random
class LCG():
    def __init__(self, seed):
        self.state = seed
        self.m = 2**32
        self.A = random.getrandbits(32) | 1 # Or 1 to make A odd
        self.B = random.getrandbits(32) | 1 # Or 1 to make B odd
    
    def getbits(self):
        self.clock()
        return self.state
    
    def clock(self):
        self.state = (self.A * self.state + self.B) % self.m
# Create LCG and three consecutive 32bits output
rng = LCG(42069)
print(rng.A, rng.B)
S = []
for i in range(3):
    S.append(rng.getbits())
# Solve A,B
from Crypto.Util.number import *
#S[1] = A*S[0] + B
#S[2] = A*S[1] + B
A = (S[1]-S[2]) * inverse(S[0]-S[1], rng.m) % rng.m
B = (S[1] - A*S[0]) % rng.m
print(A, B)