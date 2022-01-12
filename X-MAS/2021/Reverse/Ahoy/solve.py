import struct
import numpy as np
import scipy.io.wavfile

d1 = {}
for x in range(2048):
    d1[x] = (x**5 + 13 * x**3 + 853 * x) % 2048

inv_d1 = {v: k for k, v in d1.items()}

d2 = {}
for x in range(32):
    d2[x] = (x**5 + 37 * x**3 + 5 * x) % 32

inv_d2 = {v: k for k, v in d2.items()}

def parse(word):
    return (inv_d1[word >> 5], inv_d2[word % 32])

s = 11025
t = 15
with open("./audio_enc.bin", "rb") as f:
    sound = np.zeros(2 * t * s, dtype = np.uint8)
    i = 0
    prev = None
    while True:
        w = f.read(2)
        if not w:
            break

        p,  = struct.unpack("<H", w)#little-endian, unsigned short integer
        dat, offs = parse(p)
        if offs:
            sound[i: i + offs] = prev * np.ones(offs, dtype = np.uint8)
        
        prev = dat
        i += offs

# the last item
sound[i: ] = prev * np.ones(len(sound[i: ]), dtype = np.uint8)

# write the audio file
scipy.io.wavfile.write("./audio.wav", s, sound) 