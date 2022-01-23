# CSHARP
## Overview
* 32-bit .Net file
* After running the file, it'll popup a window where user can type input
* There's a click button which will tell you if your input is right or wrong
## Function Analysis
### Form1
* The entire class is almost decompilable instead of method ```MetMett```
* Inside Form1's constructor, there're instructions modifying the content of ```MetMett```, so it might be self-modifying the bytes of ```MetMett``` that works like a packer
* We can set a breakpoint at the end of constructor and dump out the region of ```MetMett``` and replace the original ```MetMett``` with our new dump bytes
  * Add Watch on variable ```Form1.bb```, which is the variable that holds the new byte of ```MetMett```
  * Right click on this variable and click ```Show in Memory Window```
  * Select the entire region of ```Form1.bb```, right click and click ```Save Selection``` to dump the new ```MetMett```
  * Open the original ```CSharp.exe``` and the new ```MetMett``` in any hex editor
  * Replace the original ```MetMett``` in ```CSharp.exe``` with our new ```MetMett```
    * You can find the region of ```MetMett``` in ```CSharp.exe``` with the help of dnSpy or by analyzing the image header
    * Be careful of the header of ```MetMett``` that should not be replaced, only the content of ```MetMett``` should be replaced, which is equal to the size of our new ```MetMett```
### MetMett
```csharp
private static void MetMett(byte[] chk, byte[] bt)
{
    if (bt.Length == 12)
    {
        chk[0] = 2;
        if ((bt[0] ^ 16) != 74)
        {
            chk[0] = 1;
        }
        if ((bt[3] ^ 51) != 70)
        {
            chk[0] = 1;
        }
        if ((bt[1] ^ 17) != 87)
        {
            chk[0] = 1;
        }
        if ((bt[2] ^ 33) != 77)
        {
            chk[0] = 1;
        }
        if ((bt[11] ^ 17) != 44)
        {
            chk[0] = 1;
        }
        if ((bt[8] ^ 144) != 241)
        {
            chk[0] = 1;
        }
        if ((bt[4] ^ 68) != 29)
        {
            chk[0] = 1;
        }
        if ((bt[5] ^ 102) != 49)
        {
            chk[0] = 1;
        }
        if ((bt[9] ^ 181) != 226)
        {
            chk[0] = 1;
        }
        if ((bt[7] ^ 160) != 238)
        {
            chk[0] = 1;
        }
        if ((bt[10] ^ 238) != 163)
        {
            chk[0] = 1;
        }
        if ((bt[6] ^ 51) != 117)
        {
            chk[0] = 1;
        }
    }
}
```
* It's doing xor and checking
* Only if every condition is met then the value of ```chk[0]``` is 1
* After decrypting it, we'll get ```ZFluYWFNaWM=```, which looks like a base64 encoded string
* By base64 decoding it, we can get the real flag
## Flag
```dYnaaMic```