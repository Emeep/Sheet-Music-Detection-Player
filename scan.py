import PIL.Image
from preprocessing import *
from staff_removal import *
from helper_methods import *

import cv2 as cv
import configparser as cp
from PIL import Image
from ultralytics import YOLO

path_in = "input/Screenshot 2024-05-11 135411.png"
path_out = "output"

config = cp.ConfigParser()
config.read('config.ini')

img = cv.imread(path_in, cv.IMREAD_GRAYSCALE)
# img = resize(img, int(config.get("size", "size"))) # from helper_methods
height, width = img.shape

img = cv2.fastNlMeansDenoising(img, None, 10, 7, 21)
_threshold, in_img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)

staff_lines_thicknesses, staff_lines = get_staff_lines(width, height, in_img, 0.8)
cleaned = remove_staff_lines(in_img, width, staff_lines, staff_lines_thicknesses)

# resize late because resize early causes the staff lines to disappear
size = resize(cleaned, int(config.get("size", "size"))) # from helper_methods
cv.imwrite("no1.jpg", cleaned)

final = Image.fromarray(size)

model = YOLO('best.pt')
results = model.predict(final,
                        conf=0.1, iou=0.01, save=True, show=True, show_labels=False)

print(results)