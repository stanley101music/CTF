# Easy Unpack
## Overview
* 32-bit PE file
* According to the challenge's name, it's a packed pe file
* According to [ReadMe.txt](./ReadMe.txt), we need to find the OEP (Original Entry Point) of this program
## File Analysis
* Since it's a packed file, we can first use [Exeinfo PE]() to figure out whether it's a common packer and we can unpack it directly<br>
![](../img/Easy%20Unpack%20-%20Exeinfo%20PE.png)
    * It's not our case
## Packer
* Packer is a method to compress a file
* This technique can be used to reduce file size, hide secrets
* When it comes to malware, it'll make the reverse process harder since the executable file becomes unreadable
* There're various kinds of packer, one of the most common packer is [UPX](https://upx.github.io/)
## Original Entry Point
* The original entry point (OEP) is the address of the malware's first instruction (where malicious code begins) before it was packed
### How to find OEP
* Look for calls that don’t return
* Look for jumps with no code after them
* Look for long jumps that jump into a different section
* [Look for pushad. Sent a memory breakpoint on these stack addresses, which should break on the corresponding popad](https://www.youtube.com/watch?v=IxkPwBWUyEk)
* Add breakpoints on ```GetVersion``` or ```GetCommandLineA```, ```GetModuleHandle```
## Function Analysis
### start (0x40A04B)
* This is the new entry point of the packed executable file
* Here, I'm going to use the long jump strategy
* The first long jump appears at 0x40A1FB and it jumps to 0x401150
  * We can verify it by setting breakopint at 0x401150 and when we meet the breakpoint, we can check if the assembly codes look like a normal windows start function and if it's significantly different from the original static assembly view in Disassembler<br>
  ![](../img/Easy%20Unpack%20-%20OEP.png)
## Flag
```00401150```

## References
* [Packer](https://encyclopedia.kaspersky.com/glossary/packer/)
* [Manual Unpacking](https://grazfather.github.io/posts/2016-11-06-manual-unpacking/)
* [Dump a packed executalbe with Scylla](https://guidedhacking.com/threads/how-to-dump-a-packed-executable-with-scylla.15937/)