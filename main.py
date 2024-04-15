import cv2 as cv
import os

input_dir = os.listdir('input')

img = cv.imread(f'input/{input_dir[0]}')

import imgprep
cv.imshow('win', imgprep.prep(img))

if cv.waitKey(0):
    cv.destroyAllWindows()
    exit()
