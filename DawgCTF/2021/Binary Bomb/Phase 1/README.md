# Phase 1 (25)

### Description
> Welcome to the CyberDawgs Binary Bomb challenge series! The "bbomb" binary contains a series of mini reversing challenges broken into 9 phases. Each phase becomes incresingly more difficult, but it is not required to solve a phase to move onto the next. Simply press enter for a phase's input to skip it. Additionally, known phase solutions can be stored in a file named "flags.txt". See the binary's welcome message for the format and requirements. When submitting to this scoreboard, wrap the phase's solution in DawgCTF{}. Happy reversing!
>
> Starting off easy... reversing (things) is fun!

### File
* [bbomb](../bbomb)

### Tool
* IDA Pro

### Solution
1. Observe function phase1()
   ```c
   __int64 phase1()
   {
       unsigned int v1; // [rsp+14h] [rbp-2Ch]
       int index; // [rsp+18h] [rbp-28h]
       int v3; // [rsp+1Ch] [rbp-24h]
       char *s; // [rsp+28h] [rbp-18h]
       
       puts("\nStarting off easy... reversing (things) is fun! (Wrap all flags in DawgCTF{} when submitting to the scoreboard)");
       v1 = 1;
       s = (char *)calloc(0x29uLL, 1uLL);
       getInput(1);
       index = 0;
       v3 = strlen(s);
       while ( index < strlen("Gn1r7s_3h7_Gn15Rev3R") && index < strlen(s) )
       {
           if ( aGn1r7s3h7Gn15r[index] != s[v3 - index - 1] )
           v1 = 0;
           ++index;
       }
       if ( index != strlen("Gn1r7s_3h7_Gn15Rev3R") )
           v1 = 0;
       free(s);
       return v1;
   }
   ```
2. s is the input and it's going to be compared with aGn1r7s3h7Gn15r = "Gn1r7s_3h7_Gn15Rev3R"
3. v3 is the length of s and when index=0, v3-index-1 = last index of s, that is, s is compared with aGn1r7s3h7Gn15r in a reverse order. s = R3veR51nG_7h3_s7r1nG

### Flag
```
DawgCTF{R3veR51nG_7h3_s7r1nG}
```