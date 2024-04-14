import cv2 as cv
import numpy as np


def scan(img, w, h):
    img = cv.resize(img, (w, h))
    imgray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    imblur = cv.GaussianBlur(imgray, (5, 5), 0)
    
    # edge detection
    imthresh = cv.Canny(imblur, 0, 50)

    # find all contours
    contours, heirarchy = cv.findContours(imthresh, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv.contourArea, reverse=True)

    biggest = np.array([[[0, 0]], [[w, 0]], [[w, h]], [[0, h]]])
    max_area = 0
    for contour in contours:
        area = cv.contourArea(contour)
        print(area)
        if area > 5000:
            peri = cv.arcLength(contour, True)
            approx = cv.approxPolyDP(contour, 0.02 * peri, True)
            if area > max_area and len(approx) == 4:
                biggest = approx
                max_area = area

    print(biggest)
    return biggest
