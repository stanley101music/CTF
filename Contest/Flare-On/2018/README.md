# Flare-On 2018 writeup
* [Download challenges](https://flare-on.com/files/Flare-On5_Challenges.zip)
* [Official writeup](https://www.mandiant.com/resources/2018-flare-on-challenge-solutions)
## Minesweeper Championship Registration
### File Analysis
* This is a ```jar``` file
### Function Analysis
* I use [Bytecode Viewer](https://github.com/Konloch/bytecode-viewer) to decompile the java byte code
    ```java
    import java.awt.Component;
    import javax.swing.JOptionPane;

    public class InviteValidator {
        public static void main(String[] args) {
            String response = JOptionPane.showInputDialog((Component)null, "Enter your invitation code:", "Minesweeper Championship 2018", 3);
            if (response.equals("GoldenTicket2018@flare-on.com")) {
                JOptionPane.showMessageDialog((Component)null, "Welcome to the Minesweeper Championship 2018!\nPlease enter the following code to the ctfd.flare-on.com website to compete:\n\n" + response, "Success!", -1);
            } else {
                JOptionPane.showMessageDialog((Component)null, "Incorrect invitation code. Please try again next year.", "Failure", 0);
            }

        }
    }
    ```
### Flag
```GoldenTicket2018@flare-on.com```

## Ultimate Minesweeper
### File Analysis
* Portable Executable 32 .NET Assembly
### Process Analysis
* It's a minesweeper game but with 897 mines<br>
  ![](img/UM%20-%20start.png)
  * You need to be very lucky to win the game by playing in normal way
### Function Analysis
* MainForm::MainForm()
    ```csharp
    public MainForm()
        {
            this.InitializeComponent();
            this.MineField = new MineField(MainForm.VALLOC_NODE_LIMIT);
            this.AllocateMemory(this.MineField);
            this.mineFieldControl.DataSource = this.MineField;
            this.mineFieldControl.SquareRevealed += this.SquareRevealedCallback;
            this.mineFieldControl.FirstClick += this.FirstClickCallback;
            this.stopwatch = new Stopwatch();
            this.FlagsRemaining = this.MineField.TotalMines;
            this.mineFieldControl.MineFlagged += this.MineFlaggedCallback;
            this.RevealedCells = new List<uint>();
        }
    ```
    * This is the first function called to do the initilization
    * ```InitializeComponent``` doesn't deal with the mines
    * ```AllocateMemory``` will set some attributes on each block
* MainField::AllocateMemory(MineField mf)
    ```csharp
    private void AllocateMemory(MineField mf)
    {
        for (uint num = 0U; num < MainForm.VALLOC_NODE_LIMIT; num += 1U)
        {
            for (uint num2 = 0U; num2 < MainForm.VALLOC_NODE_LIMIT; num2 += 1U)
            {
                bool flag = true;
                uint r = num + 1U;
                uint c = num2 + 1U;
                if (this.VALLOC_TYPES.Contains(this.DeriveVallocType(r, c)))
                {
                    flag = false;
                }
                mf.GarbageCollect[(int)num2, (int)num] = flag;
            }
        }
    }
    ```
    * This part is setting the flag of each block, this flag might be the one determinig whether this block is a mine or not
    * At first, I thought that ```flag = false``` means this block is a mine, but after a few test, it turns out that when ```flag = false``` denotes the block is not a mine
    * Set a breakpoint at ```flag = false``` to figure out which three blocks aren't mine<br>
      ![](img/UM%20-%201.png)<br>
      ![](img/UM%20-%202.png)<br>
      ![](img/UM%20-%203.png)
      * Now, if we click this threee blocks then we can we the game
      * However, calculating the position of blocks are bothering. Instead, we can click any places and set a breakpoint where the program is judging the position and modify the value
* MineFieldControl::MineFieldControl_MouseClick(object sender, MouseEventArgs e)
    ```csharp
    private void MineFieldControl_MouseClick(object sender, MouseEventArgs e)
    {
        uint num = Convert.ToUInt32(e.Y / this.CellSize);
        uint num2 = Convert.ToUInt32(e.X / this.CellSize);
        if (e.Button == MouseButtons.Right)
        {
            bool flag = this.DataSource.MinesFlagged[(int)num2, (int)num];
            this.DataSource.MinesFlagged[(int)num2, (int)num] = !flag;
            base.Invalidate();
            if (this.MineFlagged != null)
            {
                this.MineFlagged(!flag);
            }
        }
        else if (e.Button == MouseButtons.Left)
        {
            bool flag2 = this.DataSource.MinesVisible[(int)num2, (int)num];
            this.DataSource.MinesVisible[(int)num2, (int)num] = true;
            base.Invalidate();
            if (!flag2 && this.SquareRevealed != null)
            {
                this.SquareRevealed(num2, num);
            }
        }
        if (!this.firstClickHappened && this.FirstClick != null && (e.Button == MouseButtons.Left || e.Button == MouseButtons.Right))
        {
            this.firstClickHappened = true;
            this.FirstClick();
        }
    }
    ```
    * we can set a breakpoint after it calculates the value of ```num``` and ```num2``` and then modify their values to meet the condition
      ![](img/UM%20-%20win.png)
### Flag
```Ch3aters_Alw4ys_W1n@flare-on.com```

## FLEGGO
* This challenge contains 48 executable files
* All of them are similar
### Function Analysis (1BpnGjHOT7h5vvZsV4vISSb60Xj3pX5G.exe)
* main (0x401300)
    ```c
    int __cdecl main(int argc, const char **argv, const char **envp)
    {
        int result; // eax
        __int128 v4; // [esp+0h] [ebp-24h]
        __int128 v5; // [esp+10h] [ebp-14h]

        v4 = 0i64;
        v5 = 0i64;
        sub_4012D0(0, DWORD1(v4), 0i64 >> 63, 0i64 >> 96, 0, DWORD1(v5), 0i64 >> 63, 0i64 >> 96);
        if ( sub_401050() )
        {
            printf(L"What is the password?\n");
            scanf(L"%15ls", &v4, 16);
            if ( compare_401240(&v4) )
            {
                sub_4010B0();
                if ( sub_401100() )
                {
                    printf(L"Everything is awesome!\n");
                    printf(L"%s => %s\n", &unk_4043A0, &unk_4043C0);
                    result = word_4043CA;
                }
                else
                {
                    printf(L"Oh look a rainbow.\n");
                    result = -1;
                }
            }
            else
            {
                printf(L"Go step on a brick!\n");
                result = -1;
            }
        }
        else
        {
            printf(L"I super hate you right now.\n");
            result = -1;
        }
        return result;
    }
    ```
    * We've to provide a password with length <= 15
    * ```compare_401240``` will determine whether our password is correct
      * The return value of this function should be non-zero
* compare_401240 (0x401240)
    ```c
    BOOL __thiscall sub_401240(const unsigned __int16 *this)
    {
        int v1; // eax
        BOOL result; // eax
        int v3; // kr00_4

        v1 = wcscmp(this, L"IronManSucks");
        if ( v1 )
            v1 = -(v1 < 0) | 1;
        if ( v1 )
        {
            v3 = wcscmp(this, &unk_404380);
            if ( v3 )
                result = (-(v3 < 0) | 1) == 0;
            else
                result = 1;
        }
        else
        {
            printf(L"Oh, hello Batman...\n");
            result = 0;
        }
        return result;
    }
    ```
    * Although it first compares our input with ```IronManSucks```, the return value for this condition is 0, which is not a non-zero value
    * The real password is at ```unk_404380```, however, it's unknown<br>
      ![](img/FL%20-%20unknown.png)
      * Search for cross-references to see where it's value is assigned<br>
        ![](img/FL%20-%20x1.png)<br>
        ![](img/FL%20-%20x2.png)
        * The value comes from the resource named ```BRICK```
        * Thus, our password is the first 15 bytes of resource ```BRICK```
    * ```BRICK```<br>
      ![](img/FL%20-%20brick.png)
### Process Analysis
* After sending the correct password, it'll generate an image and output a character
  ![](img/65141174.png)
* Write a script to extract and send all the correct passwords to each executable file, and see what are the generated images and output character<br>
  ![](img/FL%20-%20pass.png)
* Like the first image, each picture has a number at the top left corner, which might be the order of output character we got from the program
* Reorder the character with this information and we can get the flag
### Flag
```mor3_awes0m3_th4n_an_awes0me_p0ssum@flare-on.com```
### Reference
* [Interactive input/output using Python](https://stackoverflow.com/questions/19880190/interactive-input-output-using-python)