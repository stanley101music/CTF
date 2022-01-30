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