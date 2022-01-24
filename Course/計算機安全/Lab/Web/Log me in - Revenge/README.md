* Category
  * SQL injection
* Solution
  1. Logic in source.py
    * username needs to be 'admin'
    * the password from users needs to be the same as the value from db
  2. How to select determined value?
    * Make the first query failed by ending it with non-existent username
    * Use ```UNION SELECT``` to choose our own determined value as input to ```get_db()```
* Payload
  1. username = ') UNION SELECT 'admin','SPECIFIED-PASSWORD' --
  2. password = SPECIFIED-PASSWORD
* ```FLAG{un10n_bas3d_sqli}```