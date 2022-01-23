# AutoHotkey1
## Overview
* 32-bit PE file
* Packed by UPX 3.03
* According [readme.txt](./readme.txt), we need to find two md5 value
* The packed version will ask for input and after clicking "OK" it'll exit the process unless you type the correct value
  * One of the md5 value should be this input
* The unpacked version will corrupt immediately after running<br>
  ![](../img/AutoHotkey1%20-%20corrupt.png)
  * However, this is not a usual corrupted window activated by OS
  * It seems to be a popup window defined by ahk itself
  * The OEP is at 0x442B4F and the WinMain function is at 0x44770D
## Process Analysis
* We first figure out how ahk is going to deal with our input
* Set a hardware breakpoint at ```WinMain``` function and run the program. After hitting the breakpoint we start to run the program one instruction at a time until the input window popups. Set a new hardware breakpoint at this address and rerun the entire program.
  * Continue this process until we find which function is doing the comparison
  * The maximum number of harware breakpoint is 4, we can delete the previous hardware breakpoint that is no longer needed
  * After some trial-and-error, the function 0x425C34 called at 0x405649 in function 0x402CC4 is the one we're looking for
  * This whole process can be accelerated by viewing the Call stack when clicking the "OK" button, but I cannot get the correct result every time
## Function Analysis
### sub_425C34 (0x425C34)
* There's a ```DialogBoxParamA``` function with call back function, ```DialogFunc``` at 0x425E6D
  * This call back function is dealing with our input
### DialogFunc (0x425E6D)
* ```GetWindowTextA``` is the exact function that's reading our input, set a breakpoint at this api and see where does the program store out input
  * The ```GetWindowTextA``` is called from 0x425FBD, and we know that the second parameter of ```GetWindowTextA``` is the buffer that will receive the text, we can now set another breakpoint at this buffer
    * right click on the buffer's address in dump window
    * select breakpoint
    * select harware access
    * select dword
  * Also set a breakpoint at 0x425FBD to know the value of its parameters<br>
    ![](../img/AutoHotkey1%20-%20buffer.png)
* Continue running and hit the breakpoint we set on the buffer and we'll find out that it's actually comparing it to ```54593f6b9413fc4ff2b4dec2da337806```
  * Using [CrackStation](https://crackstation.net/) we can get the original string that is ```pawn```
* So far, we still need another md5 value
  * The readme.txt also says that one md5 value is for EXE's Key, and the other is for DecryptKey
  * This one might be the EXE's key since there aren't any access to this address after the comparison and the value isn't stored anywhere else
  * The DecryptKey might be compared before we enter our input
## Process Analysis
* Remember that we get crashed on the unpacked version, it make sense if the DecryptKey doesn't match after we unpack the file. It might be doing some self-checking to validate the DecryptKey is correct
* Search for string "EXE corrupted" to find out which function is doing the validation
* The strnig was referenced at two locations and both of them are only executed if the return value of sub_4508C7 is non-zero
  * To avoid executing the error message, we want the return value to be 0
## Function Analysis
### sub_4508C7 (0x4508C7)
* The only opportunity for the program to return 0 is to execute the entire function till the end
* Since we know the original packed version of ahk can pass the validation, we can run the packed version and set breakpoints at every sub functions of sub_4508C7
  * After hitting the breakopint, check on all the address of parameter and see if there's any value that looks like md5 after executing that sub function
* It turns out that the first parameter of sub function sub_450ABA is the one that will store the md5 hash value which is ```220226394582d7117410e3c021748c2a```<br>
  ![](../img/AutoHotkey1%20-%20DecryptKey.png)
  * Use the same online tool again and get the original string ```isolated```
## Flag
```isolated pawn```

