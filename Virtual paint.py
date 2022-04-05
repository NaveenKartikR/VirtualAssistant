import cv2
import numpy

frame_width = 640
frame_height = 480
frame_brightness = 100

cap = cv2.VideoCapture(0)
cap.set(3,frame_width)
cap.set(4, frame_height)
cap.set(10, frame_brightness)

while True:
    success, img = cap.read()
    cv2.imshow("Paint", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break