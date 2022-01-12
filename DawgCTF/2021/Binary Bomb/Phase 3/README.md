# Phase 3 (75)

### Description
> Reflections? Rotations? Translations? This is starting to sound like geometry...

### File
* [bbomb](../bbomb)

### Tool
* IDA Pro

### Solution
1. Observe function phase3()
   ```c
   __int64 __fastcall phase3(char *a1)
   {
     __int64 v1; // r8
     __int64 v2; // r9
     _BOOL4 v3; // ST14_4
     char *i; // [rsp+18h] [rbp-18h]
     char *s1; // [rsp+28h] [rbp-8h]
   
     puts("\nReflections? Rotations? Translations? This is starting to sound like geometry...");
     s1 = (char *)calloc(0x29uLL, 1uLL);
     getInput(3u, a1, (__int64)"%s", (__int64)s1, v1, v2);
     for ( i = s1; *i; ++i )
     {
       *i = *func3_1(i);
       *i = *func3_2(i);
     }
     v3 = strcmp(s1, "\"_9~Jb0!=A`G!06qfc8'_20uf6`2%7") == 0;
     free(s1);
     return (unsigned int)v3;
   }
   ```
2. Each character in input s1 will be converted first by func3_1 and then func3_2. The result should match \"_9~Jb0!=A\`G!06qfc8'_20uf6\`2%7
3. The flag can be found by directly reverse func3_1 and func3_2 or brute force through all printable ascii as input to find out which result is correct
4. Write a [python file](./solve.py) to simulate two functions and brute force

### Flag
```
DawgCTF{D0uBl3_Cyc1iC_rO74tI0n_S7r1nGs}
```