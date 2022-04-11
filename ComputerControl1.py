#ComputerControl1
#imports for gesture recognition
import cv2
import FingerCounterModule as fcm
import HandTrackingModuleBox as htm
import time
import PySimpleGUI as sg

#imports for mouse control
import numpy as np
import pyautogui as mouse
import mouse as fastMouse
import math

#Imports for screen and volume control
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import screen_brightness_control as sbc


# get current brightness  value
current_brightness = sbc.get_brightness()
print(current_brightness)

sg.theme('DarkAmber')   # Add a touch of color
# All the stuff inside your window.
gesturesList = ['Fist','L','Hang Loose','I love you','No Ring','No pink','No Middle','No First','Four (No thumb)','Three (Hold Pinky)','Peace (Two/ Hold ring pinky)','Five (Hand)','Rock on','Other Three','Okay / Hold First','First','Thumb','Ring','Pinky','Weird','Impresive','Not nice']
usefulKeybinds = ['playpause, prevtrack','nexttrack','volumeup','volumedown','volumemute']# Holds keybinds but can't put array in array for Combo.
functionsList = ['Mouse Toggle','Brightness / Volume Toggle','Keybinds Toggle','playpause', 'prevtrack','nexttrack','volumeup','volumedown','volumemute']
setFunctions = [
                [sg.Text(functionsList[0]), sg.Combo(gesturesList, default_value='Fist')],
                [sg.Text(functionsList[1]), sg.Combo(gesturesList, default_value='Okay / Hold First')],
                [sg.Text(functionsList[2]), sg.Combo(gesturesList, default_value='Three (Hold Pinky)')],
                [sg.Text('')],
                [sg.Text('Function Keybinds')],
                [sg.Text(functionsList[3]), sg.Combo(gesturesList, default_value='I love you')],
                [sg.Text(functionsList[4]), sg.Combo(gesturesList, default_value='No First')],
                [sg.Text(functionsList[5]), sg.Combo(gesturesList, default_value='No Middle')],
                [sg.Text(functionsList[6]), sg.Combo(gesturesList, default_value='No Ring')],
                [sg.Text(functionsList[7]), sg.Combo(gesturesList, default_value='No Pinky')],
                [sg.Text(functionsList[8]), sg.Combo(gesturesList, default_value='L')],
                [sg.Text('Custom Function (Coming Soon)'), sg.Combo(gesturesList),sg.Combo(functionsList)],
            
                ]
layout = [  
            
            [sg.Text('Welcome to the gesture controled computer system')],
            [sg.Text('Please adjust features you would like')],
            [sg.Text('')],
            [sg.Text('Select Camera'), sg.Combo(['Default Webcam', 'Camera 2 (Doc Cam)'])],
            [sg.Text('Mouse Sensitivity'), sg.Slider(range=(1,500), default_value=100, size=(20,15), orientation='horizontal', font=('Helvetica', 12))],
            [sg.Text('Click Delay, miliseconds'), sg.Slider(range=(0,2500), default_value=500, size=(20,15), orientation='horizontal', font=('Helvetica', 12))],
            [sg.Radio('Use PreNamed Gesture', "RADIO1", default=True), sg.Radio('Use custom gestures (Coming Soon)', "RADIO1")],
            [sg.Checkbox('Run Gesture Mouse', default=True), sg.Checkbox('Volume/Brightness Control Available')],
            [sg.Button('Save Bindings (Coming Soon)')],
            setFunctions,
            [sg.Button('Start'), sg.Button('Cancel')]
        ]

# Create the Window
window = sg.Window('Gesture Control', layout)
# Event Loop to process "events" and get the "values" of the inputs



