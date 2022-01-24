* Category
  * Broken Access Control
  * Bussiness Logic Vulnerabilities
* Solution
  1. How to traverse to FLAG buying page?
      * Observe other object's buying page
      * They are all under ```http://splitline.tw:8100/item/****```, where ```****``` are digits
      * The number's order is same with the object's presentation order
        * In this case, 5430
  2. How to buy FLAG with limited money?
      * Modify the FLAG's money and press Buy!
        * ```<input type="hidden" name="cost" value="desired money">```
* ```FLAG{omg_y0u_hack3d_th3_c4t_sh0p!}```