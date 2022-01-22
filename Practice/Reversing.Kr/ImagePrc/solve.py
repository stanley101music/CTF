#https://stackoverflow.com/questions/54642772/how-to-create-image-in-python-and-save-it/54644375
import numpy as np
import cv2

f = open('./Manifest101.bin', 'rb')
pixels = f.read()

w = 200
h = 150

img = np.zeros((h, w, 3), np.uint8)
idx = 0
for x in range(h-1,-1,-1):
    for y in range(w):
        pixel = []
        # r,b,g
        for z in range(3):
            pixel.append(pixels[idx])
            idx += 1
        img[x,y] = pixel
cv2.imwrite("Manifest101.png", img)