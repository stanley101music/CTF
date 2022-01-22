# Easy Keygen
## Overview
* 32-bit PE file
* The symbols aren't stripped, so we can see the main function is at 0x401000
* The program will ask for user's input twice, one for the Name and one for the Serial
* According to [Readme.txt](./ReadMe.txt), we need to find a Name that matches ```5B134977135E7D13```
## Function Analysis
### main (0x401000)
* After taking our input as Name, it'll do the encryption and the result is the corresponding value of Serial
* Encryption Algorithm
  ```c
  v6 = [16, 32, 48]
  for ( i = 0; i < strlen(&Name); ++i )
  {
    sprintf(&Serial, "%s%02X", &Serial, Name[i] ^ v6[i%3] );
  }
  ```
  * So it's a like a Vigenere cipher where key = [16, 32, 48]
## Solution
* Decryption
  ```python
    Serial = [0x5B, 0x13, 0x49, 0x77, 0x13, 0x5E, 0x7D, 0x13]
    key = [16, 32, 48]
    flag = ""
    for i in range(len(Serial)):
        flag += chr(Serial[i] ^ key[i%3])
    print(flag)
  ```
## Flag
```K3yg3nm3```