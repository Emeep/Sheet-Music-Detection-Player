import cv2 as cv
import numpy as np


def scan(img, w, h):
    img = cv.resize(img, (w, h))
    imgray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    imblur = cv.GaussianBlur(imgray, (5, 5), 0)
    
    # edge detection
    imthresh = cv.Canny(imblur, 0, 50)

    # find biggest contours
    contours, heirarchy = cv.findContours(imthresh, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv.contourArea, reverse=True)

    win = np.array([[[0, 0]], [[w, 0]], [[w, h]], [[0, h]]])
    biggest = win
    contour = contours[0]
    area = cv.contourArea(contour)
    for i in contours:
        print(cv.contourArea(i))

    if area > 200:
        approx = cv.approxPolyDP(contour, 0.02 * cv.arcLength(contour, True), True)
        if len(approx) == 4:
            biggest = approx

    # warp perspective
    matrix = cv.getPerspectiveTransform(np.float32(biggest), np.float32(win))
    imwarp = cv.warpPerspective(img, matrix, (w, h))

    cv.drawContours(img, biggest, -1, (0, 255, 0), 10)

    print(biggest)
    return imwarp