def wip(mouseToggleOn, volBrightToggleOn, mouseSensInput, clickDelayInput, inputGestures, outputBindings, cameraName, keybindsToggleOn):
#Conrtrol System
    if True: #general setup and settings
        #print("General Setup")
        cTime = 0
        pTime = 0
        if cameraName=='Camera 2 (Doc Cam)':
            camera = 1
        else:
            camera = 0
        cap = cv2.VideoCapture(camera)
        wCam, hCam = cap.get(3), cap.get(4)
        detector = htm.handDetector(detectionCon=0.75)
        success, img = cap.read()
        if(not success):
            print("No image detected")
        else:
            img = detector.findHands(img)
            lmList, bbox = detector.findPosition(img)
    
    if True: #Mouse control setup Shrinker
        #print("mouse setup")
        mouseOn = False
        clickDelay=clickDelayInput/1000
        clickWatch=0
        switchDelay = 1
        switchWatch = 0

        mouseSens = mouseSensInput*0.01
       
        #This stuff is pulled from the inner loop to make finger counter function
        
        #counter = fcm.FingerCounter(lmList)
        ##

        frameR=100
        wScreen, hScreen = mouse.size()
        print(wScreen,hScreen)
        mouse.FAILSAFE = False

        lastPos = [0, 0]
    
    if True: #Volume and Brighness Setup
        #print("volbright setup")
        volBrightOn = False
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(
            IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))
        # volume.GetMute()
        # volume.GetMasterVolumeLevel()
        volRange = volume.GetVolumeRange()
        # volRange  = (-65.25 , 0)
    
        minVol = volRange[0]
        maxVol = volRange[1]
        vol = 0
        volBar = 400
        volPer = 0

        brightBar = 400
        brightPer = 0
        cBright = 0

        area = 0
        colorVol = (255, 0, 0)
        colorBright = (0, 255, 0)   

    if True: # Keybind control Setup
        #print('keybind Control Setup')
        keybindsOn = False

    while True: # Main Gesture detection Loop
        #print("Main Detector")
        if True: # Setup
            success, img = cap.read()
            if(not success):
                print("Image Detection Failure")
                break
            if not cameraName == 'Camera 2 (Doc Cam)':
                img = cv2.flip(img,1)
            else:
                img = cv2.flip(img,1)
                img = cv2.flip(img,0)
            
            img = detector.findHands(img)
            lmList, bbox = detector.findPosition(img)
            if len(lmList)!=0:
                cFingers = detector.fingersUp()
                #print(cFingers)
                cGesture = detector.matchGesture(cFingers)
                #print(cGesture)
        if True: # Mouse
            #print("mouseStuff")
            if mouseToggleOn: #mouse toggle
                #print("mouse Toggle")
                if len(lmList)!=0:
                    #print(inputGestures[0])
                    #print(cGesture)
                    #print(str(inputGestures[0]) == str(cGesture))
                    if (str(inputGestures[0]) == str(cGesture) and switchWatch>switchDelay):
                        switchWatch=0
                        if mouseOn:
                            mouseOn=False
                        else:
                            mouseOn=True
                            keybindsOn=False
                            volBrightOn=False
                        # success, img = cap.read() 
                        # img = detector.findHands(img)
                        # lmList, bbox = detector.findPosition(img)
                        # cFingers = detector.fingersUp()
                        print('mouse', mouseOn)
            if mouseOn: #Mouse Control 
                #print("mouse on")
                if len(lmList)!=0:
                    mx,my = lmList[5][1:]
                    x1,y1 = lmList[4][1:] #for using distance to click 
                    x2,y2 = lmList[5][1:]

                    #x1,y1 = lmList[8][1:] #for using distance to click 
                    #x2,y2 = lmList[7][1:]

                # check which fingers are up
                    fingers = detector.fingersUp()
                    #print(fingers)
                # Moving mode w/ index 1st knuckle only
                    cv2.rectangle(img, (frameR,frameR), (int(wCam-frameR),int(hCam-frameR)), (255,0,0), 2,)
                
                    if fingers[1]==1 and fingers[2]==1 :
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
                        #print("x diff", abs(mx-lastX))
                        #print("y diff", abs(my-lastY))
                        #print(mouse.onScreen(mouseX, mouseY))
                    #Gives a small dead zone to hand movements to prevent jitter
                        if abs(mx-lastX)>0.001*wScreen or abs(my-lastY)>0.001*hScreen:
                            time1 = time.time()

                            #relative position movement based on hand motion.
                            fastMouse.move((mouseX-lastMouseX)*mouseSens, (mouseY-lastMouseY)*mouseSens, absolute=False)
                            #mouse.moveRel((mouseX-lastMouseX)*mouseSens, (mouseY-lastMouseY)*mouseSens)

                            #absolute position movement based on hand position in frame
                            #mouse.moveTo(mouseX, mouseY)
                            #print(time.time()-time1)
                        length, img, _ = detector.findDistance(5,4,img)
                        length2, img, _ = detector.findDistance(5,13,img)

                        if length<length2 and clickWatch>clickDelay:
                            clickWatch=0
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
        
        if True: #Volume and Brightness Control:
            if volBrightToggleOn: #Volume and Brightness Toggle
                #print("VolBright Toggle")
                if len(lmList)!=0:
                    #print(cFingers)
                    #print(cGesture)
                    #print(switchWatch)
                    if (str(inputGestures[1]) == str(cGesture) and switchWatch>switchDelay):
                        switchWatch=0
                        if volBrightOn:
                            volBrightOn=False
                        else:
                            volBrightOn=True
                            keybindsOn=False
                            mouseOn=False
                        # success, img = cap.read() 
                        # img = detector.findHands(img)
                        # lmList, bbox = detector.findPosition(img)
                        # cFingers = detector.fingersUp()
                        print('Volume and Brightness', volBrightOn)    
            if volBrightOn: 
                #print("volBright On")
                if len(lmList) != 0:

                    # Filter based on size
                    area = (bbox[2] - bbox[0]) * (bbox[3] - bbox[1]) // 100
                    print(area)
                    
                    # Find Distance between index and Thumb
                    length, img, lineInfo = detector.findDistance(4, 8, img)
                    compLengthMin, img, lineInfo = detector.findDistance(5, 9, img)
                    compLengthMax, img, lineInfo = detector.findDistance(0, 5, img)
                    
                    # print(length)

                    # Convert Volume
                    volBar = np.interp(length, [compLengthMin, compLengthMax*1.2], [400, 150])
                    volPer = np.interp(length, [compLengthMin, compLengthMax*1.2], [0, 100])
                    
                    brightBar = np.interp(length, [compLengthMin, compLengthMax*1.2], [400, 150])
                    brightPer = np.interp(length,[compLengthMin, compLengthMax*1.2], [0,100])
                    
                    # Reduce Resolution to make it smoother
                    smoothness = 10
                    volPer = smoothness * round(volPer / smoothness)
                    brightPer = smoothness* round(brightPer/smoothness)
                    # Check fingers up
                    fingers = detector.fingersUp()
                    # print(fingers)

                    # If pinky is down set volume
                    if not fingers[4]:
                        volume.SetMasterVolumeLevelScalar(volPer / 100, None)
                        cv2.circle(img, (lineInfo[4], lineInfo[5]), 15, (0, 255, 0), cv2.FILLED)
                        colorVol = (0, 255, 0)
                    else:
                        colorVol = (255, 0, 0)
                        
                    #if Ring is down set brightness
                    if not fingers[3]:
                        cBright = brightPer
                        sbc.set_brightness(brightPer)
                        cv2.circle(img, (lineInfo[4], lineInfo[5]), 15, (0, 255, 0), cv2.FILLED)
                        colorBright = (0, 0, 255)
                    else:
                        colorBright = (0, 255, 0)
                if True: # Drawings
                    cv2.rectangle(img, (50, 150), (85, 400), colorVol, 3)
                    cv2.rectangle(img, (50, int(volBar)), (85, 400), colorVol, cv2.FILLED)
                    
                    cv2.rectangle(img, (150, 150), (185, 400), colorBright, 3)
                    cv2.rectangle(img, (150, int(brightBar)), (185, 400), colorBright, cv2.FILLED)
                    
                    cv2.putText(img, f'{int(volPer)} %', (40, 450), cv2.FONT_HERSHEY_COMPLEX,
                                1, (255, 0, 0), 3)
                    cVol = int(volume.GetMasterVolumeLevelScalar() * 100)
                    
                    cv2.putText(img, f'Vol Set: {int(cVol)}', (400, 50), cv2.FONT_HERSHEY_COMPLEX,
                                1, colorVol, 3)
                    cv2.putText(img, f'Bright Set: {int(cBright)}', (350, 150), cv2.FONT_HERSHEY_COMPLEX,
                                1, colorBright, 3)
                    
                    cv2.imshow('Computer Control', img)
        
        if True: #Keybinds
            if keybindsToggleOn:
                if len(lmList)!=0:
                    if (str(inputGestures[2]) == str(cGesture) and switchWatch>switchDelay):
                        switchWatch=0
                        if keybindsOn:
                            keybindsOn=False
                        else:
                            keybindsOn=True
                            volBrightOn=False
                            mouseOn=False
                        print('Keybinds', keybindsOn)
            if keybindsOn:
                #print(cFingers)
               
                #print(inputGestures)
                #print(outputBindings)
                #print(outputBindings)
                cv2.putText(img, 'Keybinds On', (350, 150), cv2.FONT_HERSHEY_COMPLEX,
                                1, [255,255,0], 3)
                index=0
                for gesture in inputGestures:
                    #print(gesture)
                    #print(cGesture)
                    #print(str(cGesture)==str(gesture))

                    #print(cGesture.equals(gesture))
                    if(str(gesture) == str(cGesture) and index<len(outputBindings)):
                        if(switchWatch>switchDelay):
                            switchWatch=400
                            mouse.press(outputBindings[index])
                            print("Activated: ",outputBindings[index])
                        else:
                            print("TimeWait: ", outputBindings[index])
                        #print(cGesture)
                        #print(inputGestures[index])
                        
                    index+=1
        
        if True: # frame rate and Clock 
            cTime = time.time()
            if(cTime-pTime>0):
                fps = 1/(cTime-pTime)
            #Increment Clickwatch by time elapsed
            clickWatch+=cTime-pTime
            switchWatch+=cTime-pTime
            pTime = cTime
            cv2.putText(img, str(int(fps)),(20,50),cv2.FONT_HERSHEY_SIMPLEX,2,[255,0,0],3)
     
        #Escape
        if cv2.waitKey(1) ==ord('q'):
            print("Exit")
            break

        # Display
        cv2.imshow('Computer Control', img)
    
    cv2.destroyAllWindows()
    cap.release()
    

#run program by creating window and getting values
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
        break
    if event == 'Start':
        print('Stuff: ', values)
        if(True):
            mouseToggleOn = values[5]
            volBrightToggleOn = values[6]
            mouseSensIn = values[1]
            clickDelayIn = values[2]
            bindingsOut = functionsList
            gesturesIn = [values[7],values[8],values[9],values[10],values[11],values[12],values[13],values[14],values[15]]
            cameraNameIn = values[0]
            keybindsOn = True
            wip(mouseToggleOn,volBrightToggleOn,mouseSensIn,clickDelayIn,gesturesIn,bindingsOut,cameraNameIn,keybindsOn)
        #Comment this break to return to settings screen on gesture control close.
        #break
        
    #print('You entered ', values[0])
    
window.close()