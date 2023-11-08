import cv2,numpy as np

cap = cv2.VideoCapture(0)
frameWidth = 640
frameHeight = 480
cap.set(3,frameWidth)
cap.set(4,frameHeight)
cap.set(10,130) #brightness

#   HSV VALUES OF COLORS
Colors = [[5,107,0,19,255,255], #orange     
          [133,56,0,159,156,255], #purple
          [57,76,0,100,255,255] #green
          ]

#BGR VALUES OF COLORS
ColorValues = [[51,153,255],[255,0,255],[0,255,0]]

#Points that we will loop  [x,y,colorID]
Points = []


def getContours(img):
    contours,hierarchy = cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    x,y,w,h = 0,0,0,0
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if(area>500):
            cv2.drawContours(imgResult,cnt,-1,(255,0,0) ,3)
            peri = cv2.arcLength(cnt,True)
            approx = cv2.approxPolyDP(cnt,0.02*peri,True)            
            x,y,w,h = cv2.boundingRect(approx)
    return x+w//2,y

def findColor(img,Colors):
    imgHSV = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    newPoints = []
    count = 0
    for color in Colors:
        lower = np.array([Colors[0][:3]])
        upper = np.array([Colors[0][3:]])
        mask = cv2.inRange(imgHSV,lower,upper)
        x,y = getContours(mask)
        if x!=0 and y!=0 :
            newPoints.append([x,y,count])
        cv2.circle(imgResult,(x,y),10,ColorValues[count],cv2.FILLED)
        count = count+1
        cv2.imshow(str(color[0]),mask)
    return newPoints


def drawOnCanvas(Points,ColorValues):
    for point in Points:
        cv2.circle(imgResult , (point[0],point[1]),10,ColorValues[point[2]],cv2.FILLED) 
    
    
    
while True:
    success,img = cap.read()
    imgResult = img.copy()
    newPoints = findColor(img,Colors)
    if newPoints!=0 :
        for new in newPoints:
            Points.append(new)
    if len(Points) > 0 :
        drawOnCanvas(Points,ColorValues)
    cv2.imshow("Video",imgResult)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break



# go through:
#     1. Finding the colour 
#     2. Finding the location of the object
#     3. Contouring the pen
#     4. Locating the center
#     5. Drawing the starting point of the same color
#     6. To Draw, we are creating a list of points and just looping it around
