from ultralytics import YOLO
import cv2 as cv

img = cv.imread("input/esgfui.png")

height, width, c = img.shape

border_y = (640 - height)//2
border_x = (640 - width)//2

# top, bottom, left, right
img = cv.copyMakeBorder(img, border_y, border_y, border_x, border_x, cv.BORDER_CONSTANT, None, value = (255,255,255)) 

model = YOLO('best.pt')
results = model.predict(img,
                        conf=0.1, iou=0.01, save=True, show=True, show_labels=False)