# x64 Lotto
## Overview
* 64-bit PE file
* The program will ask for 6 inputs and keep cleaning the terminal window
* The wmain function is at 0x140001000
## Function Analysis
### wmain (0x140001000)
* All the program behavior is written in this function
```c
wscanf_s(L"%d %d %d %d %d %d", &input_0, &input_1, &input_2, &input_3, &input_4, &input_5);
wsystem(L"cls");                            // clear screen
Sleep(0x1F4u);
```
* It first take 6 input from user and stored it as integer
* Then it'll call ```cls``` command to clear the screen and a ```Sleep``` to make user wait for a very long time
  * These two instructions are irrelevant to the program's main logic flow and will slow down the dynamic analysis
  * I'll patch them to ```NOP``` during dynamic analysis
```c
    do
        *(&input_5 + ++idx) = rand() % 100;       // random number (0~99)
                                                // update rand_0 ~ rand_5
    while ( idx < 6 );
    Succ = 1;
    v3 = 0;
    idx4 = 0i64;
    byte_1400035F0 = 1;
    while ( *(&rand_0 + idx4) == *(&input_0 + idx4) )// Comparing our input with the random number
    {
        idx4 += 4i64;
        ++v3;
        if ( idx4 >= 24 )
        goto Succeed;
    }
    Succ = 0;
    byte_1400035F0 = 0;
Succeed:
```
* The program will generate 6 random numbers and compare them with the previous user's input
* There's a large loop containing these two code blocks and will only break if the user guesses all the correct numbers
```c
do
{
    v7 = byte_140003021[idx5 - 1];
    idx5 += 5i64;
    *(&rand_3 + idx5 + 1) ^= (v7 - 12);         
    *(&rand_4 + idx5) ^= (byte_140003021[idx5 - 5] - 12);
    *(&rand_4 + idx5 + 1) ^= (byte_140003021[idx5 - 4] - 12);
    *(&rand_5 + idx5) ^= (byte_140003021[idx5 - 3] - 12);
    *(&rand_5 + idx5 + 1) ^= (byte_140003021[idx5 - 2] - 12);
}
while ( idx5 < 25 );                          // loop 5 times
if ( Succ )
{
    index = 0;
    v9 = &v25;
    do
    {
        v10 = *v9;
        ++v9;
        v11 = index++ + (v10 ^ 0xF);
        *(v9 - 1) = v11;
    }
    while ( index < 25 );
    v50 = 0;
    wprintf(L"%s\n", &v25);
}
```
* The last part is doing some encryption and if everything goes right, it'll output the flag
* The variables ```&rand_3, &rand_4, &rand_5``` seemed to be the random number generated earlier, but if we take a look at the address of each variable and the real address of ```&rand_3 + idx5 +1```, we'll find out that these address are actually storing some constant integers instead of random numbers
  * It make sense, otherwise the flag will always be different
* Therefore, we can write a script to simulate the encryption or utilize the debugger to first modify our input to match the random number and then let the program does its job
## Flag
```from_GHL2_-_!```