# Multiplicative
## Overview
* jar file
* I use [Bytecode Viewer](https://github.com/Konloch/bytecode-viewer) for decompilation, although the decompilation failed, the byte code instructions aren't hard to read
## Function Analysis
```java
public class JavaCrackMe {
     <ClassVersion=51>
     <SourceFile=JavaCrackMe.java>

     public JavaCrackMe() { // <init> //()V
         L1 {
             aload0 // reference to self
             invokespecial java/lang/Object.<init>()V
             return
         }
     }

     public static final synchronized strictfp bridge synthetic varargs main(java.lang.String[] arg0) { //([Ljava/lang/String;)V
         TryCatch: L1 to L2 handled by L3: java/lang/Exception
         L1 {
             getstatic java/lang/System.out:java.io.PrintStream
             ldc "Reversing.Kr CrackMe!!" (java.lang.String)
             invokevirtual java/io/PrintStream.println(Ljava/lang/String;)V
         }
         L4 {
             getstatic java/lang/System.out:java.io.PrintStream
             ldc "-----------------------------" (java.lang.String)
             invokevirtual java/io/PrintStream.println(Ljava/lang/String;)V
         }
         L5 {
             getstatic java/lang/System.out:java.io.PrintStream
             ldc "The idea came out of the warsaw's crackme" (java.lang.String)
             invokevirtual java/io/PrintStream.println(Ljava/lang/String;)V
         }
         L6 {
             getstatic java/lang/System.out:java.io.PrintStream
             ldc "-----------------------------\n" (java.lang.String)
             invokevirtual java/io/PrintStream.println(Ljava/lang/String;)V
         }
         L7 {
             aload0
             iconst_0
             aaload
             invokestatic java/lang/Long.decode(Ljava/lang/String;)Ljava/lang/Long;
             invokevirtual java/lang/Long.longValue()J
             lstore1
         }
         L8 {
             lload1
             ldc 26729 (java.lang.Long)
             lmul
             lstore1
         }
         L9 {
             lload1
             ldc -1536092243306511225 (java.lang.Long)
             lcmp
             ifne L10
         }
         L11 {
             getstatic java/lang/System.out:java.io.PrintStream
             ldc "Correct!" (java.lang.String)
             invokevirtual java/io/PrintStream.println(Ljava/lang/String;)V
             goto L2
         }
         L10 {
             f_new (Locals[2]: [Ljava/lang/String;, 4) (Stack[0]: null)
             getstatic java/lang/System.out:java.io.PrintStream
             ldc "Wrong" (java.lang.String)
             invokevirtual java/io/PrintStream.println(Ljava/lang/String;)V
         }
         L2 {
             f_new (Locals[1]: [Ljava/lang/String;) (Stack[0]: null)
             goto L12
         }
         L3 {
             f_new (Locals[1]: [Ljava/lang/String;) (Stack[1]: java/lang/Exception)
             astore1
         }
         L13 {
             getstatic java/lang/System.out:java.io.PrintStream
             ldc "Please enter a 64bit signed int" (java.lang.String)
             invokevirtual java/io/PrintStream.println(Ljava/lang/String;)V
         }
         L12 {
             f_new (Locals[1]: [Ljava/lang/String;) (Stack[0]: null)
             return
         }
     }
}
```
* There's only one class and two method
* The main logic part is in L7, L8, L9
### L7
```java
L7 {
    aload0
    iconst_0
    aaload
    invokestatic java/lang/Long.decode(Ljava/lang/String;)Ljava/lang/Long;
    invokevirtual java/lang/Long.longValue()J
    lstore1
}
```
* It'll take an our input from commandline argument and stored it as long type
### L8
```java
L8 {
    lload1
    ldc 26729 (java.lang.Long)
    lmul
    lstore1
}
```
* It'll take out the previous stored input and multiply it with 26729
### L9
```java
L9 {
    lload1
    ldc -1536092243306511225 (java.lang.Long)
    lcmp
    ifne L10
}
```
* It'll check if the result of multiplication is equal to -1536092243306511225
* If it matches, Then it'll output "Correct!", otherwise, it'll output "Wrong"

## Overflow
* Although ```-1536092243306511225 % 26729 != 0```, it doesn't mean that it's impossible to find a number such that the equation holds
* Since the size of type long is 64 bits, It's possible that the multiplication of two long variable is larger than 64 bits and leads to overflow
* Our goal is to find a multiple of ```26729``` such that after dealing with overflow, the result becomes ```-1536092243306511225```
  * Bruteforce is enough to solve this problem
* The challenge asked for a 64bit signed int, so we need to convert the result from unsigned int to 64bit signed int
## Flag
```-8978084842198767761```