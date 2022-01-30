# Flare-On 2020 writeup
* [Download challenges](http://flare-on.com/files/Flare-On7_Challenges.zip)
* [Official writeup](https://www.real-sec.com/2020/10/flare-on-7-challenge-solutions/)
## fidler
### Process Analysis
* First stage is to type in the correct password
* Second stage is to gather enough money, and the flag will shows
### Function Analysis
* password_check
    ```python
    def password_check(input):
        altered_key = 'hiptu'
        key = ''.join([chr(ord(x) - 1) for x in altered_key])
        return input == key
    ```
    * This is the function verifying the password
    * Run it locally and the key is our password, which is ```ghost```
* game_screen
    ```python
    target_amount = (2**36) + (2**35)
    if current_coins > (target_amount - 2**20):
        while current_coins >= (target_amount + 2**20):
            current_coins -= 2**20
        victory_screen(int(current_coins / 10**8))
        return
    ```
    * This is part of the ```game_screen``` that reveals our target amount of money is ```(2**36) + (2**35)```
    * setting the ```current_coins``` to the value of ```target_amount``` and run this loop, then we can know the parameter for ```victory_screen```
* victory_screen
    ```python
    def victory_screen(token):
        screen = pg.display.set_mode((640, 160))
        clock = pg.time.Clock()
        heading = Label(20, 20, 'If the following key ends with @flare-on.com you probably won!',
                        color=pg.Color('gold'), font=pg.font.Font('fonts/arial.ttf', 22))
        flag_label = Label(20, 105, 'Flag:', color=pg.Color('gold'), font=pg.font.Font('fonts/arial.ttf', 22))
        flag_content_label = Label(120, 100, 'the_flag_goes_here',
                                color=pg.Color('red'), font=pg.font.Font('fonts/arial.ttf', 32))

        controls = [heading, flag_label, flag_content_label]
        done = False

        flag_content_label.change_text(decode_flag(token))
    ```
    * the ```token``` is the parameter we previously calcualted, and it'll be passed as a parameter to ```decode_flag```
* decode_flag
    ```python
    def decode_flag(frob):
        last_value = frob
        encoded_flag = [1135, 1038, 1126, 1028, 1117, 1071, 1094, 1077, 1121, 1087, 1110, 1092, 1072, 1095, 1090, 1027,
                        1127, 1040, 1137, 1030, 1127, 1099, 1062, 1101, 1123, 1027, 1136, 1054]
        decoded_flag = []

        for i in range(len(encoded_flag)):
            c = encoded_flag[i]
            val = (c - ((i%2)*1 + (i%3)*2)) ^ last_value
            decoded_flag.append(val)
            last_value = c

        return ''.join([chr(x) for x in decoded_flag])
    ```
    * This function will decode our flag and shows it
### Decryption
```python
target_amount = (2**36) + (2**35)
current_coins = (2**36) + (2**35)

while current_coins >= (target_amount + 2**20):
    current_coins -= 2**20
current_coins = int(current_coins / 10**8)

def decode_flag(frob):
    last_value = frob
    encoded_flag = [1135, 1038, 1126, 1028, 1117, 1071, 1094, 1077, 1121, 1087, 1110,  1092, 1072, 1095, 1090, 1027, 1127, 1040, 1137, 1030, 1127, 1099, 1062, 1101, 1123, 1027, 1136, 1054]
    decoded_flag = []
    for i in range(len(encoded_flag)):
        c = encoded_flag[i]
        val = (c - ((i%2)*1 + (i%3)*2)) ^ last_value
        decoded_flag.append(val)
        last_value = c
    return ''.join([chr(x) for x in decoded_flag])

flag = decode_flag(current_coins)
```
### Other method
* You can actually win the game by plaing it in normal way<br>
  ![](img/C1%20-%20flag.png)
### Flag
```idle_with_kitty@flare-on.com```

## 