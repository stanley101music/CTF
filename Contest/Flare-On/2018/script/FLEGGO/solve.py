import glob
import subprocess

def start(executable_file):
    return subprocess.Popen(
        executable_file,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE)

def read(process):
	return process.stdout.readline().decode('utf-8').strip()
		
def write(process, message):
    process.stdin.write(message + b'\n')
    process.stdin.flush()

FLEGGO = []
files = glob.glob('./*.exe')
for file in files:
	# Dump password
	f = open(file, 'rb')
	fcontent = f.read()
	BRICK = fcontent[0x2AB0: 0x2AD0]
	password = BRICK.replace(b'\x00', b'')
	#print(password)	
	
	# Send password to each process
	process = start(file)
	write(process, password)
	read(process)
	read(process)
	key, value = read(process).split(' => ')
	FLEGGO.append(value)
	f.close()

order = [7, 35, 1, 3, 24, 18, 47, 4, 28, 21, 48, 46, 30, 11, 36, 41, 27, 25, 19, 45, 14, 6, 37, 23, 16, 2, 17, 5, 9, 15, 8, 13, 40, 29, 38, 31, 26, 12, 42, 10, 32, 22, 39, 34, 44, 43, 33, 20]

flag = "".join([ele for _, ele in sorted(zip(order, FLEGGO))])
print(flag)