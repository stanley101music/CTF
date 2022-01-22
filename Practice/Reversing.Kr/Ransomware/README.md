# Ransomware
## Overview
* 32-bit PE file
## File Analysis
* Use [Ditect It Easy] and find out that it's packed by upx 3.0<br>
  ![](../img/Ransomware%20-%20UPX.png)
* Unpack it with command ```upx -d run.exe```
## Function Analysis
* After opening it with IDA, it take a long time to do the auto analysis
* Find the main function at 0x4135E0, however it's too large to decompile or show the graph mode. This situation also happens in function at 0x401000
* However most of the instruction is meaningless and just keep pushing and poping values on the stack,  we can redefine the function boundary to exclude these useless instructions in the main function
  * Remember to add the function prologue at the start of the function. Press ```F2``` in hex mode of IDA can modify the bytes
* It turns out that the function at 0x401000 is entirely useless, so I undefine this function and rename it as ```NOP```
* The redefine main function starts at 0x44A76F including the function prologue
  * At this point, we can decompile the main function
### _main (0x44A76F)
* It'll take user's input as key and start to encrypt ```file``` and write the result back to ```file```
* Encryption
  ```python
  #pseudo code
  for i in range(len(plain)):
      cipher[i] = plain[i] ^ key[i % keylen]
      cipher[i] = ~cipher[i]
  ``` 
* Within this information is not enough for us to decrypt ```file```
  * There're additional information hidden in [readme.txt](./readme.txt), which tells us that the original type of ```file``` is actually an EXE, and every EXE file has the same DOS header
## File Analysis
* The decrypt ```file``` is also an upx packed file, use the same technique mentioned above to unpack it
* Since all the symbols aren't stripped, we know which one is main function
* Another way is to run the ```file``` directly and it should show the key
  * I get some system error when running ``file```<br>
    ![](../img/Ransomware%20-%20error.png)
    * It should be fixed by download ```MSVCR100D.dll``` but anyway I choose to reverse it
## Function Analysis
### wmain_0 (0x411390)
```
int wmain_0()
{
  printf("Key -> Colle System");
  getch();
  return 0;
}
```
## Flag
```Colle System```