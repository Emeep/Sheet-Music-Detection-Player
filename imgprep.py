import cv2 as cv
import numpy as np
import configparser as cp

def remove_lines(img):
    horizontal, vertical = img, img
    
    rows, cols, c = img.shape

    horizontalSize = cols/30
    verticalSize = rows/30
    
    h_struct = cv.getStructuringElement(cv.MORPH_RECT, (horizontalSize, 1))
    
    horizontal = cv.erode(horizontal, horizontal, h_struct)
    horizontal = cv.dilate(horizontal, horizontal, h_struct)
    
    cv.imshow(img)


def prep(img):
    import datetime as dt
    config = cp.ConfigParser()

    roi = cv.selectROI('select roi', img)
    cropped_image = img[int(roi[1]):int(roi[1]+roi[3]), int(roi[0]):int(roi[0]+roi[2])]
    
    imgray = cv.cvtColor(cropped_image, cv.COLOR_BGR2GRAY)
    imthresh = cv.adaptiveThreshold(imgray, 255,cv.ADAPTIVE_THRESH_GAUSSIAN_C,\
                    cv.THRESH_BINARY,15,2)
    return imthresh


# def scan(img):
#     config = cp.ConfigParser()
#     config.read('config.ini')

#     imgray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
#     imblur = cv.GaussianBlur(imgray, (1, 1), 0)
    
#     # edge detection
#     imthresh = cv.Canny(imblur, 0, 50)

#     # find biggest contours
#     contours, heirarchy = cv.findContours(imthresh, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
#     contours = sorted(contours, key=cv.contourArea, reverse=True)

#     win = np.array([[[0, 0]], [[w, 0]], [[w, h]], [[0, h]]])
#     biggest = win
#     contour = contours[0]
#     area = cv.contourArea(contour)
#     for i in contours:
#         print(cv.contourArea(i))

#     if area > 200:
#         approx = cv.approxPolyDP(contour, 0.02 * cv.arcLength(contour, True), True)
#         if len(approx) == 4:
#             biggest = approx

#     # warp perspective
#     matrix = cv.getPerspectiveTransform(np.float32(biggest), np.float32(win))
#     imwarp = cv.warpPerspective(img, matrix, (w, h))

#     cv.drawContours(img, biggest, -1, (0, 255, 0), 10)

#     print(biggest)
#     return imwarp


if __name__ == '__main__':
    path = "input/2024-05-11 054809.jpg"
    img = cv.imread(path)
    remove_lines(img)