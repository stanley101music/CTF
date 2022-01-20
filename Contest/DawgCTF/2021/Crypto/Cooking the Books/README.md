# Cooking the Books (100)

### Description
> If it's from GCHQ why do they call it the Swiss Army Knife??
> 
> #)%|&Ap*!dq$#h8h:!xhx)7_)b_x:5!Cq:;>I4(;`4x4b6Il

### Tool
* [CyberChef](https://gchq.github.io/CyberChef/#recipe=ROT47(47)Bifid_Cipher_Decode('')Rail_Fence_Cipher_Decode(2,0)From_Base64('A-Za-z0-9%2B/%3D',true)&input=IyklfCZBcCohZHEkI2g4aDoheGh4KTdfKWJfeDo1IUNxOjs%2BSTQoO2A0eDRiNkls)

### Solution
1. ROT47
    * RXTMUpAYP5BSR9g9iPI9IXf0X30IidPrBijmxcWj1cIc3ex=
2. [Bifid Cipher](https://en.wikipedia.org/wiki/Bifid_cipher)
    * RFZNRtMIQ5YNZ9d9bVR9MYc0G30UnqHkGfjsmyFj1sFu3zn=
3. [Rail Fence Cipher](https://en.wikipedia.org/wiki/Rail_fence_cipher)
    * Key = 2
    * RGF3Z0NURntqMHIkQG5fYjNsZm9ydF9jb1VsRF9uM3Yzcn0=
4. Base64

### Flag
```
DawgCTF{j0r$@n_b3lfort_coUlD_n3v3r}
```
