# Finger Counter

import cv2
import mediapipe as mp
import HandTrackingModuleBox as htm
import numpy as np
import os
import time

cap = cv2.VideoCapture(0)
wCam, hCam = cap.get(3), cap.get(4) #Get camera width and height
detector = htm.handDetector()


class FingerCounter():
    def __init__(self, lmList) :
        self.lmList = lmList
        self.fingersOpen = [0,0,0,0,0]
        self.gestureName=""
        if len(lmList)!=0:
            #check if finger tip is below second knuckle landmark, then a finger is "closed" otherwise: open
            #This can be used to identify where fingers are in general in relation to other fingers and other hand landmarks.
            #IE: This can be used to identify and customize hand gestures
            for x in range(len(lmList)): 
                if lmList[x][0]%4 ==0:
                    if detector.findDistance(lmList[x],lmList[0])<detector.findDistance(lmList[x-2],lmList[0]) and x!=4:
                        self.fingersOpen[int(x/4-1)]=1 #using 1 and 0 for true and false bc its easier. TODO: Edit this function to compare distance between wrist and landmarks, so orientation doesn't matter
                    else:
                        self.fingersOpen[int(x/4-1)]=0

                if lmList[4][1]<lmList[3][1]:
                    #print('thumb in')
                    self.fingersOpen[0]=0
                else:
                    self.fingersOpen[0]=1
           
    #print(fingersOpen)
    
    def countFingers(self):
        fingerCount = 0
        for finger in self.fingersOpen:
            if finger:
                fingerCount+=1
            #cv2.putText(img,str(fingerCount),(10,100),cv2.FONT_HERSHEY_SIMPLEX,1,[255,0,0],3)
        return fingerCount
    def baseGesture(self):
        for x in range(len(self.lmList)): 
            if self.lmList[x][0]%4 ==0:
                if self.lmList[x][2]<self.lmList[x-2][2] and x!=4:
                    self.fingersOpen[int(x/4-1)]=1 #using 1 and 0 for true and false bc its easier. TODO: Edit this function to compare distance between wrist and landmarks, so orientation doesn't matter
                else:
                    self.fingersOpen[int(x/4-1)]=0

            if self.lmList[4][1]<self.lmList[3][1]:
                #print('thumb in')
                self.fingersOpen[0]=0
            else:
                self.fingersOpen[0]=1
        match self.fingersOpen:
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
                    
            

        cv2.imshow('FingerCounter', img) #show frame with modifications
        
    def dist(self, lm1, lm2):
        lm1
        lm2
    #end function defenitions
    
def main():
    pTime = 0
    cTime = 0
    cap = cv2.VideoCapture(1)
    detector = htm.handDetector(detectionCon=0.75)
    
    while True:
        success, img = cap.read()
        img = detector.findHands(img)
        lmList = detector.findPosition(img)
        gestureDetector = FingerCounter(lmList)
        gestureDetector.baseGesture()
 
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
 
        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3,
                    (255, 0, 255), 3)
 
        cv2.imshow("Image", img)
        cv2.waitKey(1)
        if cv2.waitKey(1) == ord('q'):
            break
    cap.release() # release camera
    cv2.destroyAllWindows() # Destroy all camera showing windows
 
 
if __name__ == "__main__":
    main()