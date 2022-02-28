from email.mime import image
from itertools import count
import cv2
from cv2 import putText
import numpy as np
import math


cap = cv2.VideoCapture(0)
while(cap.isOpened()):
    ret, img = cap.read()
    cv2.rectangle(img, (100,100), (300,300), (0,255,0), 0)
    crop_img = img[100:300, 100:300]


    #convert to gray scale

    gray = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)

    #applying gaissian blur
    value = (35, 35)
    blurred = cv2.GaussianBlur(gray, value, 0)
    thresh1  = cv2.threshold(blurred, 0, 255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
    cv2.imshow('Thresholded', thresh1)

    (version, _, _) = cv2.__version__.split('.')

    if version == '3':
        image, contours, hierarchy = cv2.findContours(thresh1.copy(),cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)


    elif version == '4':
        contours, hierarchy = cv2.findContours(thresh1.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    cnt = max(contours, key = lambda x: cv2.contourArea(x))

    x,y,w,h = cv2.boundingRect(cnt)
    cv2.rectangle(crop_img, (x,y),(x+w, y+h),(0,0,255),0)

    #finding convex hull

    hull = cv2.convexHull(cnt)

    #drawing contours

    drawing = np.zeros(crop_img.shape,np.uint8)
    cv2.drawContours(drawing, [cnt],0, (0,255,0),0)
    cv2.drawContours(drawing,[hull],0,(0,0,255),0)
    area_hull = cv2.contourArea(hull)
    area_cnt = cv2.contourArea(cnt)

    area_ratio = ((area_hull - area_cnt) / area_cnt)*100

    #findinf convex hull

    hull = cv2.convexHull(cnt, returnPoints=False)
    #finding cinvex defects

    defects = cv2.convexityDefects(cnt, hull)
    count_defects = 0
    cv2.drawContours(thresh1, contours, -1, (0,255,0), 3)

    # applying Cosine Rule to find angle for all defects (between fingers)

    for i in range(defects.shape[0]):
        s,e,f,d = defects[i,0]

        start = tuple(cnt[s][0])
        end = tuple(cnt[e][0])
        far = tuple(cnt[f][0])

        #find the lenfth of all sides of triangle
        a = math.sqrt((end[0] - start[0])**2 + (end[1] - start[1])**2)
        b = math.sqrt((far[0] - start[0])**2 + (far[1] - start[1])**2)
        c = math.sqrt((end[0] - far[0])**2 + (end[1] - far[1])**2)

        #apply cosine rule here

        angle = math.acos((b**2+c**2-a**2)/(2*b*c)) * 57

        if angle <= 90:
            count_defects += 1
            cv2.circle(crop_img,far, 1, [0,0,255], -1)
        cv2.line(crop_img,start, end, [0,255,0], 2)

    if count_defects == 0:
        if(area_ratio<2000):
            cv2.putText(img,"put hand in box", (5,50), cv2.FONT_HERSHEY_SIMPLEX, 1, 2)
        if(area_ratio < 12):
    	    cv2.putText(img, "0", (5, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, 2)
        if(area_ratio > 17.5):
                cv2.putText(img, "Best of luck", (5, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, 2)   
        else:
            cv2.putText(img, "1", (5, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, 2)
    elif count_defects == 1:
        cv2.putText(img, "2", (5, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, 2)
    elif count_defects == 2:
        cv2.putText(img, "3", (5, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, 2)
    elif count_defects == 3:
        cv2.putText(img, "4", (5, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, 2)
    elif count_defects == 4:
        cv2.putText(img, "5", (5, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, 2)

    cv2.imshow('Gesture', img)
    all_img = np.hstack((drawing, crop_img))
    cv2.imshow('Contours', all_img)

    k = cv2.waitKey(10)
    if k == 27:
        break
    