# Flash Encrypt
## Overview
* swf file
* I use [FFdec](https://github.com/jindrapetrik/jpexs-decompiler) to decompile the file
* [Flash Player projector (content debugger)](https://www.adobe.com/support/flashplayer/debug_downloads.html)
  * This is necessary for debugginig and running flash
## Function Analysis
* There're 7 frames and 6 button click scripts
  * Each frame can get one input from user and if the input is correct, after clicking the button, it'll step to the next frame
* We can know which frame's button own's which script by hovering over the button in FFdec<br>
  ![](../img/Flash%20Encrypt%20-%20own.png)
* The ActionScript is hardly obfuscated, but there're options such as ```Automatic deobfuscation``` and ```Simplify expressions``` in FFdec to deal with these problems
### DefineButton2 (4)
```c
on(release){
   if(spw == 1456)
   {
      gotoAndPlay(3);
   }
   else
   {
      _root.spw = "";
   }
}

```
* owned by frame 1
* input = 1456
* go to frame 3
* This is the starting frame
### DefineButton2 (7)
```c
on(release){
   if(spwd == 8)
   {
      spw /= spwd;
      spwd = "";
      gotoAndPlay(6);
   }
}
```
* owned by frame 2
* input = 8
* go to frame 6
### DefineButton2 (9)
```c
on(release){
   if(spwd == 25)
   {
      spw *= spwd;
      spwd = "";
      gotoAndPlay(4);
   }
}
```
* owned by frame 3
* input = 25
* go to frame 4
### DefineButton2 (11)
```c
on(release){
   if(spwd == 44)
   {
      spw += spwd;
      spwd = "";
      gotoAndPlay(2);
   }
}
```
* owned by frame 4
* input = 44
* go to frame 2
### DefineButton2 (13)
```c
on(release){
   if(spwd == 20546)
   {
      spw %= spwd;
      spwd = "";
      gotoAndPlay(7);
   }
}
```
* owned by frame 5
* input = 20546
* go to frame 7
### DefineButton2 (15)
```c
on(release){
   if(spwd == 88)
   {
      spw *= spwd;
      spwd = "";
      gotoAndPlay(5);
   }
}
```
* owned by frame 6
* input = 88
* go to frame 5
## Order
* frame
  * 1 -> 3 -> 4 -> 2 -> 6 -> 5 -> 7
* input value
  * 1456 -> 25 -> 44 -> 8 -> 88 -> 20546
  * After typing all the input in correct order, the flag will show up in the last frame
## Flag
```16876```