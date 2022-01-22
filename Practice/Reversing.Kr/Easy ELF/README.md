# Easy ELF
## Overview
* 32-bit ELF file
## Function Analysis
### main (0x804851B)
```c
int __cdecl main()
{
  write(1, "Reversing.Kr Easy ELF\n\n", 0x17u);
  sub_8048434();
  if ( sub_8048451() == 1 )
    sub_80484F7();                              // Correct
  else
    write(1, "Wrong\n", 6u);
  return 0;
}
```
* sub_8048434 will call scanf and store our input as string at 0x804A020
* sub_80484F7 will output "Correct", so we need to make sure sub_8048451 returns 1
### sub_804851 (0x804851)
```c
_BOOL4 sub_8048451()
{
  if ( byte_804A021 != '1' )                    // byte_21 = '1'
    return 0;
  byte_804A020 ^= 0x34u;
  byte_804A022 ^= 0x32u;
  byte_804A023 ^= 0x88u;
  if ( byte_804A024 != 'X' )                    // byte_24 = 'X'
    return 0;
  if ( byte_804A025 )                           // byte_25 = 0x0
    return 0;
  if ( byte_804A022 != 0x7C )                   // byte_22 ^ 0x32 = 0x7C
                                                // byte_22 = 0x32 ^ 0x7C = 'N'
    return 0;
  if ( byte_804A020 == 0x78 )                   // byte_20 ^ 0x34 = 0x78
                                                // byte_20 = 0x34^0x78 = 'L'
    return byte_804A023 == 0xDDu;               // byte_23 ^ 0x88 = 0xDD
                                                // byte_23 = 0x88^0xDD = 'U'
  return 0;
}
```
* So our input should be ```L1NUX```
## angr
* This file is simple enough to demonstrate the basic useage of angr
* Also it can be a perfect example of dealing with scanf with angr
### scanf
* Currently, angr cannot deal with scanf, so we need to write a symobols hook to replace it
```python
#pseudo code
class myscanf(angr.SimProcedure):
    def run(self, format_str, param0, param1, ...):
        scanf0 = claripy.BVS("0", sizeof(element) * 8) # The unit of second parameter is bit
        scanf1 = claripy.BVS("1", sizeof(element) * 8)
        ...
        
        self.state.memory.store(param0, scanf0, endness=pro.arch.memory_endness) # If this parameter is storing string, maybe you'd want to make endness='big'
        self.state.memory.store(param1, scanf1, endness=pro.arch.memory_endness)
        ...

        self.state.globals["solutions"] = (scanf0, scanf1, ...)
# Symbol hook
scanf_sym = "__isoc99_scanf"
proj.hook_symbol(scanf_sym, myscanf())

# Solution
if simu.found:
    solve_state = simu.found[0]
    res = solve_state.globals["solutions"]
    flag = b""
    for i in range(len(params)):
        # cast_to only supports for int and bytes
        flag += solve_state.solver.eval(res[i], cast_to=bytes) + b" "
    print(flag)
```

## Flag
```L1NUX```
## References
* [angr with CTF](https://chowdera.com/2021/12/20211205113716864q.html#11_angr_sim_scanf_491)
* [angr with scanf](https://blog.csdn.net/doudoudouzoule/article/details/79977415)