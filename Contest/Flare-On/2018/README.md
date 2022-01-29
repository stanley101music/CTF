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