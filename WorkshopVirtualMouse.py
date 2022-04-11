#WorkshopVirtualMouse
import cv2
import HandTrackingModuleBox as htm
import time
import numpy as np
import pyautogui as mouse
import mouse as fastMouse

cTime = 0
pTime = 0
camera = 0  
mouseSens = 1.5
cap = cv2.VideoCapture(camera)
wCam, hCam = cap.get(3), cap.get(4)
detector = htm.handDetector(detectionCon=0.75)

frameR=150
wScreen, hScreen = mouse.size()
print(wScreen,hScreen)
mouse.FAILSAFE = False

time1 = time.time()
#mouse.moveTo(100,100,duration=.25)
print(time.time()-time1)

lastPos = [0, 0]

while True:
    success, img = cap.read()
    if camera == 1:
        img = cv2.flip(img,1)
    else:
        img = cv2.flip(img,1)
        img = cv2.flip(img,0)
    img = detector.findHands(img)
    lmList, bbox = detector.findPosition(img)
    
    # get the tip of middle and index
    if len(lmList)!=0:
        mx,my = lmList[5][1:]
        x1,y1 = lmList[4][1:] #for using distance to click 
        x2,y2 = lmList[5][1:]

        #x1,y1 = lmList[8][1:] #for using distance to click 
        #x2,y2 = lmList[7][1:]

    # check which fingers are up
        fingers = detector.fingersUp()
        #print(fingers)
    # Moving mode w/ index only
        cv2.rectangle(img, (frameR,frameR), (int(wCam-frameR),int(hCam-frameR)), (255,0,0), 2,)
    
        if fingers[1]==1 and fingers[2]==1 :        
    # smooth values
    # Move mouse
            #print(lmList)
            #print(lastPos)
            lastX=lastPos[0]
            lastY=lastPos[1]
        # Convert Coordinates
            mouseX = np.interp(mx,(frameR,wCam-frameR),(0,wScreen)) 
            mouseY = np.interp(my,(frameR,hCam-frameR),(0,hScreen)) 
            lastMouseX = np.interp(lastX,(frameR,wCam-frameR),(0,wScreen)) 
            lastMouseY = np.interp(lastY,(frameR,hCam-frameR),(0,hScreen)) 
            #print(mx, my)
            #print(lastX,lastY)
            #print(.2*wScreen)
            #print(.2*hScreen)
            print("x diff", abs(mx-lastX))
            print("y diff", abs(my-lastY))
            #print(mouse.onScreen(mouseX, mouseY))
           #Gives a small dead zone to hand movements to prevent jitter
            if abs(mx-lastX)>0.002*wScreen or abs(my-lastY)>0.002*hScreen:
                time1 = time.time()

                #relative position movement based on hand motion.
                fastMouse.move((mouseX-lastMouseX)*mouseSens, (mouseY-lastMouseY)*mouseSens, absolute=False)
                #mouse.moveRel((mouseX-lastMouseX)*mouseSens, (mouseY-lastMouseY)*mouseSens)

                #absolute position movement based on hand position in frame
                #mouse.moveTo(mouseX, mouseY)
                print(time.time()-time1)
            length, img, _ = detector.findDistance(5,4,img)

            if length<60:
                cv2.circle(img,(lmList[4][1],lmList[4][2]),10,[0,255,0],-1)
                fastMouse.click()
            # Clicking mode w/ thumb
            # click if thumb is in
            # if fingers[0]==1:
            #     cv2.circle(img,(lmList[4][1],lmList[4][2]),10,[0,255,0],-1)
            #     mouse.click()
            lastPos=[mx, my]
        else:
            lastPos=[mx, my]
    

    # frame rate
    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)),(20,50),cv2.FONT_HERSHEY_SIMPLEX,2,[255,0,0],3)
    # Display


    #Opt 2: use distances between thumb and lm or index and middle

    cv2.imshow('Virtual Mouse', img)
    if cv2.waitKey(1) == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()

