#gestureInput
#WorkshopVirtualMouse
import cv2
import HandTrackingModuleBox as htm
import FingerCounterModule as fcm
import time
import numpy as np
import pyautogui as mouse
import mouse as fastMouse

cTime = 0
pTime = 0
#Delay for gesture input
delay = 0.5
stopwatch = 0 #starts and resets based on gesture input.
lastGesture = '' # Check if the gesture has actually changed.

camera = 0  
mouseSens = 1.5
cap = cv2.VideoCapture(camera)
wCam, hCam = cap.get(3), cap.get(4)
detector = htm.handDetector(detectionCon=0.75)
fingersOpen = [0,0,0,0,0]

frameR=150
wScreen, hScreen = mouse.size()
#print(wScreen,hScreen)
mouse.FAILSAFE = False

time1 = time.time()
#mouse.moveTo(100,100,duration=.25)
#print(time.time()-time1)

lastPos = [0, 0]
usefulKeybinds = ['playpause, prevtrack','nexttrack','volumeup','volumedown','volumemute']

def gesture(fingers):
    gestureName=''
    match fingers:
        case [0,0,0,0,0]:
            gestureName = 'fist'
        case [1,0,0,0,0]:
            gestureName = 'Thumb'    
        case [0,1,0,0,0]:
            gestureName = 'First'
        case [0,0,1,0,0]:
            gestureName = 'Not nice'
        case [0,0,0,1,0]:
            gestureName = 'Ring'
        case [0,0,0,0,1]:
            gestureName = 'Pinky'
        case [1,1,0,0,0]:
            gestureName = 'L'
        case [1,0,1,0,0]:
            gestureName = 'Weird'
        case [1,0,0,1,0]:
            gestureName = 'Impresive'
        case [1,0,0,0,1]:
            gestureName = 'Hang Loose'
        case [1,1,0,0,1]:
            gestureName = 'I love you'
        case [1,1,1,0,1]:
            gestureName = 'No Ring'
        case [1,1,1,1,0]:
            gestureName = 'No pink'
        case [1,1,0,1,1]:
            gestureName = 'No Middle'
        case [1,0,1,1,1]:
            gestureName = 'No First'
        case [0,1,1,1,1]:
            gestureName = 'Four (No thumb)'
        case [0,1,1,1,0]:
            gestureName = 'Three (Hold Pinky)'
        case [0,1,1,0,0]:
            gestureName = 'Peace (Two/ Hold ring pinky)'
        case [1,1,1,1,0]:
            gestureName = 'fist'
        case [1,1,1,1,1]:
            gestureName = 'Five (Hand)'
        case [0,1,0,0,1]:
            gestureName = 'Rock on'
        case [1,1,1,0,0]:
            gestureName = 'Other Three'
        case [0,0,1,1,1]:
            gestureName = 'Okay / Hold First'
        case [1,0,1,1,1]:
            gestureName = 'Okay / No First'
    #cv2.putText(img,gestureName,(10,50),cv2.FONT_HERSHEY_SIMPLEX,1,[255,0,0],3)
    return gestureName

def keybindG(gesture):
    match gesture:
        case  'fist':
            print("No Command Set")
        case 'Thumb':
            print("No Command Set")
        case 'First':
            print("No Command Set")
        case 'Not nice':
            print("No Command Set")
        case 'Ring':
            print("No Command Set")
        case 'Pinky':
            print("No Command Set")
        case 'L':
            print("No Command Set")
        case 'Weird':
            print("No Command Set")
        case 'Impresive':
            print("No Command Set")
        case 'Hang Loose':
            print("No Command Set")
        case 'I love you':
            print("No Command Set")
        case 'No Ring':
            print("No Command Set")
        case 'No pink':
            print("No Command Set")
        case 'No Middle':
            print("No Command Set")
        case 'No First':
            print("No Command Set")
        case 'Four (No thumb)':
            print("No Command Set")
        case 'Three (Hold Pinky)':
            print("No Command Set")
        case 'Peace (Two/ Hold ring pinky)':
            print("No Command Set")
        case 'fist':
            print("No Command Set")
        case 'Five (Hand)':
            print("No Command Set")
        case 'Rock on':
            print("No Command Set")
        case 'Other Three':
            print("No Command Set")
        case 'Okay / Hold First':
            print("No Command Set")
        case 'Okay / No First':
            print("No Command Set")

