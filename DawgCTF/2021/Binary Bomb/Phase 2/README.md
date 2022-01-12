# Phase 2 (50)

### Description
> Can you help me find my lost key so I can read my string?

### File
* [bbomb](../bbomb)

### Tool
* IDA Pro

### Solution
1. Observe function phase2()
   ```c
   __int64 phase2()
   {
     unsigned int v1; // [rsp+18h] [rbp-28h]
     int i; // [rsp+1Ch] [rbp-24h]
     char *v3; // [rsp+28h] [rbp-18h]
   
     puts("\nCan you help me find my lost key so I can read my string?");
     v1 = 1;
     v3 = (char *)calloc(0x29uLL, 1uLL);
     getInput(2);
     for ( i = 0; i < strlen("Dk52m6WZw@s6w0dIZh@2m5a") && i < strlen(v3); ++i )
     {
       if ( aDk52m6wzwS6w0d[i] != ((unsigned __int8)v3[i] ^ 5) )
         v1 = 0;
     }
     if ( i != strlen("Dk52m6WZw@s6w0dIZh@2m5a") )
       v1 = 0;
     free(v3);
     return v1;
   }
   ```
2. Input v3 should be the same as Dk52m6WZw@s6w0dIZh@2m5a after xor 5
3. v3 = An07h3R_rEv3r5aL_mE7h0d

### Flag
```
DawgCTF{An07h3R_rEv3r5aL_mE7h0d}
```