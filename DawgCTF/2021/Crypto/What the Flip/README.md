# What the Flip?! (300)

### Description
> Hackers have locked you out of your account! Fortunately their netcat server has a vulnerability.
### Connection
```shell
nc umbccd.io 3000
```
> This netcat server is username and password protected. The admin login is known but forbidden. Any other login entered gives a cipher.

### File
* [app.py](./File/app.py)

### Solution
1. Analyze [app.py](./File/app.py)
2. Encryption
    ```python
    key = get_random_bytes(16)
    iv = get_random_bytes(16)
    def encrypt_data(data):
	padded = pad(data.encode(),16,style='pkcs7')
	cipher = AES.new(key, AES.MODE_CBC,iv)
	enc = cipher.encrypt(padded)
	return enc.hex()
    ```
    * It uses AES CBC mode to encrypt message, with block size 16-bits
3. Input sanitizing
    ```python
    msg = 'logged_username=' + user +'&password=' + passwd

	try:
		assert('admin&password=goBigDawgs123' not in msg)
	except AssertionError:
		send_msg(s, 'You cannot login as an admin from an external IP.\nYour activity has been logged. Goodbye!\n')
		raise
    ```
    * The username and password cannot be admin and goBigDawgs123 at the same time
4. Validation
    ```python
    def decrypt_data(encryptedParams):
	cipher = AES.new(key, AES.MODE_CBC,iv)
	paddedParams = cipher.decrypt( unhexlify(encryptedParams))
	print(paddedParams)
	if b'admin&password=goBigDawgs123' in unpad(paddedParams,16,style='pkcs7'):
		return 1
	else:
		return 0
    #---------------------------------------------------------------------------
    # main
    try:
		check = decrypt_data(enc_msg)
	except Exception as e:
		send_msg(s, str(e) + '\n')
		s.close()

	if check:
		send_msg(s, 'Logged in successfully!\nYour flag is: '+ FLAG)
		s.close()
	else:
		send_msg(s, 'Please try again.')
		s.close()
    ```
    * The validation was performed on the decrypted message instead of the input message
    * The decrypted message should include "admin&password=goBigDawgs123" but doesn't care about other redundant strings
5. According to the challenge's name and the cipher block mode it used, it's apparently we should use [Byte Flipping Attack](https://resources.infosecinstitute.com/topic/cbc-byte-flipping-attack-101-approach/)\
    ![](https://mk0resourcesinf5fwsf.kinstacdn.com/wp-content/uploads/082113_1459_CBCByteFlip3.jpg)
    * Split input into blocks with size 16-bytes
      * "logged_username="
      * "admin&password=g"
      * "oBigDawgs123"
    * The input is actually the start of a block
6. PoC
    * First we modified the first byte of input to change the plaintext to something other than "admin&password=goBigDawgs123"
    * The server will return us with ciphertext where the first byte of second block, i.e., 17th byte, is modified
      * P1 = Dec(C1) ^ IV
      * Pi = Dec(Ci) ^ C{i-1}, for i > 1
    * To make the decryption of ciphertext become "admin&password=goBigDawgs123" again, calculate hex('A')^Enc('l') = Dec(Ci), then hex('a') = Dec(Ci) ^ ?, where ? is the encrypted data we need to send to make the plaintext become 'a' again
      * 'A' is used to replace 'a'
      * ? = hex('a') ^ Dec(Ci) = hex('a') ^ hex('A') ^ Enc('l')
      * ? = hex(\<the target character\>) ^ hex(\<the modified character\>) ^ hex(\<the character with corresponding location of the block before\>)

### Flag
```
DawgCTF{F1ip4J0y}
```
