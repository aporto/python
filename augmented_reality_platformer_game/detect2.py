# Standard imports
import cv2
import numpy as np;
import time

def detectBlocks():
    img = cv2.imread("C:\\Users\\aporto\\Desktop\\whiteboard.jpg")
    #, cv2.IMREAD_GRAYSCALE)
    time1 = time.time();
    imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret,thresh = cv2.threshold(imgray, 200,255,0)
    #image, contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        x,y,w,h = cv2.boundingRect(contour)
        if w < 620 and w > 30:
            if h < 400 and h > 5:
                cv2.rectangle(im,(x,y),(x+w,y+h),(0,255,0),2)
    #cv2.drawContours(im, contours, -1, (0,255,0), 3)
    print (time.time() - time1) * 1000

    #cv2.imshow("thresould", thresh)
    cv2.imshow("img", im)
    cv2.waitKey(0)

detectBlocks()