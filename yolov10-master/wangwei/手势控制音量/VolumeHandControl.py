### 手势控制设备音量

import cv2
import HandTrackingModule as htm
import numpy as np
import time
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
volumeRange = volume.GetVolumeRange()  # (-63.5, 0.0, 0.03125)
minVol = volumeRange[0]
maxVol = volumeRange[1]

#############################
wCam, hCam = 640, 480
#############################
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # 若使用笔记本自带摄像头则编号为0  若使用外接摄像头 则更改为1或其他编号
cap.set(3, wCam)
cap.set(4, hCam)
if not cap.isOpened():
    print("打开摄像头失败！")

pTime = 0
detector = htm.handDetector()

while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)
    if len(lmList) != 0:
        # print(lmList[4], lmList[8])
        x1, y1, x2, y2 = lmList[4][1], lmList[4][2], lmList[8][1], lmList[8][2]
        xc, yc = (x2 + x1) // 2, (y2 + y1) // 2
        cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
        cv2.circle(img, (x2, y2), 15, (255, 0, 255), cv2.FILLED)
        cv2.circle(img, (xc, yc), 15, (255, 0, 255), cv2.FILLED)
        cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)

        length = math.hypot(x2 - x1, y2 - y1)  # 15--200
        if length < 25:
            cv2.circle(img, (xc, yc), 15, (0, 255, 0), cv2.FILLED)
        # print(length)   # 25--230
        # 下面实现长度到音量的转换
        vol = np.interp(length, [15, 200], [minVol, maxVol])
        volume.SetMasterVolumeLevel(vol, None)
        volBar = np.interp(length, [15, 200], [350, 150])
        volPer = np.interp(length, [15, 200], [0, 100])

        cv2.rectangle(img, (20, 150), (50, 350), (255, 0, 255), 2)
        cv2.rectangle(img, (20, int(volBar)), (50, 350), (255, 0, 255), cv2.FILLED)
        cv2.putText(img, f'{int(volPer)}%', (10, 380), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 255), 2)

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, f'fps: {int(fps)}', (10, 40), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)

    cv2.imshow("Image", img)
    cv2.waitKey(1)
