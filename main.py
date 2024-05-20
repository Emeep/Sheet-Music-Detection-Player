import PIL.Image
from preprocessing import *
from staff_removal import *
from helper_methods import *
from transcribe import *

import cv2 as cv
import configparser as cp
from PIL import Image
from ultralytics import YOLO

from statistics import mean

path_in = "input/test.png"

config = cp.ConfigParser()
config.read('config.ini')

img = cv.imread(path_in, cv.IMREAD_GRAYSCALE)
# img = resize(img, int(config.get("size", "size"))) # from helper_methods
height, width = img.shape

img = cv2.fastNlMeansDenoising(img, None, 10, 7, 21)
_threshold, in_img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)

staff_lines_thicknesses, staff_lines = get_staff_lines(width, height, in_img, 0.8)
cleaned, staff_coords = remove_staff_lines(in_img, width, staff_lines, staff_lines_thicknesses)

size = int(config.get("size", "size"))
# resize late because resize early causes the staff lines to disappear
scaled, res_percent, border_top = resize(cleaned, size) # from preprocessing
staff_coords = resized_staff_coords(staff_coords, res_percent, border_top)

cv.imwrite('no1.jpg', scaled)
final = Image.fromarray(scaled)

note_list = detect("notehead.pt", final)
aug_list = detect_aug("others.pt", final)
print(aug_list)

notes_dict = get_notes(staff_coords)
pitch_list = get_pitch(notes_dict, note_list)
rest_list = detect("others.pt", final)

all_list = pitch_list + rest_list # "+ lists"
all_list = sorted(all_list, key=lambda x: x[1])
