# Flare-On 2019 writeup
* [Download challenges](http://flare-on.com/files/Flare-On6_Challenges.zip)
* [Official wirteup](https://www.mandiant.com/resources/2019-flare-on-challenge-solutions)
## MemeCatBattlestation
> This is a simple game. Reverse engineer it to figure out what "weapon codes" you need to enter to defeat each of the two enemies and the victory screen will reveal the flag. Enter the flag here on this site to score and move on to the next level.
### File Analysis
* Portable Executable 32 .NET Assembly
### Function Analysis
* As the challenge's description says, we need to find out what is te "weapon codes"
* Stage1Form::FireButton_Click(object sender, EventArgs e)
    ```csharp
    private void FireButton_Click(object sender, EventArgs e)
    {
        if (this.codeTextBox.Text == "RAINBOW")
        {
            this.fireButton.Visible = false;
            this.codeTextBox.Visible = false;
            this.armingCodeLabel.Visible = false;
            this.invalidWeaponLabel.Visible = false;
            this.WeaponCode = this.codeTextBox.Text;
            this.victoryAnimationTimer.Start();
            return;
        }
        this.invalidWeaponLabel.Visible = true;
        this.codeTextBox.Text = "";
    }
    ```
    * The weapon codes for the first stage is ```RAINBOW```
* Stage2Form::isValidWeaponCode(string s)
    ```csharp
    private bool isValidWeaponCode(string s)
    {
        char[] array = s.ToCharArray();
        int length = s.Length;
        for (int i = 0; i < length; i++)
        {
            char[] array2 = array;
            int num = i;
            array2[num] ^= 'A';
        }
        return array.SequenceEqual(new char[]
        {
            '\u0003',
            ' ',
            '&',
            '$',
            '-',
            '\u001e',
            '\u0002',
            ' ',
            '/',
            '/',
            '.',
            '/'
        });
    }
    ```
    * It's xor our inputs with ```A``` and compre the result to a new array
    * decryption
      ```python
      cipher = b'\x03 &$-\x1e\x02 //./'
      weapon_code = ""
      for c in cipher:
          weapon_code += chr(c ^ ord('A'))
      ```
      * weapon code is ```Bagel_Cannon```
* After passing these two stages, it'll output the flag<br>
  ![](img/C1%20-%20flag.png)
### Flag
```Kitteh_save_galixy@flare-on.com```

## Overlong
### Process Analysis
* After running the program<br>
  ![](img/C2%20-%20broken.png)
  * Nothing interesting shows
### Function Analysis
* start function (0x4011C0)
    ```c
    int __stdcall start(int a1, int a2, int a3, int a4)
    {
        unsigned int v4; // eax
        char Text[128]; // [esp+0h] [ebp-84h]
        unsigned int v7; // [esp+80h] [ebp-4h]

        v4 = sub_401160(Text, (int)&unk_402008, 0x1Cu);
        v7 = v4;
        Text[v4] = 0;
        MessageBoxA(0, Text, Caption, 0);
        return 0;
    }
    ```
    * It'll call ```MessageBoxA``` and output the strings stored in ```Text```
* sub_401160
    ```c
    unsigned int __cdecl sub_401160(char *a1, int a2, unsigned int a3)
    {
        int v3; // ST08_4
        unsigned int i; // [esp+4h] [ebp-4h]

        for ( i = 0; i < a3; ++i )
        {
            a2 += sub_401000(a1, (unsigned __int8 *)a2);
            v3 = *a1++;
            if ( !v3 )
            break;
        }
        return i;
    }
    ```
    * It's decryption the value from ```a2```, which is ```unk_402008```, with length ```a3```, which is ```0x1C```
* ```unk_402008```
  * This location actually holds data size larger than 0x1C<br>
    ![](img/C2%20-%20start.png)<br>
    ![](img/C2%20-%20end.png)
    * The length is ```0xAF```
    * Run the program again while setting the parameter from ```0x1C``` to ```0xAF``` and the flag will show up<br>
      ![](img/C2%20-%20flag.png)
### Flag
```I_a_M_t_h_e_e_n_C_o_D_i_n_g@flare-on.com```