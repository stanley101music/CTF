# Easy Crack
## Overview
* 32-bit PE file
* The function symbols aren't stripped, so it's easy to find WinMain function at 0x401000
## Function Analysis
### WinMain (0x401000)
* It contains only one function, [```DialogBoxParamA```](https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-dialogboxparama)(hInstance, 0x65, 0, DialogFunc, 0)
  ```c
  INT_PTR DialogBoxParamA(
    [in, optional] HINSTANCE hInstance,
    [in]           LPCSTR    lpTemplateName,
    [in, optional] HWND      hWndParent,
    [in, optional] DLGPROC   lpDialogFunc,
    [in]           LPARAM    dwInitParam
  );
  ```
  > Creates a modal dialog box from a dialog box template resource. Before displaying the dialog box, the function passes an application-defined value to the dialog box procedure as the lParam parameter of the WM_INITDIALOG message. An application can use this value to initialize dialog box controls.
* [```lpDialogFunc```](https://docs.microsoft.com/en-us/windows/win32/api/winuser/nc-winuser-dlgproc) is an application-defined callback function and dwInitParam is the parameter sent to this procedure
### DialogFunc (0x401020)
* This function will respond to [windows messages](https://wiki.winehq.org/List_Of_Windows_Messages) with different action
* Our target is sub_401080, which is the only function that will deal with user's input

### sub_401080 (0x401080)
* This function will compare our input with some fixed string and it'll output ```Congratulation !!``` if they matches
* [```GetDlgItemTextA```](https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-getdlgitemtexta)
  ```c
  UINT GetDlgItemTextA(
  [in]  HWND  hDlg,
  [in]  int   nIDDlgItem,
  [out] LPSTR lpString,
  [in]  int   cchMax
  );
  ```
  > Retrieves the title or text associated with a control in a dialog box.
* [```MessageBoxA```](https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-messageboxa)
  ```c
  int MessageBoxA(
    [in, optional] HWND   hWnd,
    [in, optional] LPCSTR lpText,
    [in, optional] LPCSTR lpCaption,
    [in]           UINT   uType
  );
  ```
  > Displays a modal dialog box that contains a system icon, a set of buttons, and a brief application-specific message, such as status or error information. The message box returns an integer value that indicates which button the user clicked.
* Comparison condition
  * ```if ( v3 != 'a' || strncmp(&v4, a5y, 2u) || strcmp(&v5, aR3versing) || String != 'E' )```
  * Since the target string is visible, ```a``` ```5y``` ```R3versing``` ```E```, the only problem remain is the order of these four strings
  * It can be figured out by analyzing the stack address of each variable
      ```c
      CHAR String; // [esp+4h] [ebp-64h]
      char v3; // [esp+5h] [ebp-63h]
      char v4; // [esp+6h] [ebp-62h]
      char v5; // [esp+8h] [ebp-60h]
      ```
  * So the order is ```String -> v3 -> v4 -> v5```
## Flag
```Ea5yR3versing```