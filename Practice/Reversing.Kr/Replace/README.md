# Replace
## Overview
* 32-bit PE file
* The function symbols aren't stripped, so it's easy to find WinMain function at 0x401000
* Users can type at the window and after clicking the Check button it'll crash
## Function analysis
* The basic component is similar to [Eascy Crack](../Easy%20Crack), so I'll skip the first few steps and start from the DialogFunc at 0x401020
### DialogFunc (0x401020)
* It's using ```GetDlgItemInt``` to take user's input
  ```c
  UINT GetDlgItemInt(
    [in]            HWND hDlg,
    [in]            int  nIDDlgItem,
    [out, optional] BOOL *lpTranslated,
    [in]            BOOL bSigned
  );
  ```
  > Translates the text of a specified control in a dialog box into an integer value
* After viewing the graph view of this function, it seems that there's no way to reach the correct path<br>
  ![](../img/Replace%20-%20correct%20path.png)
* We can set a breakopint after ```GetDlgItemInt``` to see how the program is going to process our input, and why it crashes

## Process Analysis
* After some tracing, it eventually stops at 0x40466F ```mov byte ptr [eax], 0x90```, where eax is currently an invalid address
  * 0x90 is ```nop```
  * So, what the program does is to overwrite an address to ```nop```, and as we can tell from the above figure, if we patch the instruction at 0x401071 to ```nop```, the control flow will executes to the correct path instead of skipping it
* Our next step is to figure out what is the relationship between our input and the value of eax
  * The return value is storing at 0x4084D0, so we're going to focus on how it's going to be modified
  * The process includes
    * +1
    * +1
    * +0x601605c7
    * +1
    * +1
  * eax = input + 0x601605CB
* To make the value of eax = 0x401071
  * input = 0x401071 - 0x601605CB = (0x100000000 - 0x601605CB) + 0x401071 = 0xA02A0AA6 = 2687109798
* After typing this value, it'll reach the correct path<br>
  ![](../img/Replace%20-%20flag.png)
## Flag
```2687109798```