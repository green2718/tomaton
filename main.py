
import picamera
from time import sleep
from gpiozero import LED
from IO.Buzzer import Buzzer
from UI import UI
import config as cfg

# import pygame
# from pygame import locals as pyloc
import cv2

import io





FREQ = 2000
DUREE = 2

LARGEUR_ECRAN     = 1280
HAUTEUR_ECRAN    = 1024

# def initCamera(camera):
#     #camera settings
#     camera.resolution            = (LARGEUR_ECRAN, HAUTEUR_ECRAN)
#     camera.framerate             = 24
#     camera.sharpness             = 0
#     camera.contrast              = 0
#     camera.brightness            = 50
#     camera.saturation            = 0
#     camera.ISO                   = 0
#     camera.video_stabilization   = False
#     camera.exposure_compensation = 0
#     camera.exposure_mode         = 'auto'
#     camera.meter_mode            = 'average'
#     camera.awb_mode              = 'auto'
#     camera.image_effect          = 'none'
#     camera.color_effects         = None
#     camera.rotation              = 0
#     camera.hflip                 = True
#     camera.vflip                 = True
#     #camera.crop                  = (0.0, 0.0, 1.0, 1.0)
#     camera.crop                  = (0.0, 0.0, 0.0, 0.0)

# TEXT_COLOR = (255, 255, 255)
# TEXT_SIZE = 10
# TEXT_FONT = cv2.FONT_HERSHEY_SIMPLEX
# TEXT_TICKNESS = 20


if __name__ == "__main__":

    ENABLE_FOUR = False
    ENABLE_PRINT = True


    # pygame.init()
    # screen = pygame.display.set_mode((1280,1024), pyloc.RESIZABLE)
    # width, height = screen.get_size()

    cv2.namedWindow(cfg.WINDOW_NAME, cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty(cfg.WINDOW_NAME, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    vc = cv2.VideoCapture(0)

    if vc.isOpened(): # try to get the first frame
        w = vc.get(cv2.CAP_PROP_FRAME_WIDTH)
        h = vc.get(cv2.CAP_PROP_FRAME_HEIGHT)
        ratio = h/w
        print(w, h, ratio)
        ww = cfg.CAMERA_WIDTH
        #hh = round(ww*ratio)
        hh = round(ww * cfg.PRINT_RATIO)
        # hh = cfg.CAMERA_HEIGHT
        # ww = round(hh / cfg.PRINT_RATIO)
        vc.set(cv2.CAP_PROP_FRAME_WIDTH, ww)
        vc.set(cv2.CAP_PROP_FRAME_HEIGHT, hh)

        w = vc.get(cv2.CAP_PROP_FRAME_WIDTH)
        h = vc.get(cv2.CAP_PROP_FRAME_HEIGHT)
        ratio = h/w
        print(w, h, ratio)
        rval, frame = vc.read()

        ui = UI(frame, ENABLE_FOUR, ENABLE_PRINT)
    else:
        rval = False



    while rval:
        ui.updateScene()
        frame = ui.drawScene(frame)

        rval, frame = vc.read()
        key = cv2.waitKey(20)
        if key == 27: # exit on ESC
            break

    vc.release()
    cv2.destroyWindow(cfg.WINDOW_NAME)

