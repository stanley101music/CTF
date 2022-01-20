# It's Not RSA! (100)

### Description
> Our team intercepted this suspicious JSON file, but the keys don't seem quite right. We suspect this file contains critical data. Due to transmission loss, the format may need to be corrected slightly for our database.

### File
* [intercepted_code.json](./File/intercepted_code.json)

### Tool
* [CyberChef](https://gchq.github.io/CyberChef/#recipe=Enigma('3-rotor','LEYJVCNIXWPBQMDRTAKZGFUHOS','A','A','BDFHJLCPRTXVZNYEIWGAKMUSQO%3CW','C','F','ESOVPZJAYQUIRHXLNFTGKDCMWB%3CK','L','V','EKMFLGDQVZNTOWYHXUSPAIBRCJ%3CR','F','M','AY%20BR%20CU%20DH%20EQ%20FS%20GL%20IP%20JX%20KN%20MO%20TZ%20VW','AU%20CB%20GI%20ZX%20YQ%20OS%20FE',true)&input=ZXZnbmd1ZXh0bGl3Y21uZHlwemRuaGJzaHJhY3JucHo)

### Solution
1. The file is actually the configuration of [Enigma](https://en.wikipedia.org/wiki/Enigma_machine)
2. Notice the format of output needs to be slightly modified

### Flag
```
DawgCTF{spinningandrotatingrotors}
```