def keybindF(fingers):
    match fingers:
        case [0,0,0,0,0]:
            print('No Command Set')
        case [1,0,0,0,0]:
            print('No Command Set')
        case [0,1,0,0,0]:
            print('No Command Set')
        case [0,0,1,0,0]:
            print('No Command Set')
        case [0,0,0,1,0]:
            print('No Command Set')
        case [0,0,0,0,1]:
            print('No Command Set')
        case [1,1,0,0,0]:
            print('No Command Set')
        case [1,0,1,0,0]:
            print('No Command Set')
        case [1,0,0,1,0]:
            print('No Command Set')
        case [1,0,0,0,1]:
            print('No Command Set')
        case [1,1,0,0,1]:
            print('No Command Set')
        case [1,1,1,0,1]:
            print('No Command Set')
        case [1,1,1,1,0]:
            print('No Command Set')
        case [1,1,0,1,1]:
            print('No Command Set')
        case [1,0,1,1,1]:
            print('No Command Set')
        case [0,1,1,1,1]:
            print('No Command Set')
        case [0,1,1,1,0]:
            print('No Command Set')
        case [0,1,1,0,0]:
            print('No Command Set')
        case [1,1,1,1,0]:
            print('No Command Set')
        case [1,1,1,1,1]:
            print('No Command Set')
        case [0,1,0,0,1]:
            print('No Command Set')
        case [1,1,1,0,0]:
            print('No Command Set')
        case [0,0,1,1,1]:
            print('No Command Set')
        case [1,0,1,1,1]:
            print('No Command Set')

def baseGesture(lmList):
    gestureName=''
    for x in range(len(lmList)): 
        if lmList[x][0]%4 ==0:
            if lmList[x][2]<lmList[x-2][2] and x!=4:
                fingersOpen[int(x/4-1)]=1 #using 1 and 0 for true and false bc its easier. TODO: Edit this function to compare distance between wrist and landmarks, so orientation doesn't matter
            else:
                fingersOpen[int(x/4-1)]=0

        if lmList[4][1]<lmList[3][1]:
            #print('thumb in')
            fingersOpen[0]=0
        else:
            fingersOpen[0]=1
    match fingersOpen:
        case [0,0,0,0,0]:
            gestureName = 'fist'
        case [1,0,0,0,0]:
            gestureName = 'Thumb'    
        case [0,1,0,0,0]:
            gestureName = 'First'
        case [0,0,1,0,0]:
            gestureName = 'Not nice'
        case [0,0,0,1,0]:
            gestureName = 'Ring'
        case [0,0,0,0,1]:
            gestureName = 'Pinky'
        case [1,1,0,0,0]:
            gestureName = 'L'
        case [1,0,1,0,0]:
            gestureName = 'Weird'
        case [1,0,0,1,0]:
            gestureName = 'Impresive'
        case [1,0,0,0,1]:
            gestureName = 'Hang Loose'
        case [1,1,0,0,1]:
            gestureName = 'I love you'
        case [1,1,1,0,1]:
            gestureName = 'No Ring'
        case [1,1,1,1,0]:
            gestureName = 'No pink'
        case [1,1,0,1,1]:
            gestureName = 'No Middle'
        case [1,0,1,1,1]:
            gestureName = 'No First'
        case [0,1,1,1,1]:
            gestureName = 'Four (No thumb)'
        case [0,1,1,1,0]:
            gestureName = 'Three (Hold Pinky)'
        case [0,1,1,0,0]:
            gestureName = 'Peace (Two/ Hold ring pinky)'
        case [1,1,1,1,0]:
            gestureName = 'fist'
        case [1,1,1,1,1]:
            gestureName = 'Five (Hand)'
        case [0,1,0,0,1]:
            gestureName = 'Rock on'
        case [1,1,1,0,0]:
            gestureName = 'Other Three'
        case [0,0,1,1,1]:
            gestureName = 'Okay / Hold First'
        case [1,0,1,1,1]:
            gestureName = 'Okay / No First'
    #cv2.putText(img,gestureName,(10,50),cv2.FONT_HERSHEY_SIMPLEX,1,[255,0,0],3)
    return gestureName

while True:
    success, img = cap.read()
    if camera == 0:
        img = cv2.flip(img,1)
    else:
        img = cv2.flip(img,1)
        img = cv2.flip(img,0)
    img = detector.findHands(img)
    lmList, bbox = detector.findPosition(img)
    

    if len(lmList)!=0:
        mx,my = lmList[5][1:]
        x1,y1 = lmList[4][1:] #for using distance to click 
        x2,y2 = lmList[5][1:]

        #x1,y1 = lmList[8][1:] #for using distance to click 
        #x2,y2 = lmList[7][1:]

    # check which fingers are up
        fingers = detector.fingersUp()
        cGesture = gesture(fingers)
        #print(gesture(fingers))
        if(cGesture != lastGesture and stopwatch>delay):
            stopwatch=0 #reset stopwatch
            #do something
            print ('Gesture changed',lastGesture,'to', cGesture)
            keybindF(fingers)
            
        lastGesture=cGesture

        #print(baseGesture(fingers))
        #could make this a function: Commands would go here, possibly with a timer to prevent too many Commands firing at once.
        #Can match to gesture name from gesture(fingers), or directly from fingers.
        
        #length, img, _ = detector.findDistance(5,4,img)
    

    # frame rate
    cTime = time.time()
    fps = 1/(cTime-pTime)
    #Stopwatch increments by the amount of time passed
    stopwatch+=cTime-pTime
    pTime = cTime
    cv2.putText(img, str(int(fps)),(20,50),cv2.FONT_HERSHEY_SIMPLEX,2,[255,0,0],3)
    # Display
    

    #Opt 2: use distances between thumb and lm or index and middle

    cv2.imshow('Virtual Mouse', img)
    if cv2.waitKey(1) == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()

#Shtop