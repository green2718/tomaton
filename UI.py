from copy import copy
from Utils.Countdown import Countdown
import config as cfg

from gpiozero import LED, Button
import cv2

import os.path as osp
import os
import shutil
import time


TEXT_COLOR = (255, 255, 255)
TEXT_SIZE = 10
TEXT_FONT = cv2.FONT_HERSHEY_SIMPLEX
TEXT_THICKNESS = 20

BOX_WIDTH = 10
BOX_HEIGHT = 4
BOX_BORDER = 5
BOX_COLOR = (150, 150, 150)
BOX_FILL_COLOR = (255, 255, 255)
BOX_TEXT_SIZE = 1.2
BOX_TEXT_THICKNESS = 3


class UI:

    def __init__(self, firstFrame, enableFour, enablePrint):

        self.enableFour = enableFour
        self.enablePrint = enablePrint

        dim = firstFrame.shape
        self.width = dim[1]
        self.height = dim[0]
        
        boxUnit = self.width / (3 * BOX_WIDTH + 4)
        self.boxX = [int((1 + (BOX_WIDTH + 1) * box) * boxUnit) for box in range(3)]
        self.boxWidth = int(BOX_WIDTH * boxUnit)
        self.boxHeight = int(BOX_HEIGHT * boxUnit)
        self.boxY = self.height - int(boxUnit + BOX_HEIGHT * boxUnit)

        self.scene = UI.Scene.MAIN
        self.pictureCnt = 0
        self.btnActive = -1

        self.cntdwn = Countdown()
        self.btns = [Button(cfg.BTN_1), Button(cfg.BTN_2), Button(cfg.BTN_3)]
    

    def drawScene(self, picture):
        frame =  {
            UI.Scene.MAIN : self.__drawMainScene,
            UI.Scene.CNTDWN : self.__drawCountDown,
            UI.Scene.RES : self.__drawResScene,
            UI.Scene.PICTURE : self.__drawPictureScene
        }.get(self.scene)(picture)

        rszFrame = cv2.resize(frame, (1542, 1080))
        cv2.imshow(cfg.WINDOW_NAME, rszFrame)
    
    def __drawTextMiddle(self, frame, text):
        self.__drawTextCenter(frame, text, (self.width//2, self.height//2), TEXT_FONT, TEXT_SIZE, TEXT_COLOR, TEXT_THICKNESS)
        return frame
    
    def __drawBox(self, frame, text, position, fill=False):
        ptStart = (self.boxX[position], self.boxY)
        ptEnd = (self.boxX[position] + self.boxWidth, self.boxY + self.boxHeight)
        if fill:
            frame = cv2.rectangle(frame, pt1=ptStart, pt2=ptEnd, color=BOX_FILL_COLOR, thickness=-1)
        frame = cv2.rectangle(frame, pt1=ptStart, pt2=ptEnd, color=BOX_COLOR, thickness=BOX_BORDER)

        textBoxPos = (self.boxX[position] + self.boxWidth//2, self.boxY + self.boxHeight//2)
        self.__drawTextCenter(frame, text, textBoxPos, TEXT_FONT, BOX_TEXT_SIZE, BOX_COLOR, BOX_TEXT_THICKNESS)

        return frame

    def __drawMainScene(self, frame):
        posOne = 0 if self.enableFour else 1
        textOne = "1 Photo" if self.enableFour else "Photo"
        frame = self.__drawBox(frame, textOne, posOne, True)

        if self.enableFour:
            frame = self.__drawBox(frame, "4 Photos", 2, True)

        return frame

    def __drawCountDown(self, frame):
        if self.cntdwn.isRunning():
            cnt = self.cntdwn.numstr
            return self.__drawTextMiddle(frame, cnt)

        return frame

    def __drawResScene(self, frame):
        return self.takenPicture
        

    def __drawPictureScene(self, frame):
        cv2.imwrite(cfg.PATH_TMP, frame)

        mFrame = self.__drawBox(frame, "Supprimer", 1, False)
        if self.enablePrint:
            mFrame = self.__drawBox(mFrame, "Imprimer", 0, False)
        self.takenPicture = copy(self.__drawBox(mFrame, "Retour", 2, False))

        return cv2.rectangle(frame, pt1=(0, 0), pt2=(self.width, self.height), color=BOX_FILL_COLOR, thickness=-1)


    def __drawTextCenter(self, frame, text, position, font, size, color, thickness):
        (text_width, text_height) = cv2.getTextSize(text, font, size, thickness)[0]
        posX = position[0] - text_width//2
        posY = position[1] + text_height//2
        cv2.putText(frame, text, (posX, posY), font, size, color, thickness)


    def updateScene(self):
        if self.btnActive != -1:
            if not self.btns[self.btnActive].is_pressed:
                self.btnActive = -1
        elif self.__checkOneButtonOnly():
            {
                UI.Scene.MAIN : self.__updateMainScene,
                UI.Scene.CNTDWN : self.__updateCntDwnScene,
                UI.Scene.RES : self.__updateResScene,
                UI.Scene.PICTURE : self.__updatePictureScene
            }.get(self.scene)()


    def __updateMainScene(self):
        self.picTime = None
        if self.enableFour:
            # 1 photo
            if self.btns[0].is_pressed:
                self.btnActive = 0
                self.scene = UI.Scene.CNTDWN
                self.cntdwn.startCount(cfg.COUNTDOWN_PIC)
            # 4 photos
            elif self.btns[2].is_pressed:
                self.btnActive = 2
                self.scene = UI.Scene.CNTDWN
                self.cntdwn.startCount(cfg.COUNTDOWN_PIC)
                self.pictureCnt = 3

        else:
            # 1 photo
            if self.btns[1].is_pressed:
                self.btnActive = 1
                self.scene = UI.Scene.CNTDWN
                self.cntdwn.startCount(cfg.COUNTDOWN_PIC)

    def __updateCntDwnScene(self):
        if not self.cntdwn.isRunning():
            self.scene = UI.Scene.PICTURE
    
    def __updatePictureScene(self):
        if self.picTime is None:
            self.picTime = time.strftime("%Y%m%d_%H%M%S")

        if self.pictureCnt > 0:
            self.cntdwn.startCount(cfg.COUNTDOWN_BTWN)
            self.scene = UI.Scene.CNTDWN
            os.rename(cfg.PATH_TMP, cfg.PATH_TMP_NUM.format(4-self.pictureCnt))
            self.pictureCnt -= 1
        else:
            self.__savePicture()
            self.scene = UI.Scene.RES

    def __updateResScene(self):
        # Print
        if self.enablePrint and self.btns[0].is_pressed:
            self.btnActive = 0
            pass
        # Suppr
        elif self.btns[1].is_pressed:
            self.btnActive = 1
            self.scene = UI.Scene.MAIN
            self.__deletePicture()
        # Retour
        elif self.btns[2].is_pressed:
            self.btnActive = 2
            self.scene = UI.Scene.MAIN

    def __deletePicture(self):
        os.remove(cfg.PATH_PIC.format(self.picTime))

    def __savePicture(self):
        shutil.copy(cfg.PATH_TMP, cfg.PATH_PIC.format(self.picTime))

    def __checkOneButtonOnly(self):
        return not ((self.btns[0].is_pressed and self.btns[1].is_pressed) or (self.btns[0].is_pressed and self.btns[2].is_pressed) or (self.btns[1].is_pressed and self.btns[2].is_pressed))

    class Scene:
        MAIN = 0
        CNTDWN = 1
        RES = 2
        PICTURE = 3
