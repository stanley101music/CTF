#!/usr/bin/env python3
import cv2      #https://pypi.org/project/opencv-python/

flag_enc = cv2.imread("flag_enc.png", cv2.IMREAD_GRAYSCALE)
golem_enc = cv2.imread("golem_enc.png", cv2.IMREAD_GRAYSCALE)
h, w = flag_enc.shape
for i in range(h):
    for j in range(w):
        flag_enc[i][j] ^= golem_enc[i][j]
cv2.imwrite("flag_xor_golem.png", flag_enc)