import cv2
import numpy as np

kernel = np.ones((5, 5), np.uint8)

img = cv2.imread("Barney Stinson.jpg")

imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
imgBlur = cv2.GaussianBlur(imgGray, (7, 7), 0)
imgCanny = cv2.Canny(img, 100, 100)
imgDialation = cv2.dilate(imgCanny, kernel, iterations = 1)
imgEroded = cv2.erode(imgDialation, kernel, iterations = 1)

#cv2.imshow("Original Barney", img)
#cv2.imshow("Gray image", imgGray)
#cv2.imshow("Blur image", imgBlur)
#cv2.imshow("Canny image", imgCanny)
#cv2.imshow("Dialation image", imgDialation)
#cv2.imshow("Eroded image", imgEroded)
#cv2.waitKey(0)

# DISPLAYING IMAGE #

'''img_bs = cv2.imread("Barney Stinson.jpg")
img_hj = cv2.imread("Hugh Jackman.jpg")

cv2.imshow("Barney Stinson", img_bs)
cv2.imshow("Hugh Jackman", img_hj)

cv2.waitKey(0)

# DISPLAYING VIDEO #

cap = cv2.VideoCapture(0)
cap.set(3,640)
cap.set(4, 480)
cap.set(10, 100)

while True:
    success, img = cap.read()
    cv2.imshow("Webcam", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break'''

####################### STACKING USING THE FUNCTION #####################

frameWidth = 640
frameHeight = 480
cap = cv2.VideoCapture(0)
cap.set(3, frameWidth)
cap.set(4, frameHeight)

def stackImages(imgArray,scale,lables=[]):
    sizeW= imgArray[0][0].shape[1]
    sizeH = imgArray[0][0].shape[0]
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range ( 0, rows):
            for y in range(0, cols):
                imgArray[x][y] = cv2.resize(imgArray[x][y], (sizeW, sizeH), None, scale, scale)
                if len(imgArray[x][y].shape) == 2: imgArray[x][y]= cv2.cvtColor( imgArray[x][y], cv2.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank]*rows
        hor_con = [imageBlank]*rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
            hor_con[x] = np.concatenate(imgArray[x])
        ver = np.vstack(hor)
        ver_con = np.concatenate(hor)
    else:
        for x in range(0, rows):
            imgArray[x] = cv2.resize(imgArray[x], (sizeW, sizeH), None, scale, scale)
            if len(imgArray[x].shape) == 2: imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
        hor= np.hstack(imgArray)
        hor_con= np.concatenate(imgArray)
        ver = hor
    if len(lables) != 0:
        eachImgWidth= int(ver.shape[1] / cols)
        eachImgHeight = int(ver.shape[0] / rows)
        print(eachImgHeight)
        for d in range(0, rows):
            for c in range (0,cols):
                cv2.rectangle(ver,(c*eachImgWidth,eachImgHeight*d),(c*eachImgWidth+len(lables[d][c])*13+27,30+eachImgHeight*d),(255,255,255),cv2.FILLED)
                cv2.putText(ver,lables[d][c],(eachImgWidth*c+10,eachImgHeight*d+20),cv2.FONT_HERSHEY_COMPLEX,0.7,(255,0,255),2)
    return ver

while True:
    success, img = cap.read()
    kernel = np.ones((5,5),np.uint8)
    print(kernel)
    #path = "Resources/lena.png"
    #img =  cv2.imread(path)
    imgGray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray,(7,7),0)
    imgCanny = cv2.Canny(imgBlur,100,200)
    imgDilation = cv2.dilate(imgCanny,kernel , iterations = 2)
    imgEroded = cv2.erode(imgDilation,kernel,iterations=2)

    #imgBlank = np.zeros((200,200),np.uint8)
    StackedImages = stackImages(([img,imgGray,imgBlur],
                                   [imgCanny,imgDilation,imgEroded]),0.6)
    cv2.imshow("Staked Images", StackedImages)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


################### Stacking images without Function ################
# import cv2
# import numpy as np
# img1 = cv2.imread('../Resources/lena.png',0)
# img2 = cv2.imread('../Resources/land.jpg')
# print(img1.shape)
# print(img2.shape)
# img1 = cv2.resize(img1, (0, 0), None, 0.5, 0.5)
# img2 = cv2.resize(img2, (0, 0), None, 0.5, 0.5)
# img1 = cv2.cvtColor(img1, cv2.COLOR_GRAY2BGR)
# hor= np.hstack((img1, img2))
# ver = np.vstack((img1, img2))
# cv2.imshow('Vertical', ver)
# cv2.imshow('Horizontal', hor)
# cv2.waitKey(0)