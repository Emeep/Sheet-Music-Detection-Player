import cv2 as cv
import os


input_dir = os.listdir('input')

img = cv.imread(f'input/{input_dir[0]}')
w, h = 600, 800
if img.shape[0] < img.shape[1]:
    w, h = 800, 600
img = cv.resize(img, (w, h))

import scan
cv.drawContours(img, scan.scan(img, w, h), -1, (0, 255, 0), 10)
cv.imshow('win', img)

if cv.waitKey(0):
    cv.destroyAllWindows()
    exit()
