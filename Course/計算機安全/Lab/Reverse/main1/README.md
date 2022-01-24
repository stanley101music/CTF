* Category
  * init / fini
* Solution
  1. Search in ```init``` and ```fini``` functions or ```_init_array``` and ```_init_array``` to see if there's any hidden functions
     * General speaking, it's wierd to see more than one function
     * we can stop immediately after program starts by gdb with command ```starti```
  2. sub_1328 in ```_init_array``` is wierd
     * use gdb ```vmmap``` to find out base address
  3. Trace into it and figure out the main hidden function is at offset 0x11EA
  4. By dynamic analysis, figure out that the original flag will be replaced by the correct flag generated dynamically if the input equals to 0x54878745
     * ```set $[register]=0x54878745```
* ```FLAG{DK_ShowMaker_WWT}```