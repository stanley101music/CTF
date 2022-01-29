# Flare-On 2016 writeup
* [Download challenges](https://flare-on.com/files/Flare-On3_Challenges.zip)
* [Official writeup](https://www.mandiant.com/resources/2016-flare-challenges)
## C1
### Function Analysis
* main function (0x401420)
    ```c
    int __cdecl main(int argc, const char **argv, const char **envp)
    {
    char Buffer; // [esp+0h] [ebp-94h]
    char *cipher; // [esp+80h] [ebp-14h]
    char *target; // [esp+84h] [ebp-10h]
    HANDLE stdin; // [esp+88h] [ebp-Ch]
    HANDLE stdout; // [esp+8Ch] [ebp-8h]
    DWORD NumberOfBytesWritten; // [esp+90h] [ebp-4h]

    stdout = GetStdHandle(STD_OUTPUT_HANDLE);
    stdin = GetStdHandle(STD_INPUT_HANDLE);
    target = "x2dtJEOmyjacxDemx2eczT5cVS9fVUGvWTuZWjuexjRqy24rV29q";
    WriteFile(stdout, "Enter password:\r\n", 0x12u, &NumberOfBytesWritten, 0);
    ReadFile(stdin, &Buffer, 0x80u, &NumberOfBytesWritten, 0);
    cipher = sub_401260(&Buffer, NumberOfBytesWritten - 2);
    if ( !strcmp(cipher, target) )
        WriteFile(stdout, "Correct!\r\n", 0xBu, &NumberOfBytesWritten, 0);
    else
        WriteFile(stdout, "Wrong password\r\n", 0x11u, &NumberOfBytesWritten, 0);
    return 0;
    }
    ```
    * The return value of sub_401260 should equals to the value of target
* sub_401260 (0x401260)
    ```c
    _BYTE *__cdecl sub_401260(int pInput, unsigned int length)
    {
    unsigned int v3; // ST24_4
    int v4; // ST2C_4
    int v5; // [esp+Ch] [ebp-24h]
    int v6; // [esp+10h] [ebp-20h]
    int v7; // [esp+14h] [ebp-1Ch]
    int i; // [esp+1Ch] [ebp-14h]
    _BYTE *v9; // [esp+24h] [ebp-Ch]
    int v10; // [esp+28h] [ebp-8h]
    unsigned int idx; // [esp+2Ch] [ebp-4h]

    v9 = malloc(4 * ((length + 2) / 3) + 1);
    if ( !v9 )
        return 0;
    idx = 0;
    v10 = 0;
    while ( idx < length )
    {
        if ( idx >= length )
        v7 = 0;
        else
        v7 = *(idx++ + pInput);
        if ( idx >= length )
        v6 = 0;
        else
        v6 = *(idx++ + pInput);
        if ( idx >= length )
        v5 = 0;
        else
        v5 = *(idx++ + pInput);
        v3 = v5 + (v7 << 16) + (v6 << 8);
        v9[v10] = byte_413000[(v3 >> 18) & 0x3F];
        v4 = v10 + 1;
        v9[v4++] = byte_413000[(v3 >> 12) & 0x3F];
        v9[v4++] = byte_413000[(v3 >> 6) & 0x3F];
        v9[v4] = byte_413000[v5 & 0x3F];
        v10 = v4 + 1;
    }
    for ( i = 0; i < dword_413040[length % 3]; ++i )// dword_413040 = [0, 2, 1]
        v9[4 * ((length + 2) / 3) - i - 1] = '=';   // Append '=' to the end of output according to the value of (length % 3)
    v9[4 * ((length + 2) / 3)] = 0;               // Append '\x00' to the end of output
    return v9;
    }
    ```
    * This function is doing the encryption
    * It might not be clear what is actually doing at first, but we can first take a look at the last loop about what is's doing
      * It's appending ```=``` to the end of the output according to the value of ```dword_413040[length % 3]``` where ```dword_413040 = [0, 2, 1]```
      * This process is the same as base64
    * ```byte_413000 = "ZYXABCDEFGHIJKLMNOPQRSTUVWzyxabcdefghijklmnopqrstuvw0123456789+/"```
      * This also looks like the custom charset for base64
    * I assume this is doing the same process as base64 with non-standard charset
    * Verification
      * [Base64 C++ version](https://en.wikibooks.org/wiki/Algorithm_Implementation/Miscellaneous/Base64)
        ```cpp
        const static TCHAR encodeLookup[] = TEXT("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/");
        const static TCHAR padCharacter = TEXT('=');
        std::basic_string<TCHAR> base64Encode(std::vector<BYTE> inputBuffer)
        {
            std::basic_string<TCHAR> encodedString;
            encodedString.reserve(((inputBuffer.size()/3) + (inputBuffer.size() % 3 > 0)) * 4);
            DWORD temp;
            std::vector<BYTE>::iterator cursor = inputBuffer.begin();
            for(size_t idx = 0; idx < inputBuffer.size()/3; idx++)
            {
                temp  = (*cursor++) << 16; //Convert to big endian
                temp += (*cursor++) << 8;
                temp += (*cursor++);
                encodedString.append(1,encodeLookup[(temp & 0x00FC0000) >> 18]);
                encodedString.append(1,encodeLookup[(temp & 0x0003F000) >> 12]);
                encodedString.append(1,encodeLookup[(temp & 0x00000FC0) >> 6 ]);
                encodedString.append(1,encodeLookup[(temp & 0x0000003F)      ]);
            }
            switch(inputBuffer.size() % 3)
            {
            case 1:
                temp  = (*cursor++) << 16; //Convert to big endian
                encodedString.append(1,encodeLookup[(temp & 0x00FC0000) >> 18]);
                encodedString.append(1,encodeLookup[(temp & 0x0003F000) >> 12]);
                encodedString.append(2,padCharacter);
                break;
            case 2:
                temp  = (*cursor++) << 16; //Convert to big endian
                temp += (*cursor++) << 8;
                encodedString.append(1,encodeLookup[(temp & 0x00FC0000) >> 18]);
                encodedString.append(1,encodeLookup[(temp & 0x0003F000) >> 12]);
                encodedString.append(1,encodeLookup[(temp & 0x00000FC0) >> 6 ]);
                encodedString.append(1,padCharacter);
                break;
            }
            return encodedString;
        }
        ```
      * After comparing each operation, we can verify that this function is exactly base64 encode
### Decryption
```python
import base64
std_b64charset = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
custom_b64charset = "ZYXABCDEFGHIJKLMNOPQRSTUVWzyxabcdefghijklmnopqrstuvw0123456789+/"
cipher = "x2dtJEOmyjacxDemx2eczT5cVS9fVUGvWTuZWjuexjRqy24rV29q"
trans = str.maketrans(custom_b64charset, std_b64charset)
flag = base64.b64decode(cipher.translate(trans))
```
### Flag
```sh00ting_phish_in_a_barrel@flare-on.com```