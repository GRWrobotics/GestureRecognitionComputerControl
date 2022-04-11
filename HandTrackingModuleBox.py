#HandTrackingModuleBox
"""
Hand Tracking Module
By: Murtaza Hassan
Youtube: http://www.youtube.com/c/MurtazasWorkshopRoboticsandAI
Website: https://www.computervision.zone
"""

import cv2
import mediapipe as mp
import time
import math

class handDetector():
    def __init__(self, mode=False, maxHands=2, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.complexity = 1
        self.detectionCon = detectionCon
        self.trackCon = trackCon
        
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands (self.mode, self.maxHands, self.complexity, self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils
        self.tipIds = [4, 8, 12, 16, 20]

    def findHands(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        # print(results.multi_hand_landmarks)

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms,self.mpHands.HAND_CONNECTIONS)
        return img

    def findPosition(self, img, handNo=0, draw=True):
        xList = []
        yList = []
        bbox = []
        self.lmList = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myHand.landmark):
                # print(id, lm)
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                xList.append(cx)
                yList.append(cy)
                # print(id, cx, cy)
                self.lmList.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 5, (255, 0, 255), cv2.FILLED)
            xmin, xmax = min(xList), max(xList)
            ymin, ymax = min(yList), max(yList)
            bbox = xmin, ymin, xmax, ymax

            if draw:
                cv2.rectangle(img, (bbox[0] - 20, bbox[1] - 20),
            (bbox[2] + 20, bbox[3] + 20), (0, 255, 0), 2)
            
        return self.lmList, bbox

    def fingersUp(self):
        fingers = []
        # Thumb
        thumbTipToCenter = math.hypot(self.lmList[self.tipIds[0]][1] - self.lmList[9][1], self.lmList[self.tipIds[0]][2] - self.lmList[9][2])
        thumbKnuckleToCenter = math.hypot(self.lmList[self.tipIds[0]-1][1] - self.lmList[9][1], self.lmList[self.tipIds[0]][2] - self.lmList[9][2])
        if thumbTipToCenter > thumbKnuckleToCenter:
            fingers.append(1)
        else:
            fingers.append(0)
        # 4 Fingers
        for id in range(1, 5):
            if self.lmList[self.tipIds[id]][2] < self.lmList[self.tipIds[id] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)
        #print(thumbTipToCenter)
        #print(thumbKnuckleToCenter)
        #print(fingers)
        return fingers
    def matchGesture(self, fingers):
        gestureName='Unknown'
        match fingers:
            case [0,0,0,0,0]:
                gestureName = 'Fist'
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
                gestureName = 'No Pinky'
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


    def findDistance(self, p1, p2, img, draw=True):

        x1, y1 = self.lmList[p1][1], self.lmList[p1][2]
        x2, y2 = self.lmList[p2][1], self.lmList[p2][2]
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
        
        if draw:
            cv2.circle(img, (x1, y1), 10, (255, 0, 255), cv2.FILLED)
            cv2.circle(img, (x2, y2), 10, (255, 0, 255), cv2.FILLED)
            cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)
            cv2.circle(img, (cx, cy), 10, (255, 0, 255), cv2.FILLED)
        
        length = math.hypot(x2 - x1, y2 - y1)
        return length, img, [x1, y1, x2, y2, cx, cy]

def main():
    pTime = 0
    cap = cv2.VideoCapture(0)
    detector = handDetector()
    while True:
        success, img = cap.read()
        img = detector.findHands(img)
        lmList = detector.findPosition(img)
        
    
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        
        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3,
        (255, 0, 255), 3)
        
        cv2.imshow("Image", img)

        if cv2.waitKey(1)== ord('q'):
            break

if __name__ == "__main__":
    main()