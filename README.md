# GestureRecognitionComputerControl

Created by Glen Warren in research for Versatile and Customizable Gesture Recognition Based Computer Control Using Open Source, Inexpensive Computer Vision Technology

This is a work in progress Gesture Recognition System designed for computer control. It uses OpenCV in Python modules and uses the landmark recognition algorithm to identify hand position. It then uses other python libraries (a), to initiate computer control.


a - Libraries/Imports Used
import cv2
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
