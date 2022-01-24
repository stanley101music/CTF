def Double_and_Add(d, P):
    bits = bin(d)[2:]
    Q = 0
    for bit in bits:
        Q = Q + Q
        if bit == '1':
            Q = Q + P
    return Q