def Square_and_Multiply(x, y):
    if y==0: return 1
    k = Square_and_Multiply(x, y//2) ** 2
    return k*x if y&1 else k