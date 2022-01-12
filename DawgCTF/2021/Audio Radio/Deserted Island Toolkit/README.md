# Deserted Island Toolkit (150)

### Description
> What would a drunken sailor do? (Wrap the output in DawgCTF{ })

### File
* [DesertedIslandToolkit](./File/DesertedIslandToolkit.zip)

### Tool
* [CyberChef](https://gchq.github.io/CyberChef/#recipe=From_Morse_Code('Space','Line%20feed')&input=Li4uIC0tLS0gLi4uIC4uIC4uLiAtLiAtLS0gLSAtIC4uLi4gLiAuLSAtLiAuLi4uIC4tLSAuLi4tLSAuLS4)
* [CDDA to WAV](https://www.onlineconvert.com/free-cdda-to-wav-converter)

### Solution
1. After unzip the folder, there is a .cdda file in the folder, convert it to wav file and play it
2. It contains a series of short and long tones, which is a pattern of morse code
3. After analyzing it, we can get the morse code as\
    ```... ---- ... .. ... -. --- - - .... . .- -. .... .-- ...-- .-.```
4. Use Cyberchef to decode it and get the flag

### Flag
```
DawgCTF{SSISNOTTHEANHW3R}
```