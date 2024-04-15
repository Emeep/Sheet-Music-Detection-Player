import cv2 as cv

def prep(img):
    w, h = 600, 800
    if img.shape[0] < img.shape[1]:
        w, h = 800, 600
    img = cv.resize(img, (w, h))

    roi = cv.selectROI('select roi', img)
    cropped_image = img[int(roi[1]):int(roi[1]+roi[3]), int(roi[0]):int(roi[0]+roi[2])]
    cv.destroyWindow('select roi')
    
    imgray = cv.cvtColor(cropped_image, cv.COLOR_BGR2GRAY)
    imthresh = cv.adaptiveThreshold(imgray, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                    cv.THRESH_BINARY, 255, 5)

    return imthresh