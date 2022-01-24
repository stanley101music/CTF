# Polig-Hellman
from sage.groups.generic import bsgs

g = 2
n = 22975024372641088191783192950030840455936651367831116706532074148973552639475113523713622342956112126457710740633725263638116108451282253328304547
c = 3391562491073162069780474526700107230909189849786338234577033763865425503028855096698198069367193995675035849507973902223745251492606324520756666
flag = bytes.fromhex('c401549a04656914f9288164f6298ccc09771d8805db7248e3162b86237cefd2621df96509d8d9f32dbd2f56c6c41414971b990f31f80ced0cfe4eac89f55a93')
f = factor(n-1)

x_list = []
f_list = []

l = len(f)
for i in range(0, l):
    fi = f[i][0]
    gi = pow(g, (n-1)//fi, n)
    hi = pow(c, (n-1)//fi, n)
    xi = bsgs(gi, hi, (0,fi))
    x_list.append(xi)
    f_list.append(fi)
k = crt(x_list, f_list)

k = hashlib.sha512(str(k).encode('ascii')).digest()
m = bytes(ci ^ ki for ci, ki in zip(flag.ljust(len(k), b'\0'), k))
print(m)