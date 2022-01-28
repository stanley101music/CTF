#quoted by Optimus Prime
from PIL import Image
prime = [ 2, 3,	5, 7, 11, 13, 17, 19, 23, 29,
		31,	37,	41,	43,	47,	53,	59,	61,	67,	71,
		73,	79,	83, 89, 97,	101, 103, 107, 109,	113,
		127, 131, 137, 139,	149, 151, 157, 163,	167, 173,
		179, 181, 191, 193,	197, 199, 211, 223,	227, 229,
		233, 239, 241, 251 ]
		
im = Image.open("op.png")
newim = Image.new("RGB", (256,256), (255,255,255))
width = im.size[0]
height = im.size[1]
for i in range(width):
	for j in range(height):
		p = im.getpixel((i, j))
		if p[0] in prime:                #Only look at Red and see whether it's a prime number
			newim.putpixel((i,j), p)     
newim.save("newop.png")