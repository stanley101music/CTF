# Flare-On 2017 writeup
* [Download challenges](https://flare-on.com/files/Flare-On4_Challenges.zip)
* [Official writeup](https://www.mandiant.com/resources/2017-flare-on-challenge-solutions)
## C1
### Function Analysis
```html
<!DOCTYPE Html />
<html>
    <head>
        <title>FLARE On 2017</title>
    </head>
    <body>
        <input type="text" name="flag" id="flag" value="Enter the flag" />
        <input type="button" id="prompt" value="Click to check the flag" />
        <script type="text/javascript">
            document.getElementById("prompt").onclick = function () {
                var flag = document.getElementById("flag").value;
                var rotFlag = flag.replace(/[a-zA-Z]/g, function(c){return String.fromCharCode((c <= "Z" ? 90 : 122) >= (c = c.charCodeAt(0) + 13) ? c : c - 26);});
                if ("PyvragFvqrYbtvafNerRnfl@syner-ba.pbz" == rotFlag) {
                    alert("Correct flag!");
                } else {
                    alert("Incorrect flag, rot again");
                }
            }
        </script>
    </body>
</html>
```
* ```function(c){return String.fromCharCode((c <= "Z" ? 90 : 122) >= (c = c.charCodeAt(0) + 13) ? c : c - 26);}```
  * This function is doing ```ROT13``` on character set ```[a-zA-Z]```
  * The inverse function of ```ROT13``` is itself
### Decryption
```python
import codecs
flag = codecs.encode('PyvragFvqrYbtvafNerRnfl@syner-ba.pbz', 'rot_13')
```
### Flag
* ```ClientSideLoginsAreEasy@flare-on.com```

## C2
### Function Analysis
* start function (0x401180)
    ```c
    void __noreturn start()
    {
        DWORD NumberOfBytesWritten; // [esp+0h] [ebp-4h]

        NumberOfBytesWritten = 0;
        stdin = GetStdHandle(STD_INPUT_HANDLE);
        stdout_403074 = GetStdHandle(STD_OUTPUT_HANDLE);
        WriteFile(stdout_403074, aG1v3M3T3hFl4g, 0x13u, &NumberOfBytesWritten, 0);
        sub_4010F0();                                 // Copy input to Input_403078 excpet for '\n' amd '\r' which denotes CRLF that represents newline in Windows
        if ( sub_401050() )
            WriteFile(stdout_403074, aG00dJ0b, 0xAu, &NumberOfBytesWritten, 0);
        else
            WriteFile(stdout_403074, aN0tT00H0tRWe7r, 0x24u, &NumberOfBytesWritten, 0);
        ExitProcess(0);
    }
    ```
    * ```sub_401050``` is doing the encryption, and if it returns 1, we'll get to the right control flow
* sub_401050 (0x401050)
    ```c
    signed int sub_401050()
    {
        int length; // ST04_4
        int i; // [esp+4h] [ebp-8h]
        unsigned int j; // [esp+4h] [ebp-8h]
        char v4; // [esp+Bh] [ebp-1h]

        length = sub_401020((int)Input_403078);
        v4 = sub_401000();                            // v4 = 0x4
        for ( i = length - 1; i >= 0; --i )
        {
            byte_403180[i] = v4 ^ Input_403078[i];
            v4 = Input_403078[i];
        }
        for ( j = 0; j < 0x27; ++j )
        {
            if ( byte_403180[j] != (unsigned __int8)byte_403000[j] )
            return 0;
        }
        return 1;
    }
    ```
    * ```sub_401020``` will return the length of input parameter
    * ```sub_401000``` is doing some arithmetic opertaions on constants, so the return value isalso a constant
      * The return value is ```0x700004```<br>
        ![](img/C2%20-%20cons.png)
      * But the value of ```v4``` is ```0x4``` since it only takes the value from ```al```
    * ```byte_403180``` stores the value of encrypted data and the value should  equal to ```byte_403000```
    * Since ```byte_403000``` is known and the xor process is invertible, we can decrypt it
### Decryption
```python
flag = [None]*0x27
byte_403000 = [0x0D, 0x26, 0x49, 0x45, 0x2A, 0x17, 0x78, 0x44, 0x2B, 0x6C, 
  0x5D, 0x5E, 0x45, 0x12, 0x2F, 0x17, 0x2B, 0x44, 0x6F, 0x6E, 
  0x56, 0x09, 0x5F, 0x45, 0x47, 0x73, 0x26, 0x0A, 0x0D, 0x13, 
  0x17, 0x48, 0x42, 0x01, 0x40, 0x4D, 0x0C, 0x02, 0x69, 0x00]
v4 = 0x4
for i in range(0x27-1, -1, -1):
    flag[i] = chr(v4 ^ byte_403000[i])
    v4 = ord(flag[i])
flag = ''.join(flag)
```
### Flag
* ```R_y0u_H0t_3n0ugH_t0_1gn1t3@flare-on.com```

## C3
### Function Analysis
* sub_401008 (0x401008)
    ```c
    int __usercall sub_401008@<eax>(int _EDI@<edi>, _DWORD *a2@<esi>)
    {
        _BYTE *v2; // eax
        char _buf; // dl
        bool v5; // cf
        unsigned int v6; // ett
        int v7; // edx
        int v9; // [esp-4h] [ebp-1Ch]
        char buf; // [esp+10h] [ebp-8h]
        SOCKET s; // [esp+14h] [ebp-4h]
        int savedregs; // [esp+18h] [ebp+0h]

        s = sub_401121(&buf);
        if ( !s )
            return 0;
        v2 = &loc_40107C;
        _buf = buf;
        do
        {
            *v2 = (_buf ^ *v2) + 0x22;
            ++v2;
        }
        while ( (signed int)v2 < (signed int)&loc_40107C + 0x79 );// Self-modifying code which depends on the first byte of client's input
        if ( (unsigned __int16)sub_4011E6((unsigned __int8 *)&loc_40107C, 0x79u) == 0xFB5E )// This condition can help us find out which value of client input is correct
                                                        // brute force is easier, the range is only (1~255), 0 is obciously the the right answer
                                                        //   Set a breakpoint at this function 
        {
            _EBX = *(_DWORD *)(v9 + 377554449);
            __asm { lock xor bl, [edi+61791C4h] }
            v5 = __CFADD__(*(_DWORD *)(8 * (_DWORD)a2 + 0xFB5E), -250248954);
            *(_DWORD *)(8 * (_DWORD)a2 + 0xFB5E) -= 250248954;
            __ES__ = *(_WORD *)(v9 + 461440542);
            if ( v9 == 1 )
            {
            v6 = v5 + 427886322;
            v5 = MEMORY[0xFB5E] < v6;
            MEMORY[0xFB5E] -= v6;
            }
            __asm { icebp }
            *a2 -= v5 + 530171120;
            v7 = *(_DWORD *)(v9 - 1 + 494994972);
            __outbyte(6u, 0x5Eu);
            *(_DWORD *)(v7 - 17) &= 0xF2638106;
            MEMORY[0xFB41] &= 0x66199C4u;
            *(a2 - 17) &= 0xE6678106;
            *(_DWORD *)(8 * (_DWORD)&savedregs + 0xFB64) &= 0x69D6581u;
            *(_DWORD *)(v7 - 14) -= 107715012;
            MEMORY[0xFB07] += 278298362;
            *(_DWORD *)((char *)a2 - 18) += 1368424186;
            *(_DWORD *)(_EBX + 6) -= 116354433;
            *(_DWORD *)(v7 - 23) ^= 0x7C738106u;
            send(s, "Congratulations! But wait, where's my flag?", 43, 0);
        }
        else
        {
            send(s, "Nope, that's not it.", 20, 0);
        }
        closesocket(s);
        return WSACleanup();
    }
    ```
    * There're lots of wierd instructions
    * The first ```do while``` loop is self-modfying itself, the new value depends on the first byte of ```buf```, which will be explained latter what it stores
    * If ```(unsigned __int16)sub_4011E6((unsigned __int8 *)&loc_40107C, 0x79u) == 0xFB5E``` is True, than it'll go to the right control flow
      * sub_4011E6 is hard to decrypt, but there's other way
* sub_401121
    ```c
    SOCKET __cdecl sub_401121(char *buf)
    {
        SOCKET v2; // esi
        SOCKET v3; // eax
        SOCKET v4; // edi
        struct WSAData WSAData; // [esp+0h] [ebp-1A0h]
        struct sockaddr name; // [esp+190h] [ebp-10h]

        if ( WSAStartup(0x202u, &WSAData) )
            return 0;
        v2 = socket(2, 1, 6);
        if ( v2 != -1 )
        {
            name.sa_family = 2;
            *(_DWORD *)&name.sa_data[2] = inet_addr("127.0.0.1");
            *(_WORD *)name.sa_data = htons(0x8AEu);     // 0xAE08
            if ( bind(v2, &name, 16) != -1 && listen(v2, 0x7FFFFFFF) != -1 )// port 2222
            {
            v3 = accept(v2, 0, 0);
            v4 = v3;
            if ( v3 != -1 )
            {
                if ( recv(v3, buf, 4, 0) > 0 )          // take 4 bytes from client
                return v4;
                closesocket(v4);
            }
            }
            closesocket(v2);
        }
        WSACleanup();
        return 0;
    }
    ```
    * It'll only continue if we send to ```127.0.0.1:2222``` at least four bytes. Otherwise, if the sent bytes are less than four bytes, it'll return 0 and the ```sub_401008``` will also return without running the rest program
    * The received bytes will be stored in ```buf```
* Since the self-modifying bytes depend only on the the first byte of Client send, the possibility to make the statement ```(unsigned __int16)sub_4011E6((unsigned __int8 *)&loc_40107C, 0x79u) == 0xFB5E``` true is only 1/256
  * We can bruteforce from 0 to 256 and stop when the return value is 0xFB5E<br>
    ![](img/C3%20-%20brute.png)
    * The correct byte value is ```162```
* The instructions after self-modifying are generating stack string which is the flag
  ![](img/C3%20-%20flag.png)

```python
import socket
for i in range(1,256,1):
    print(i)
    s = socket.socket()
    s.connect(("127.0.0.1",2222))
    s.send(i.to_bytes(1,'big') + b'000')
    s.close
    input()
```
### Flag
```et_tu_brute_force@flare-on.com```