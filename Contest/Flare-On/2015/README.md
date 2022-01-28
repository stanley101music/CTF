# Flare-on 2015 writeup
* [Download challenges](https://flare-on.com/files/2015_FLAREOn_Challenges.zip)
* [Official writeup](https://www.fireeye.com/blog/threat-research/2015/09/flare-on_challenges.html)
## C1
### Process Analysis
* Users can type in the password, If the password is wrong, it'll output "You are failure"<br>
  ![](img/C1%20-%20start.png)
### Function Analysis
```c
BOOL start()
{
  HANDLE stdin; // ST18_4
  int i; // ecx
  HANDLE stdout; // [esp+8h] [ebp-8h]
  DWORD NumberOfBytesWritten; // [esp+Ch] [ebp-4h]

  stdin = GetStdHandle(STD_INPUT_HANDLE);
  stdout = GetStdHandle(STD_OUTPUT_HANDLE);
  WriteFile(stdout, aLetSStartOutEa, 0x2Au, &NumberOfBytesWritten, 0);
  ReadFile(stdin, byte_402158, 0x32u, &NumberOfBytesWritten, 0);
  i = 0;
  while ( ((unsigned __int8)byte_402158[i] ^ 0x7D) == byte_402140[i] )
  {
    if ( ++i >= 24 )
      return WriteFile(stdout, aYouAreSuccess, 0x12u, &NumberOfBytesWritten, 0);
  }
  return WriteFile(stdout, aYouAreFailure, 0x12u, &NumberOfBytesWritten, 0);
}
```
* There's only one function and the logic is clear
* We'll be success if and only if we don't get out of the while loop
* Write a script to decode the input
    ```python
    flag = byte_402158 = ""
    byte_402140 = [0x1F, 0x08, 0x13, 0x13, 0x04, 0x22, 0x0E, 0x11, 0x4D, 0x0D, 
    0x18, 0x3D, 0x1B, 0x11, 0x1C, 0x0F, 0x18, 0x50, 0x12, 0x13, 
    0x53, 0x1E, 0x12, 0x10]
    for i in range(24):
        flag += chr(byte_402140[i] ^ 0x7D)
    ```
### Flag
```bunny_sl0pe@flare-on.com```

## C2
### Process Analysis
* Another password crack challenge<br>
  ![](img/C2%20-%20start.png)
### IDA Pro Issue solution
![](img/C2%20-%20warning.png)
1. ```Options``` -> ```General``` -> Click on ```Stack pointer```<br>
  ![](img/C2%20-%20sp.png)
2. Find the place where sp value is negative<br>
  ![](img/C2%20-%20negsp.png)
3. Cursor points to the address right before the address where sp value is negative -> type ```ALT + k``` and we can change the sp value<br>
  ![](img/C2%20-%20ALT_k.png)
4. Change the difference to the negative value<br>
  ![](img/C2%20-%20change.png)
5. All the sp value is now non-negative, and we can decompile it successfully<br>
  ![](img/C2%20-%20succ.png)
### Function Analysis
* main function (0x401000)
    ```c
    BOOL __usercall sub_401000@<eax>(int a1@<ebp>)
    {
    HANDLE stdin; // ST1C_4
    BOOL result; // eax
    HANDLE stdout; // [esp-10h] [ebp-10h]
    signed int v4; // [esp-Ch] [ebp-Ch]
    int v5; // [esp-8h] [ebp-8h]
    int retaddr; // [esp+0h] [ebp+0h]

    v5 = a1;
    stdin = GetStdHandle(STD_INPUT_HANDLE);
    stdout = GetStdHandle(STD_OUTPUT_HANDLE);
    WriteFile(stdout, aYouCrushedThat, 0x43u, &v4, 0);
    ReadFile(stdin, &unk_402159, 0x32u, &v4, 0);
    if ( sub_401084(&v4, retaddr, &unk_402159, v4) )
        result = WriteFile(stdout, aYouAreSuccess, 0x11u, &v4, 0);
    else
        result = WriteFile(stdout, aYouAreFailure, 0x11u, &v4, 0);
    return result;
    }
    ```
    * To output YouAreSuccess, the return value of sub_401084 should not be zero
    * ```v4``` is the number of bytes read from user
    * ```retaddr``` is unknown, but can be retrieved during dynamic analysis
      ![](img/C2%20-%20stack.png)
    * ```&unk_402159``` is a buffer which points to a buffer that stores the user input
* sub_401084 (0x401084)
    ```c
    int __usercall sub_401084@<eax>(int result@<eax>, int a2, char *pInput, signed int NumberOfBytesRead)
    {
    __int16 v4; // bx
    signed int v5; // ecx
    char *_pInput; // esi
    _BYTE *target; // edi
    char Cur; // al
    unsigned int v9; // et0
    char v10; // cf
    __int16 v11; // ax
    bool Succ; // zf
    int v13; // edi
    int hex_C7; // [esp+0h] [ebp-Ch]

    v4 = 0;
    v5 = 37;
    if ( NumberOfBytesRead >= 37 )
    {
        _pInput = pInput;
        target = (a2 + 36);                         // a2[36]
        while ( 1 )
        {
        LOWORD(result) = 0x1C7;
        hex_C7 = result;
        Cur = *_pInput++;
        v9 = __readeflags();
        __writeeflags(v9);
        v11 = (__ROL1__(1, v4 & 3) + v10 + (hex_C7 ^ Cur));
        v4 += v11;
        Succ = *target == v11;
        v13 = (target + 1);
        if ( !Succ )
            LOWORD(v5) = 0;
        result = hex_C7;
        if ( !v5 )
            break;
        target = (v13 - 2);                       // v13 = v7 + 1
                                                    // v7 <- v13 - 2 = v7 + 1 - 2 = v7 - 1
        if ( !--v5 )                              // !--v5 will be True if v5 = 1
            return result;
        }
    }
    return 0;
    }
    ```
    * To avoid ```return 0;```, we cannot get out of the while loop
    * ```target``` is the same as ```retaddr```
    * Inside the loop, the program will encrypt the user input and compares it to the ```target``` from the end of ```target``` to the start of ```target```
    * There's one more unknown variable here, i.e., ```v10```
      * As the comment set by IDA says, it stores the value of ```CF```, abbreviation of Carry Flag
      * The pseudo code can't present the value of ```CF```, so we've to look at the assembly code
        ![](img/C2%20-%20eflag.png)
        * The main instructions that will affect the value of ```CF``` here are
          ```asm
          mov ax, 1C7
          sahf
          pushfd
          popfd
          ```
          * ```sahf```
            * Store AH into Flags
            * Loads the SF, ZF, AF, PF, and CF flags of the EFLAGS register with values from the corresponding bits in the AH register (bits 7, 6, 4, 2, and 0, respectively)
            * So the value of ```CF``` is now the 0 bit of ```AH``` and since ```AX``` = 0x1c7 = 0b111000111, ```AH``` = 1, 0 bit of ```AH``` = 1. Therefore the value of ```CF``` is now set to 1
          * ```pushfd```
            * Push ```EFLAGS``` register onto the stack
            * So the ```EFLAGS``` that ```CF``` = 1 is now stored on the stack
          * ```popfd```
            * Pop stack into ```EFLAGS``` register
            * Since the instructions between ```pushfd``` and ```popfd``` don't affect the stack, ```popfd``` wil take the exact value that ```pushfd``` pushed to the stack
            * Moreover, this is the last instruction before ```adc```, so the instruction ```adc``` will add ```CF``` which is always 1
    * This encryption is invertible
### Decryption
```python
def rol(bit, shift):
    # 32-bit register
    bit = bin(bit)[2:].rjust(32,'0')
    return int(bit[shift:] + bit[:shift],2)

flag = ""
v4 = 0
CF = 1
target = b'\xaf\xaa\xad\xeb\xae\xaa\xec\xa4\xba\xaf\xae\xaa\x8a\xc0\xa7\xb0\xbc\x9a\xba\xa5\xa5\xba\xaf\xb8\x9d\xb8\xf9\xae\x9d\xab\xb4\xbc\xb6\xb3\x90\x9a\xa8'

for i in range(len(target)-1,-1,-1):
    flag += chr((target[i]-CF-rol(1,v4&3)) ^ 0xC7)
    v4 += target[i]
```
### Flag
```a_Little_b1t_harder_plez@flare-on.com```