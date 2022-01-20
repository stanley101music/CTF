import string

def func3_1(i):
    if i>64 and i<=90:
        i -= 13
        if i>64:
            v1 = 0
        else:
            v1 = 26
        i += v1
    if i>96 and i<=122:
        i -= 13
        if i>96:
            v2 = 0
        else:
            v2 = 26
        i += v2
    return i

def func3_2(i):
    if i>32 and i!=127:
        i -= 47
        if i>32:
            v1 = 0
        else:
            v1 = 94
        i += v1
    return i

printable_ascii = string.printable
target = "\"_9~Jb0!=A`G!06qfc8'_20uf6`2%7"
flag = ""
id = 0
while id < len(target):
    for c in printable_ascii:
        i = ord(c)
        i = func3_1(i)
        i = func3_2(i)
        if chr(i) == target[id]:
            flag += c
            id += 1
            break
print("DawgCTF{" + flag + "}")
