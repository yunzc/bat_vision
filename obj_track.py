
import cv2
import numpy as np

cap = cv2.VideoCapture(0)

while(1):

    # Take each frame
    _, frame = cap.read()

    # Convert BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # define range of blue color in HSV
    lower_yellow = np.array([30,100,100])
    upper_yellow = np.array([45,255,255])

    # Threshold the HSV image to get only blue colors
    mask = cv2.inRange(hsv, lower_yellow, upper_yellow)

    # Bitwise-AND mask and original image
    res = cv2.bitwise_and(frame,frame, mask= mask)
    #erode and dilate kernel
    kernel = np.ones((15,15),np.uint8)
    opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    # print(hsv[250:350,250:350])
    # cv2.rectangle(hsv, (250,250),(350,350),(255,0,0),2)
    img_bw = opening 
    #start looking for rectangle
    ret,thresh = cv2.threshold(img_bw,127,255,0)
    _,contours,_ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # Find the index of the largest contour
    areas = [cv2.contourArea(c) for c in contours]
    max_index = np.argmax(areas)
    cnt = contours[max_index]

    print(areas)

    x,y,w,h = cv2.bouondingRect(cnt)
    cv2.rectangle(frame, (x,y), (x + w,y + h), (0,255,0),2)
    cv2.imshow('frame',frame)
    cv2.imshow('mask',mask)
    cv2.imshow('res',res)
    cv2.imshow('opening', opening)
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
    	break

cv2.destroyAllWindows()