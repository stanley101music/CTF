# Position
## Overview
* 32-bit PE file
* MFC program
* According to [ReadMe.txt](./ReadMe.txt) we need to find the correct Name whose Serial is 76876-77776, the Name's length is 4 and it ends with ```p```
* It's easy to find wWinMain function, but this time it won't help much due to the extern function, so we choose to first search for the string ```Wrong``` which is the text that shows on the window when the Name doesn't match the Serial

## String Analysis
* Although I've used the IDA's string window ```SHIFT + F12```, it turns out that IDA cannot find the string "Wrong" in the string window
* Therefore, I used another tool called [BinText](https://bintext.soft32.com/) and successfully find the string "Wrong" at offset 0x3808<br>
  ![](../img/Position%20-%20string.png)
## Function Analysis
### sub_401CD0 (0x401CD0)
* This is the function that contains string "Wrong"
* The logic is simple, if the return value of sub_401740 is non-zero, than it'll output "Correct", otherwise, it'll output "Wrong"
### sub_401740 (0x401740)
* There're lots of comparison in this function, so I'm going to summarize all the conditions that will output "Correct"
* Rules
  ```c
  // Check lengtht of Name
  *(_DWORD *)(Name - 12) == 4

  // Check length of Serial
  *(_DWORD *)(Serial - 12) == 11

  // Check the 5th character of Serial
  ATL::CSimpleStringT<wchar_t,1>::GetAt(&Serial, 5) == '-'

  // Conditions on the value of characters of Name
  ATL::CSimpleStringT<wchar_t,1>::GetAt(&Name, v3) >= 0x61u && ATL::CSimpleStringT<wchar_t,1>::GetAt(&Name, v3) <= 0x7Au

  // Manipulate on the first two character of Name
  v6 = ATL::CSimpleStringT<wchar_t,1>::GetAt(&Name, 0);
  v7 = (v6 & 1) + 5;
  v48 = ((v6 >> 4) & 1) + 5;
  v42 = ((v6 >> 1) & 1) + 5;
  v44 = ((v6 >> 2) & 1) + 5;
  v46 = ((v6 >> 3) & 1) + 5;
  v8 = ATL::CSimpleStringT<wchar_t,1>::GetAt(&Name, 1);
  v34 = (v8 & 1) + 1;
  v40 = ((v8 >> 4) & 1) + 1;
  v36 = ((v8 >> 1) & 1) + 1;
  v9 = ((v8 >> 2) & 1) + 1;
  v38 = ((v8 >> 3) & 1) + 1;

  // Check Serial[0], Serial[1], Serial[2], Serial[3], Serial[4]
  v7 + v9 == Serial[0]
  v46 + v38 == Serial[1]
  v42 + v40 == Serial[2]
  v44 + v34 == Serial[3]
  v48 + v36 == Serial[4]

  // Manipulate on the last two character of Name
  v20 = ATL::CSimpleStringT<wchar_t,1>::GetAt(&Name, 2);
  v21 = (v20 & 1) + 5;
  v49 = ((v20 >> 4) & 1) + 5;
  v43 = ((v20 >> 1) & 1) + 5;
  v45 = ((v20 >> 2) & 1) + 5;
  v47 = ((v20 >> 3) & 1) + 5;
  v22 = ATL::CSimpleStringT<wchar_t,1>::GetAt(&Name, 3);
  v35 = (v22 & 1) + 1;
  v41 = ((v22 >> 4) & 1) + 1;
  v37 = ((v22 >> 1) & 1) + 1;
  v23 = ((v22 >> 2) & 1) + 1;
  v39 = ((v22 >> 3) & 1) + 1;

  //Check Serial[6], Serial[7], Serial[8], Serial[9], Serial[10]
  v21 + v23 == Serial[6]
  v47 + v39 == Serial[7]
  v43 + v41 == Serial[8]
  v45 + v35 == Serial[9]
  v49 + v37 == Serial[10]
  ```
* Since the amounts of all the possibilities is small, we can brute force each character to get the flag
* What's more, we can utilize the z3-solver to help solve the equations with constraints
## Flag
```
bump
cqmp
ftmp
gpmp
```