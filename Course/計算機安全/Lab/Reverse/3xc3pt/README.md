* Category
  * SEH
* Solution
  1. How to find exception handling function
     * IDA pro
     * Manually Calculated by header information (PE-bear)
       * Optional Hdr $\rightarrow$ Exception Directory(follow RVA address) $\rightarrow$ Exception $\rightarrow$ Find the address where the exception happens in the Exception table $\rightarrow$ UnwindInfoAddress(follow RVA address) $\rightarrow$ Parse the structure (third byte is CountOfCOdes, after allignment, we can find the RVA address of exception function) $\rightarrow$ ImageBase + RVA address = Address of exception handling function
  2. Exception handling function is at offset 0x1100
* ```FLAG{Wh3n_Do1nG_PpT_SEH_alWays_be_pAtch3d_to_SHE___=_=}```