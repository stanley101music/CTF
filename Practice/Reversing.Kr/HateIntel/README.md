# HateIntel
## Overview
* ARM
## Function Analysis
### sub_2224 (0x2224)
* This is the main function
* You can find this function either by searching for words like "Correct" or "Wrong", or simply follow the control flow from the entry function at 0x2000
* program logic
  * Take user's input as key
  * Encrypt the key
  * Output "Correct" if the encrypted key is identical to byte_3004
### encrypt_232C (0x232C)
* Encryption
* It consists a sub function sub_2494(0x2494)
* I'm going to simplify the entire process
  ```python
  for i in range(len(key)):
      for j in range(4):
          key[i] <<= 1
          if key[i] & 0x100:
              key[i] |= 1
  ```
  * The inner loop can be interpreted as left rotation, since the size of an ```unsigned __int8``` as 1 byte, and thus the maximum value is 0xff. If ```key[i]&0x100``` is true, that means ```key[i]<<1``` is larger than the size of ```unsigned _int8``` and cause overflow, so the left most bit is automatically ignored, but by applying ```| 1``` we can consider it as moving the left most bit to the right most bit
  ```python
  for i in range(len(key)):
      RotateLeft(key[i], 4)
  ```
* To decrypt it, we have to rotate the cipher right 4 bits
## Flag
```Do_u_like_ARM_instructi0n?:)```