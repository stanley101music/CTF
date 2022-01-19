# CTF Container
Hope this document can help people to custom their own container for ctf environment
## Description
* This Dockerfile is modified from u1f383's [Dockerfile](https://github.com/u1f383/Software-Security-2021/blob/master/Dockerfile)
* It might take a long time to build the image due to the amounts of tools. You can delete those commands in Dockerfile to avoid installing unwanted tools

:warning: I've made a symlink for ```/usr/bin/python3``` as ```/usr/bin/python``` to run sqlmap globally. If you need ```/usr/bin/python``` to be interpreted as python2 or you don't need sqlmap to run globally, you can delete this command in Dockerfile
## Tools
Most tools can be runned globally
### Crypto
These tools are located in /Crypto folder
* [xortool](https://github.com/hellman/xortool)
* [RsaCtfTool](https://github.com/Ganapati/RsaCtfTool)
* [HashPump](https://github.com/bwall/HashPump)
* [hashcat](https://github.com/hashcat/hashcat)
* [BaseCrack](https://github.com/mufeedvh/basecrack)
  * This is the only tool that can not be runned globally

### Web
These tools are located in /Web folder
* [nmap](https://nmap.org/)
* [scrabble](https://github.com/denny0223/scrabble)
* [sqlmap](https://sqlmap.org/)

### Reverse
* [radare2](https://github.com/radareorg/radare2)
* [ltrace](https://ltrace.org/)
* [strace](https://strace.io/)

### Pwn
* [gdb](https://www.sourceware.org/gdb/)
  * [pwndbg](https://github.com/pwndbg/pwndbg) + [pwngdb](https://github.com/scwuaptx/Pwngdb)
    * ```$ gdb-pwndbg```
  * [peda](https://github.com/longld/peda)
    * ```$ gdb-peda```
  * [gef](https://github.com/hugsy/gef)
    * ```$ gdb-gef```
  * The configuration file ```.gdbinit``` is located at [```gdb_config```](./gdb_config/.gdbinit)
    * Three different commands to run your preferred extension of gdb
    * Some syntax hilighting colors are modified for better experience, especially for terminals that aren't good at rendering dark blue
  * You can learn more about the settings in [this blog](https://infosecwriteups.com/pwndbg-gef-peda-one-for-all-and-all-for-one-714d71bf36b8)
* [pwntools 4.4.0](https://github.com/Gallopsled/pwntools/tree/stable)
* [Seccomp Tools](https://github.com/david942j/seccomp-tools)
* [OneGadget](https://github.com/david942j/one_gadget)
* [ROPGadget](https://github.com/JonathanSalwan/ROPgadget)

### Forensics
These tools are located in /Forensics folder<br>
I'd recommend using kali linux vm for forensics since there're many powerful built-in tools that can handle this kind of challenges
* [exiftool](https://exiftool.org/)
* [binwalk](https://github.com/ReFirmLabs/binwalk)
* [foremost](http://foremost.sourceforge.net/)
* [fcrackzip](http://oldhome.schmorp.de/marc/fcrackzip.html)
* [pngcheck](http://www.libpng.org/pub/png/apps/pngcheck.html)

## Installation & Usage
* build image
  * ```$ mkdir ctf && docker build -t ctfbox .```
    * create a directory named "ctf" at current location
    * build with Dockerfile and name the image "ctfbox
* create container
  * linux platform
    * ```$ docker run -it -d --cap-add=SYS_PTRACE --name ctfbox -v `pwd`/ctf:/ctf ctfbox```
  * windows platform
    * ```$ docker run -it -d --cap-add=SYS_PTRACE --name ctfbox -v "%cd%"/ctf:/ctf ctfbox```
  * run with debugging enabled and name the container "ctfbox"
  * the previous created direcotry "ctf" is served as a volumn which maps to ```/ctf``` in the container
* ```$ docker exec -it ctfbox fish```
  * open an interactive fish shell
* ```$ docker stop ctfbox```
  * stop the container

## Working with [Windows Terminal](https://www.microsoft.com/zh-tw/p/windows-terminal/9n0dx20hk701)
```json
{
    "commandline": "docker exec -it ctfbox fish",
    "guid": "{a25a83da-5bd2-4c68-97b8-a8720a80cff7}",
    "icon": "\ud83d\udc33",
    "name": "ctfbox",
    "suppressApplicationTitle": true
}
```
* guid can be set to any unique value in the same format

## Lessons Learned
1. Be careful of using [```COPY```](https://docs.docker.com/engine/reference/builder/#copy) command in Dockerfile
   * Don't use relative symbols like ```~```, ```.``` in tha path of destination
   * Make sure you understand what is [context directory](https://stackoverflow.com/questions/63455621/copy-failed-stat-var-lib-docker-tmp-docker-xxx-no-such-file-or-directory) in docker and how it'll affect the value of arguments in ```COPY```
2. Make good use of [```WORKDIR```](https://docs.docker.com/engine/reference/builder/#workdir)
3. [How to mount a local volume that contains invalid characters in Windows](https://stackoverflow.com/questions/35767929/using-docker-via-windows-console-includes-invalid-characters-pwd-for-a-local-v)
4. Note the difference in newline between Windows (CR LF) and Unix (LF)
   * Notepad++ can change the format by  ```編輯 -> 換行格式```
   * It can also determine the entire file's format by ```設定 -> 偏好設定 -> 新文件預設設定```
5. How to configure gdb
6. How to [configure vim theme](https://unix.stackexchange.com/questions/88879/better-colors-so-comments-arent-dark-blue-in-vim)
7. How to [change the result's color of command ```ls``` by setting .dircolors](https://askubuntu.com/questions/466198/how-do-i-change-the-color-for-directories-with-ls-in-the-console)
   * Not implemented in these project 