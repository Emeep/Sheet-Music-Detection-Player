import cv2 as cv
import os

input_dir = os.listdir('input')

img = cv.imread(f'input/Untitled-1.png')

# import imgprep
# import time

# os.chdir('output')
# while True:
#     prepped = imgprep.prep(img)
#     cv.imwrite(f'{str(time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())).replace(".", "").replace(":", "")}.jpg', 
#             prepped)
#     cv.imshow('win', prepped)
