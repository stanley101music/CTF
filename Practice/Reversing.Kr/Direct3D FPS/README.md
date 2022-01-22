# Direct3D FPS
## Overview
* It's a game made by Direct3D
* As the name says, it's a FPS game while the moving speed is very slow and almost impossible to win the game by normal way
## String Analysis
* I find an interesting string "Game Clear!", so I assume that the function which reference to this string is the one that will be called when a user wins the game
* It's referenced in sub_4039C0
## Function Analysis
### sub_4039C0 (0x4039C0)
```c
result = dword_409194;
while ( *result != 1 )
{
    result += 132;
    if ( (signed int)result >= (signed int)&unk_40F8B4 )
    {
        MessageBoxA(hWnd, byte_407028, "Game Clear!", 0x40u);
        return (int *)SendMessageA(hWnd, 2u, 0, 0);
    }
}
```
* byte_407028 will contain the string when we win the game
* Unfortunately, this doesn't seem to be readable string<br>
  ![](../img/Direct3D%20FPS%20-%20byte_407028.png)
* After finding the cross-reference to this string, it turns out that there's another function which will modify the value of this string
### sub_403400 (0x403400)
```c
result = sub_403440();
if ( result != -1 )
{
    v2 = 132 * result;
    v3 = dword_409190[132 * result];
    if ( v3 > 0 )
    {
        dword_409190[v2] = v3 - 2;
    }
    else
    {
        dword_409194[v2] = 0;
        byte_407028[result] ^= byte_409184[v2 * 4];
    }
}
```
* It's doing xor with byte_409184, however, this time the value of byte_409184 is undefined
* Since there's no other function that will reference to byte_409184, I suppose that after it's initialized, the value won't change. Therefore, I use x32dbg to do the dynamic analysis and dump the value of this byte array. Moreover, due to the size of byte_409184 is much larger than the byte_407028, I'll dump 0x8000 bytes instead of the length of byte_407028
  * ```savedata "path/to/dump/bin", 1359184, 0x8000```
* After decryption, we'll get the string ```Congratulation~ Game Clear! Password is Thr3EDPr0m```
## Solution
* Decryption
  ```python
  #pseudo code
  for i in range(len(byte_407028)):
      flag[i] = byte_407028[i] ^ byte_409184[i*132*4]
  ```
## Flag
```Thr3EDPr0m```