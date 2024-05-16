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
cleaned, staff_coords = remove_staff_lines(in_img, width, staff_lines, staff_lines_thicknesses)

size = int(config.get("size", "size"))
# resize late because resize early causes the staff lines to disappear
scaled, res_percent, border_top = resize(cleaned, size) # from preprocessing
staff_coords = resized_staff_coords(staff_coords, res_percent, border_top)

cv.imwrite('no1.jpg', scaled)
final = Image.fromarray(scaled)

model = YOLO('best.pt')
results = model.predict(final,
                        conf=0.1, iou=0.01, save=True, show_labels=False)

boxes = results[0].boxes.xyxy.tolist()
classes = results[0].boxes.cls.tolist()
names = results[0].names
confidences = results[0].boxes.conf.tolist()

# Iterate through the results
for box, cls, conf in zip(boxes, classes, confidences):
    x1, y1, x2, y2 = box
    x1, y1, x2, y2 = round(x1), round(y1), round(x2), round(y2)

    confidence = conf
    detected_class = cls
    name = names[int(cls)]

    print(name, detected_class, confidence, mean((y1, y2)))

print(staff_coords)
print(get_notes(staff_coords))