# CSHOP
## Overview
* 32-bit .Net file
* Use [dnSpy](https://github.com/dnSpy/dnSpy) to decompile .Net file
* After running this executable file, the popup window is empty and doesn't show anyting
## Function Analysis
### FrmMain
* This is the main function
* FrmMain.InitializeComponent is initializing lots of componenet literally, we can take a look and see why nothing shows in the program window
### FrmMain.InitializeComponent
```csharp
private void \uFFFD\uFFFD\uFFFD\uFFFD\uFFFD\uFFFD\uFFFD\uFFFD_Click(object sender, EventArgs e)
{
    this.lbl\u007F\u0014.Text = "W";
    this.lbl\u007F\u000A.Text = "5";
    this.lbl\u007F\u000D.Text = "4";
    this.lbl\u007F\u0011.Text = "R";
    this.lbl\u007F\u0003.Text = "E";
    this.lbl\u007F\u0019.Text = "6";
    this.lbl\u007F\u0015.Text = "M";
    this.lbl\uFFFD\u0014.Text = "I";
    this.lbl\u007F\u000A.Text = "P";
    this.lbl\u007F\u0002.Text = "S";
    this.lbl\uFFFD\u0014.Text = "P";
    this.lbl\u007F\u0015.Text = "6";
    this.lbl\u007F\u0001.Text = "S";
}

this.\uFFFD\uFFFD\uFFFD\uFFFD\uFFFD\uFFFD\uFFFD\uFFFD.Location = new Point(165, 62);
this.\uFFFD\uFFFD\uFFFD\uFFFD\uFFFD\uFFFD\uFFFD\uFFFD.Name = "btnStart";
this.\uFFFD\uFFFD\uFFFD\uFFFD\uFFFD\uFFFD\uFFFD\uFFFD.Size = new Size(0, 0);
this.\uFFFD\uFFFD\uFFFD\uFFFD\uFFFD\uFFFD\uFFFD\uFFFD.TabIndex = 0;
this.\uFFFD\uFFFD\uFFFD\uFFFD\uFFFD\uFFFD\uFFFD\uFFFD.UseVisualStyleBackColor = true;
this.\uFFFD\uFFFD\uFFFD\uFFFD\uFFFD\uFFFD\uFFFD\uFFFD.Click += this.\uFFFD\uFFFD\uFFFD\uFFFD\uFFFD\uFFFD\uFFFD\uFFFD_Click;
```
* The variable name is obfuscated, but this part is still clear
* It's creating a button and when user click on it, it'll call to ```this.\uFFFD\uFFFD\uFFFD\uFFFD\uFFFD\uFFFD\uFFFD\uFFFD_Click```
  * Inside the Click hooked function, it's initializing the value of ```Text``` which will latter showed up in windows
  * We can memorize these values and search for ```Location``` to figure out the right order of flag
* Since the ```Size``` of this button is zero, it's not going to show the button in the program window, so user cannot click on it
  * We can edit the IL instruction with dnSpy to make the size of button larger, so we can click it
  * After clicking on it, the flag will show up
    ![](../img/CSHOP%20-%20size.png)
## Flag
```P4W6RP6SES```