# The value of ss is retrieved from the first output of nLFSR.py

F = GF(2^65)
FF.<x> = GF(2^64, modulus=F.fetch_int(0x1fd07d87ee65cb055))
poly = 0xaa0d3a677e1be0bf

def gf_step():
    global init_state
    init_state = init_state * (x^43)
    ret = init_state.integer_representation()
    return (ret >> 63) & 1

def step():
    global state
    out = state & 1
    state >>= 1
    if out:
        state ^^= poly
    return out
    

def random():
    for _ in range(42):
        step()
    return step()


ss = '1000111101101001111100111101000100111111111100000011010100000101'
seq = [int(c) for c in ss]

now_state = 1
total = []
for i in range(64):
    now = []
    now_state *= (x^43)
    for i in range(64):
        now_bit = x^i
        now_bit = now_bit * now_state
        now_bit = now_bit.integer_representation()
        now_bit = (now_bit >> 63) & 1
        now.append(now_bit)
    total.append(now)
M = Matrix(FF, total).T
seq = Matrix(FF, seq)
ret = seq * (M^-1)
ret = ret[0]

init_state = 0
for i in range(64):
    init_state += ret[i]*x^i

for i in range(64):
    gf_step()

with open('output.txt', 'w') as f:
    for i in range(300):
        f.write(str(gf_step()))