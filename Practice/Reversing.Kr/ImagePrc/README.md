# ImagePrc
## Overview
* 32-bit PE file
* The function symbols aren't stripped, so it's easy to find WinMain function at 0x401000
* It has GUI
## Function Analysis
### WinMain (0x401000)
```c
int __stdcall WinMain(HINSTANCE hInstance, HINSTANCE hPrevInstance, LPSTR lpCmdLine, int nShowCmd)
{
  int v4; // ST14_4
  int v5; // eax
  HWND v6; // eax
  struct tagMSG Msg; // [esp+4h] [ebp-44h]
  WNDCLASSA WndClass; // [esp+20h] [ebp-28h]

  ::hInstance = hInstance;
  WndClass.cbClsExtra = 0;
  WndClass.cbWndExtra = 0;
  WndClass.hbrBackground = (HBRUSH)GetStockObject(0);
  WndClass.hCursor = LoadCursorA(0, (LPCSTR)0x7F00);
  WndClass.hInstance = hInstance;
  WndClass.hIcon = LoadIconA(0, (LPCSTR)0x7F00);
  WndClass.lpfnWndProc = sub_401130;
  WndClass.lpszClassName = lpWindowName;
  WndClass.lpszMenuName = 0;
  WndClass.style = 3;
  RegisterClassA(&WndClass);
  v4 = GetSystemMetrics(1) / 2 - 75;
  v5 = GetSystemMetrics(0);
  v6 = CreateWindowExA(0, lpWindowName, lpWindowName, 0xCA0000u, v5 / 2 - 100, v4, 200, 150, 0, 0, hInstance, 0);
  ShowWindow(v6, 5);
  if ( !GetMessageA(&Msg, 0, 0, 0) )
    return Msg.wParam;
  do
  {
    TranslateMessage(&Msg);
    DispatchMessageA(&Msg);
  }
  while ( GetMessageA(&Msg, 0, 0, 0) );
  return Msg.wParam;
}
```
* This function is a good example for understnading a window program
* [```WNDCLASSA```](https://docs.microsoft.com/en-us/windows/win32/api/winuser/ns-winuser-wndclassa)
  ```c
  typedef struct tagWNDCLASSA {
    UINT      style;
    WNDPROC   lpfnWndProc;
    int       cbClsExtra;
    int       cbWndExtra;
    HINSTANCE hInstance;
    HICON     hIcon;
    HCURSOR   hCursor;
    HBRUSH    hbrBackground;
    LPCSTR    lpszMenuName;
    LPCSTR    lpszClassName;
  } WNDCLASSA, *PWNDCLASSA, *NPWNDCLASSA, *LPWNDCLASSA;
  ```
  > Contains the window class attributes that are registered by the RegisterClass function.
  > 
  > This structure has been superseded by the WNDCLASSEX structure used with the RegisterClassEx function. You can still use WNDCLASS and RegisterClass if you do not need to set the small icon associated with the window class.
  * ```style```
      * The class style(s)
      * [Window Class Styles List](https://docs.microsoft.com/en-us/windows/win32/winmsg/window-class-styles)
      * 3 = 0x2 | 0x1
      * 0x2 = CS_HREDRAW
        > Redraws the entire window if a movement or size adjustment changes the width of the client area.
      * 0x1 = CS_VREDRAW
        > Redraws the entire window if a movement or size adjustment changes the height of the client area.
  * ```lpfnWndProc```
      * A pointer to the [window procedure](https://docs.microsoft.com/en-us/windows/win32/winmsg/window-procedures)
        > Every window has an associated window procedure — a function that processes all messages sent or posted to all windows of the class. All aspects of a window's appearance and behavior depend on the window procedure's response to these messages.
  * ```cbClsExtra```
      * The number of extra bytes to allocate following the window-class structure
      * The system initializes the bytes to zero
  * ```cbWndExtra```
      * The number of extra bytes to allocate following the window instance
      * The system initializes the bytes to zero
  * ```hInstance```
      * A handle to the instance that contains the window procedure for the class
  * ```hIcon```
      * A handle to the class icon
      * This member must be a handle to an icon resource
      * If this member is NULL, the system provides a default icon
      * [```LoadIconA```](https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-loadicona)
        ```c
        HICON LoadIconA(
            [in, optional] HINSTANCE hInstance,
            [in]           LPCSTR    lpIconName
        );
        ```
        > Loads the specified icon resource from the executable (.exe) file associated with an application instance.
        * 0 = NULL
            > A standard icon is being loaded
        * 0x7F00 = 32512 = IDI_APPLICATION
            > Default application icon
  * ```hCursor```
      * A handle to the class cursor
      * This member must be a handle to a cursor resource
      * If this member is NULL, an application must explicitly set the cursor shape whenever the mouse moves into the application's window
      * [```LoadCursorA```](https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-loadcursora)
        ```c
        HCURSOR LoadCursorA(
            [in, optional] HINSTANCE hInstance,
            [in]           LPCSTR    lpCursorName
        );
        ```
        > Loads the specified cursor resource from the executable (.EXE) file associated with an application instance.
        * 0x7F00 = 32512 = IDC_ARROW
            > Standard arrow
  * ```hbrBackground```
      * A handle to the class background brush
      * This member can be a handle to the physical brush to be used for painting the background, or it can be a color value
      * [```GetStockObject```](https://docs.microsoft.com/en-us/windows/win32/api/wingdi/nf-wingdi-getstockobject)
        ```c
        HGDIOBJ GetStockObject(
            [in] int i
        );
        ```
        > The GetStockObject function retrieves a handle to one of the stock pens, brushes, fonts, or palettes
        * 0 = WHITE_BRUSH
            > White brush.
  * ```lpszMenuName```
      * The resource name of the class menu, as the name appears in the resource file
      * If this member is NULL, windows belonging to this class have no default menu
  * ```lpszClassName```
      * A pointer to a null-terminated string or is an atom
  * So after ```RegisterClassA(&WndClass)```, It's going to register a window with following attributes
    * ClassName = "ImagePrc"
    * No menu name
    * White background
    * Cursor = standard arrow
    * Icon = default application icon
    * Instance is this process
    * No extra bytes for window-class structure and instance
    * The windows procedure = sub_401130
    * Class style = HREDRAW | VREDRAW
    * Among all of them the windows procedure is the most important during reversing to figure out what it's going to deal with user input
* [```GetSystemMetrics```](https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-getsystemmetrics)
  ```c
  int GetSystemMetrics(
    [in] int nIndex
  );
  ```
  > Retrieves the specified system metric or system configuration setting.
  >
  > Note that all dimensions retrieved by GetSystemMetrics are in pixels.
  * 1 = SM_CYSCREEN
    > The height of the screen of the primary display monitor, in pixels.
  * 0 = SM_CXSCREEN
    > The width of the screen of the primary display monitor, in pixels.
* [```CreateWindowExA```](https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-createwindowexa)
  ```c
  HWND CreateWindowExA(
    [in]           DWORD     dwExStyle,
    [in, optional] LPCSTR    lpClassName,
    [in, optional] LPCSTR    lpWindowName,
    [in]           DWORD     dwStyle,
    [in]           int       X,
    [in]           int       Y,
    [in]           int       nWidth,
    [in]           int       nHeight,
    [in, optional] HWND      hWndParent,
    [in, optional] HMENU     hMenu,
    [in, optional] HINSTANCE hInstance,
    [in, optional] LPVOID    lpParam
  );
  ```
  > Creates an overlapped, pop-up, or child window with an extended window style
  * ```dwStyle```
    * The style of the window being created
    * [Window Styles List](https://docs.microsoft.com/en-us/windows/win32/winmsg/window-styles)
    * 0xCA0000 = 0xC00000 | 0x080000 | 0x020000
      * 0xC00000 = WS_CAPTION
        > The window has a title bar
      * 0x080000 = WS_SYSMENU
        > The window has a window menu on its title bar
      * 0x020000 = WS_GROUP/WS_MINIMIZEBOX
        > The window is the first control of a group of controls
        > 
        > The window has a minimize button
  * ```X```
    * The initial horizontal position of the window
  * ```Y```
    * The initial vertical position of the window
* [```ShowWindow```](https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-showwindow)
  ```c
  BOOL ShowWindow(
    [in] HWND hWnd,
    [in] int  nCmdShow
  );
  ```
  > Sets the specified window's show state.
  * ```nCmdShow```
    * Controls how the window is to be shown
    * 5 = SW_SHOW
      > Activates the window and displays it in its current size and position.
* [Window Message Loop](https://docs.microsoft.com/en-us/windows/win32/winmsg/about-messages-and-message-queues#message-loop)
  ```c
  MSG msg;
  BOOL bRet;

  while( (bRet = GetMessage( &msg, NULL, 0, 0 )) != 0)
  { 
      if (bRet == -1)
      {
          // handle the error and possibly exit
      }
      else
      {
          TranslateMessage(&msg); 
          DispatchMessage(&msg); 
      }
  }
  ```
  * [```GetMessage```](https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-getmessage)
    * The GetMessage function retrieves a message from the queue and copies it to a structure of type MSG
    * It returns a nonzero value, unless it encounters the WM_QUIT message, in which case it returns FALSE and ends the loop
    * If you specify a window handle as the second parameter of GetMessage, only messages for the specified window are retrieved from the queue
  * [```TranslateMessage```](https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-translatemessage)
    * A thread's message loop must include TranslateMessage if the thread is to receive character input from the keyboard
    * The system generates virtual-key messages (WM_KEYDOWN and WM_KEYUP) each time the user presses a key
    * TranslateMessage translates the virtual-key message into a character message (WM_CHAR) and places it back into the application message queue
  * [```DispatchMessage```](https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-dispatchmessage)
    * The DispatchMessage function sends a message to the window procedure associated with the window handle specified in the MSG structure
    * If the window handle is NULL, DispatchMessage does nothing with the message
  * An application's main thread starts its message loop after initializing the application and creating at least one window
  * After it is started, the message loop continues to retrieve messages from the thread's message queue and to dispatch them to the appropriate windows
  * Only one message loop is needed for a message queue, even if an application contains many windows

* Before we jump into analyze the window procedure (sub_401130), let's first check what this process is doing

## Process Analysis
![](../img/ImagePrc%20-%20wrong.png)
* User can draw anything in the window and after clicking the Check button, it'll popup a new window and tell you if the paint you drew is correct or wrong
* So, we know we're looking for comparison in the program, and we want to find out what it's compared to
* Moreover, if the comparison fails, it'll popup a new window with Wrong

## Function Analysis
### sub_401130 (0x401130)
```c
if ( wParam == 100 )
{
    GetObjectA(hbm, 24, &pv);
    memset(&bmi, 0, 0x28u);
    bmi.bmiHeader.biHeight = cLines;
    bmi.bmiHeader.biWidth = v16;
    bmi.bmiHeader.biSize = 40;
    bmi.bmiHeader.biPlanes = 1;
    bmi.bmiHeader.biBitCount = 24;
    bmi.bmiHeader.biCompression = 0;
    GetDIBits(hdc, (HBITMAP)hbm, 0, cLines, 0, &bmi, 0);
    v8 = operator new(bmi.bmiHeader.biSizeImage);
    GetDIBits(hdc, (HBITMAP)hbm, 0, cLines, v8, &bmi, 0);
    v9 = FindResourceA(0, (LPCSTR)0x65, (LPCSTR)0x18);
    v10 = LoadResource(0, v9);
    v11 = LockResource(v10);
    v12 = 0;
    v13 = v8;
    v14 = v11 - (_BYTE *)v8;
    while ( *v13 == v13[v14] )
    {
        ++v12;
        ++v13;
        if ( v12 >= 90000 )
        {
            sub_401500(v8);
            return 0;
        }
    }
    MessageBoxA(hWnd, Text, Caption, 0x30u);  // Text = Wrong
    sub_401500(v8);
    return 0;
}
```
* With the previous mentioned conditions, we can find our target faster
  * There's a while loop keep doing the verification
  * A MessageBoxA with Text = Wrong
* It's comparing our paint to a Resource loaded by ```FindResourceA(0, (LPCSTR)0x65, (LPCSTR)0x18)``` and ```LoadResource(0, v9)```
  * We can use [Resource Hacker](http://www.angusj.com/resourcehacker/) to dump this [resource](./Manifest101.bin)
  * Resource Hacker will labeled each resource with it's ID which is the value of second parameter of FindResourceA. In this case, it's 0x65 = 101. Thus, we can find out which resource is our target file<br>
    ![](../img/ImagePrc%20-%20resource.png)
* After getting the resource, we need to recreate an image file from this resource file, and we already know the width and hight from WinMain function where width = 200 and hight = 150
  * Write a python script to reconstruct the image and we'll get the flag<br>
    ![](./Manifest101.png)
## Flag
```GOT```
## References
* [Windows Programming - Message Loop Architecture](https://en.wikibooks.org/wiki/Windows_Programming/Message_Loop_Architecture)
* [How to create image in python](https://stackoverflow.com/questions/54642772/how-to-create-image-in-python-and-save-it/54644375)