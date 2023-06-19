import cv2
import numpy as np
cap = cv2.VideoCapture(0)
while True:
    #kamera açma
 ret, pic = cap.read()
    #hsv renk uzayına çevirme
 hsv = cv2.cvtColor(pic, cv2.COLOR_BGR2HSV)
     #mavi alt ve ust sınır belirleme
 lower_blue = np.array([75, 120, 120])
 upper_blue = np.array([130, 255, 255])
    #mavi renge gore maskeleme
 mask = cv2.inRange(hsv, lower_blue, upper_blue)
    #blurlama için gray'e cevirme
 gray = cv2.cvtColor(pic,cv2.COLOR_BGR2GRAY)
     #blurlama
 blur = cv2.bilateralFilter(gray, 10, 80,95)
    #canny detection
 canny = cv2.Canny(blur,80,150)
    #çember bulma
 circles = cv2.HoughCircles(canny,cv2.HOUGH_GRADIENT, 1, 20,param1=10,param2=30,minRadius = 10,maxRadius=220)
    #sınırları konturleme
 contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
 for cnt in contours:
    area = cv2.contourArea(cnt)
    #alan sınırlaması
    if area > 60:
     (x, y), radius = cv2.minEnclosingCircle(cnt)
     if circles is not None:
           circles = np.uint16(np.around(circles))
           for i in circles[0,:]: 
            cv2.circle(pic, (int(x), int(y)), int(radius), (0, 0, 255), 4)
    #sonuclarıgoruntuleme
 cv2.imshow("mask",mask)
 cv2.imshow("blur",blur)
 cv2.imshow("gray",gray)
 cv2.imshow("Bilgisayar Kamerasi", pic)
  #t ye basınca cıkar
 if cv2.waitKey(50) & 0xFF == ord('t'):
    break