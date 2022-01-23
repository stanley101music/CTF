res = -1536092243306511225
overflow = 1<<64
mod = 26729
mul = 1
while True:
    if (mul*overflow + res) % mod:
        mul += 1
    else:
        print(mul)
        flag = (mul*overflow + res) // mod
        print(flag)
        break
# Convert unsigned int to 64-bit signed int
while flag>=0:
    flag -= overflow
print(flag)