# Music Player
## Overview
* Music_Player.exe
  * 32-bit PE file
  * It'll ask for a mp3 file and user can play it
    * The maximum minutes to play is 1 minute
  * According to [ReadMe.txt](./ReadMe.txt), we've to play more than 1 minute to get the flag
* msvbvm60.dll
  * 32-bit PE file
  * Music_Player's import moudule
## Function Analysis
### start (0x401478)
![](../img/Muisc%20Player%20-%20Entry.png)
* This is the entry point of Music_Player.exe
* It directly calls the ThunRTMain (0x401472) and jump to the import function, ThunRTMain in msvbvm60.dll
### ThunRTMain (0x729435A4)
* It contains lots of unknown functions, so instead of reversing all of them, we can first try to run the program, and see if there's any interesting behavior to help us focus on the related function
## Process Analysis
![](../img/Muisc%20Player%20-%20one%20minute.png)
* It'll popup a windows with some unreadable strings start with 1 when the music player has palyed for 1 minute
* To trace back which function cause this behavior, we can take a look at x64dbg's call stack window<br>
  ![](../img/Music%20Player%20-%20call%20stack.png)
  * It's called from music_player.004045DE
* Go to this address, and trace back to find out the start of the function that includes this address. We can find the start of a function by searching for function prologue
  ![](../img/Muisc%20Player%20-%20function%20prologue.png)
  * The function starts from 0x4044C0
  * This is currently not recognized as function in IDA, click on this address and press ```p``` to convert it into function
* Since it's checking whether the music has plyaed over one minute, we're looking for conditional jump that relies on comparing to a constant value that semantically equals to 1 minute
  * We find it at 0x404563 where the instruction is ```cmp eax, 0xEA60```, and 0xEA60 = 60000 = 60 * 1000 = 60000(milliseconds) = 1(minute)
  * We can patch the conditional jump instruction ```jl loc_4045FE``` into ```jmp loc_4045FE``` to make the jump happens no matter the amount of time goes
  * A new error appears<br>
    ![](../img/Muisc%20Player%20-%20380%20error.png)
* Run the program again, this time run step by step to figure out which instruction triggers the error<br>
  ![](../img/Muisc%20Player%20-%20380%20error%20addr.png)
  * It appears at 0x4046B9, where it calls to ```_vbaHresultCheckObj```
  * To bypass this situation, we trace back to the nearest jump condition and use the same technique to patch it and make it jump over this block, the jump condition is at 0x4046AB
  * The flag appears at the title<br>
    ![](../img/Music%20Player%20-%20flag.png)
## Flag
```LIstenCare```
## References
* [PE Imports](https://0xrick.github.io/win-internals/pe6/#introduction)