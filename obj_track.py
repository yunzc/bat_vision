
import cv2
import numpy as np
import time

vid = cv2.VideoCapture(0)
prev_area = None
prev_coord = None
counter = 0
while(1):
    # Take each frame
    _, frame = vid.read()
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
    opening = cv2.morphologyEx(res, cv2.MORPH_OPEN, kernel)
    # print(hsv[250:350,250:350])
    # cv2.rectangle(hsv, (250,250),(350,350),(255,0,0),2)
    img_bw = cv2.cvtColor(opening, cv2.COLOR_BGR2GRAY)
    #start looking for rectangle
    ret,thresh = cv2.threshold(img_bw,0,50,0)
    _,contours,_ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
#    # Find the index of the largest contour
    
    try: 
        areas = [cv2.contourArea(c) for c in contours]
        max_index = np.argmax(areas)
        cnt = contours[max_index]
        x,y,w,h = cv2.boundingRect(cnt)
        cv2.rectangle(frame, (x,y), (x + w,y + h), (0,255,0),2)
        if counter == 10:
            if prev_area != None:
                print("==============================")
                if areas[max_index] > prev_area + 1000:
                    print("move back")
                elif areas[max_index] < prev_area - 1000:
                    print("move forward")
            if prev_coord != None: 
                if x > prev_coord[0] + 20: 
                    print("move right")
                elif x < prev_coord[0] - 20:
                    print("move left")
                if y > prev_coord[1] + 20:
                    print("move down")
                elif y < prev_coord[1] - 20:
                    print("move up")
                print("===============================")
            prev_area = areas[max_index]
            prev_coord = (x,y)
            counter = 0
        else:
            counter += 1
            
    except ValueError:
        pass
    
    cv2.imshow('frame',frame)
    cv2.imshow('hsv',hsv)
    cv2.imshow('mask',mask)
    cv2.imshow('opening', opening)
    cv2.imshow('thresh', thresh)
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
    	break

cv2.destroyAllWindows()