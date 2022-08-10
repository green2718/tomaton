#!/usr/bin/python3
# -*- coding: utf-8 -*

# Programme de "Photomaton" avec possibilité de 1 photo ou 3 photos/page ou 8 photos/page
# Script TRES fortement basé sur un travail trouvé sur Internet et appelé
# boothy - Photobooth application for Raspberry Pi
# developed by Kenneth Centurion
#
# La version d'origine a été réalisée par Alban TREVILLY en juin 2019 sur Raspberry Pi modèle 3B+
# Travail personnel effectué par plaisir, pour apprendre mais aussi pour rendre service, notamment à Julien.
#
# Cette version a été retravaillée à partir de juin 2020 (pur hasard) et fait écho à la vidéo réalisée par "SVT avec M. Reynoard" et disponible dans la PlayList "Instant Geek"
# Lien direct ici : https://www.youtube.com/watch?v=iD0Ly8lbTig
# En effet, cette vidéo m'a donné envie de retravailler ce script qui était un de mes premiers essais en Python.
#
# Et comme Sebation L va se marier ...
#
# Et comme un internaute (Salut Mickaël) m'a demandé de l'aide pour offrir un bel anniversaire pour les 7 ans de sa fille ...
#
# Et comme ...
#
# Bon, bref, au final, 
#
# Cette application :
# - Prendra soit 1 photo, soit 3 photos, soit 8 photos.
# - Superposera un texte à l'écran avec un compte à rebours (délai de 2 à 5 secondes).
# - Si choix de 3 photos, fusionnera les 3 photos +  une image "logo" dans une grille de 4.
# - Si choix de 8 photos, fusionnera les 8 photos + une image "logo") dans une grille de 9.
# L'image finale (la photo seule ou la grille de 4 ou 9) est ensuite affichée.
# Un post traitement est appliqué pour ajouter des marges sur les côtés afin que les photos soient imprimables sur le Net.
# Chez cewe.fr, elles passent par défaut en mode 11x15 (gardez le paramètre "Format variable" par défaut)
# Et chez photobox.fr, il suffit de sélectionner le format 11x15  

import picamera
import itertools
import subprocess
import os
from shutil import copyfile
import sys
import time
from datetime import datetime
import logging
import RPi.GPIO as GPIO
from PIL import Image, ImageDraw, ImageFont
import pygame
from pygame.locals import *

pygame.mixer.init()
son = pygame.mixer.Sound('/home/pi/Photomaton_x1x4x9_fond/son.wav')

IMG1             = "1.jpg"
IMG2             = "2.jpg"
IMG3             = "3.jpg"
IMG4             = "4.jpg"
IMG4logo             = "4logo.jpg"
IMG5             = "5.jpg"
IMG6             = "6.jpg"
IMG7             = "7.jpg"
IMG8             = "8.jpg"
#IMG9             = "9.jpg"
IMG9logo             = "9logo.jpg"
IMG1a4           = "1a4.jpg"
IMG1a9           = "1a9.jpg"
#CurrentWorkingDir= "/home/pi/Photomaton_x1x4x9_fond/"
CurrentWorkingDir= "/var/www/html/"
logDir           = "logs"
archiveDir       = "photos"

LARGEUR_ECRAN     = 1280
HAUTEUR_ECRAN    = 1024
LARGEUR_PHOTO      = 2560
HAUTEUR_PHOTO     = 2048
LARGEUR_PHOTOx4      = 1280
HAUTEUR_PHOTOx4     = 1024
LARGEUR_PHOTOx8      = 640
HAUTEUR_PHOTOx8     = 512
LED_PIN          = 19 # Si des LED sont ajoutées en 12V sur un Relai.
PHOTO_DELAY      = 5 # Délai en secondes avant prise de la photo
PHOTO_DELAY_bis      = 2 #Délai en secondes avant prise des photos en rafale
STOP_DELAI      = 5 # Délai en secondes avant extinction du système
overlay_renderer = None
buttonEvent      = False
buttonEvent2      = False
buttonEvent3      = False
buttonEvent_redemarre      = False
buttonEvent_stop      = False


pygame.init()
screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
#screen = pygame.display.set_mode((1280,1024),RESIZABLE)
width, height = screen.get_size()

#on initialise les GPIO en écoute
#Attention au choix des ports ; référez-vous au site https://fr.pinout.xyz/
GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(LED_PIN, GPIO.OUT)
GPIO.setup(5, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    
#Modification de l'image solo
def convertMergeImages2(fileName):
    addPreviewOverlay(150,200,45,"Enregistrement et affichage ...")
    #Modifier maintenant l'image solo
    subprocess.call(["montage",
                     IMG1,
                     "-geometry", "+2+2",
                     fileName])
    logging.info("Photo transformée.")

#Ajouter des marges pour format 11x15 (impression photo au format 11x15 cm)
def convertMergeImages2_10x15(fileName):
    #Modifier maintenant l'image solo
    subprocess.call(["montage",
                     fileName,
                     "-geometry", "+85+0",
                     fileName])
    logging.info("Photo transformée.")


#Fusionner les 4 images
def convertMergeImages(IMG1a4):
    addPreviewOverlay(150,200,45,"Fusion des images et affichage ...")
    #fusionner maintenant toutes les images
    subprocess.call(["montage",
                     IMG2,IMG1,IMG4logo,IMG3,
###                     IMG2,IMG1,IMG4,IMG3,
                     "-tile", "2x2",
                     "-geometry", "+10+10",
                     IMG1a4])
    logging.info("Les 4 photos ont été fusionnées.")

#Ajouter des marges pour format 11x15 (impression photo au format 11x15 cm)
def convertMergeImages_10x15(fileName):
    #ajouter des marges
    subprocess.call(["montage",
                     IMG1a4,
                     "-geometry", "+92+0",
                     fileName])
    logging.info("Photo transformée.")
    
  
#Fusionner les 9 images
def convertMergeImages3(IMG1a9):
    addPreviewOverlay(150,200,45,"Fusion des images et affichage ...")
    #fusionner maintenant toutes les images
    subprocess.call(["montage",
                     IMG3,IMG2,IMG1,IMG6,IMG5,IMG4,IMG9logo,IMG8,IMG7,
                     "-tile", "3x3",
                     "-geometry", "+2+2",
                     IMG1a9])
    logging.info("Les 9 photos ont été fusionnées.")

#Ajouter des marges pour format 11x15 (impression photo au format 11x15 cm)
def convertMergeImages3_10x15(fileName):
    #ajouter des marges
    subprocess.call(["montage",
                     IMG1a9,
                     "-geometry", "+66+0",
                     fileName])
    logging.info("Photo transformée.")    

#Supprimer les pré-images (celles avant transformation)
def deleteImages(fileName):
    logging.info("Suppression des anciennes images.")
    if os.path.isfile(IMG1):
        os.remove(IMG1)
    if os.path.isfile(IMG2):
        os.remove(IMG2)
    if os.path.isfile(IMG3):
        os.remove(IMG3)
    if os.path.isfile(IMG4):
        os.remove(IMG4)
    if os.path.isfile(IMG5):
        os.remove(IMG5)
    if os.path.isfile(IMG6):
        os.remove(IMG6)
    if os.path.isfile(IMG7):
        os.remove(IMG7)
    if os.path.isfile(IMG8):
        os.remove(IMG8)
#    if os.path.isfile(IMG9):
#        os.remove(IMG9)
    if os.path.isfile(IMG1a4):
        os.remove(IMG1a4)
    if os.path.isfile(IMG1a9):
        os.remove(IMG1a9)
    if os.path.isfile(fileName):
        os.remove(fileName);

def cleanUp():
    GPIO.cleanup()
    
def archiveImage(fileName):
    logging.info("Sauvegarde de l'image : "+fileName)
    copyfile(fileName,archiveDir+"/"+fileName)

def precapture1(imageName):
    addPreviewOverlay(100,50,80,"Photo dans 5 secondes !" )

def precapture1_bis(imageName):
    addPreviewOverlay(100,50,80,"Photo dans 2 secondes !" )

def precapture2(imageName):
    addPreviewOverlay(100,100,100,"Souriez !!!")


def countdownFrom(secondsStr):
    secondsNum = int(secondsStr)
    if secondsNum >= 0 :
        while secondsNum > 0 :
            addPreviewOverlay(50,50,240,str(secondsNum))
            time.sleep(1)
            secondsNum=secondsNum-1


def countdownFromStop(secondsStr):
    secondsNum = int(secondsStr)
    if secondsNum >= 0 :
        while secondsNum > 0 :
            addPreviewOverlay(50,50,240,str(secondsNum))
            time.sleep(1)
            secondsNum=secondsNum-1
            
def captureImage(imageName):
    #Sauvegarde de l'image
    camera.capture(imageName, resize=(LARGEUR_PHOTO, HAUTEUR_PHOTO))
    logging.info("Image "+imageName+" enregistrée.")

def captureImagex4(imageName):
    #Sauvegarde de l'image
    camera.capture(imageName, resize=(LARGEUR_PHOTOx4, HAUTEUR_PHOTOx4))
    logging.info("Image "+imageName+" enregistrée.")

def captureImagex9(imageName):
    #Sauvegarde de l'image
    camera.capture(imageName, resize=(LARGEUR_PHOTOx8, HAUTEUR_PHOTOx8))
    logging.info("Image "+imageName+" enregistrée.")

def addPreviewOverlay(xcoord,ycoord,fontSize,overlayText):
    global overlay_renderer
    img = Image.new("RGBA", (LARGEUR_ECRAN, HAUTEUR_ECRAN))
    draw = ImageDraw.Draw(img)
    draw.font = ImageFont.truetype(
                    #"/usr/share/fonts/truetype/freefont/FreeSerif.ttf",fontSize)
                    "/home/pi/Photomaton_x1x4x9_fond/Retrofunk_Script_Personal_Use.otf",fontSize)

    draw.text((xcoord,ycoord), overlayText, (206, 206, 206))

    if not overlay_renderer:
        overlay_renderer = camera.add_overlay(img.tobytes(),
                                              layer=3,
                                              size=img.size,
                                              alpha=128);
    else:
        overlay_renderer.update(img.tobytes())

#lancer une action complète pour 4 photos
def photox4():

    logging.info("Démarrage de la séquence '4 photos'")

    initCamera(camera)
    logging.info("Démarrage de l'aperçu")
    camera.start_preview()

    fileName = time.strftime("%Y-%m-%d_%Hh%Mm%S")+".jpg"
    fileName_10x15 = time.strftime("%Y-%m-%d_%Hh%Mm%S")+".jpg"
    logging.info("Nom de fichier créé : "+fileName)
    
    TimeExif = time.strftime("%Y:%m:%d-%H:%M:%S")

    #turn on flash
    GPIO.output(LED_PIN,GPIO.HIGH)

    precapture1(fileName)
    time.sleep(2)
    countdownFrom(PHOTO_DELAY)
    precapture2(fileName)
    canal = son.play()
    
    captureImagex4(IMG1)
    time.sleep(1)

    precapture1_bis(fileName)
    time.sleep(2)
    countdownFrom(PHOTO_DELAY_bis)
    precapture2(fileName)
    canal = son.play()
    
    captureImagex4(IMG2)
    time.sleep(1)

    precapture1_bis(fileName)
    time.sleep(2)
    countdownFrom(PHOTO_DELAY_bis)
    precapture2(fileName)
    canal = son.play()
    
    captureImagex4(IMG3)
    time.sleep(1)

    #precapture1_bis(fileName)
    #time.sleep(2)
    #countdownFrom(PHOTO_DELAY_bis)
    #precapture2(fileName)
    #canal = son.play()
    
    #captureImagex4(IMG4)
    #time.sleep(1)
    
    convertMergeImages(IMG1a4)
    
    addPreviewOverlay(100,100,85,"Merci !")
    camera.stop_preview()
    
    #turn off flash
    GPIO.output(LED_PIN,GPIO.LOW)
    
    os.system("convert -flop "+IMG1a4+" "+IMG1a4+"")

    AfficherPhoto(IMG1a4)
    addPreviewOverlay(100,100,85,"Waouh !!! Jolie photo !!!")
    #time.sleep(5)
    
    convertMergeImages_10x15(fileName)

    os.system("jhead -mkexif "+fileName+"")
    os.system("jhead -ts"+TimeExif+" "+fileName+"")
    
    os.system('exiftool -artist="Cabine Photos par Alban TREVILLY" '+fileName+' -overwrite_original')
    os.system('exiftool -copyright="Copyright (c) 2019-2020 = Lui, Moi, Nous !!!" '+fileName+' -overwrite_original')
    os.system('exiftool -xmp:dateTimeOriginal="'+TimeExif+'" '+fileName+' -overwrite_original')
    os.system('exiftool -AllDates="'+TimeExif+'" '+fileName+' -overwrite_original')
  
    archiveImage(fileName)

    deleteImages(fileName)    

    AfficherPhoto("/home/pi/Photomaton_x1x4x9_fond/accueil.jpg")
    addPreviewOverlay(20,100,35,"--> Rouge = 1 photo ; Noir = 4 photos ; Blanc = vidéos")


#lancer une action complète pour 1 photo et impression
def photox1():
    logging.info("Démarrage de la séquence '4 photos'")

    initCamera(camera)
    logging.info("Démarrage de l'aperçu")
    camera.start_preview()

    fileName = time.strftime("%Y-%m-%d_%Hh%Mm%S")+".jpg"
    fileName_10x15 = time.strftime("%Y-%m-%d_%Hh%Mm%S")+".jpg"
    logging.info("Nom de fichier créé : "+fileName)

    TimeExif = time.strftime("%Y:%m:%d-%H:%M:%S")

    #turn on flash
    GPIO.output(LED_PIN,GPIO.HIGH)

    precapture1(fileName)
    time.sleep(2)
    countdownFrom(PHOTO_DELAY)
    precapture2(fileName)
    canal = son.play()
    
    captureImage(IMG1)
    time.sleep(1)

    addPreviewOverlay(100,100,55,"Merci !")
    camera.stop_preview()
    
    #turn off flash
    GPIO.output(LED_PIN,GPIO.LOW)
    
    os.system("convert -flop "+IMG1+" "+fileName+"")
    time.sleep(1)
    
    os.system("convert "+fileName+" /home/pi/Photomaton_x1x4x9_fond/tampon.png -gravity SouthEast -composite "+fileName+"")

    AfficherPhoto(fileName_10x15)
    addPreviewOverlay(100,100,45,"Waouh !!! Jolie photo !!!")
    
    convertMergeImages2_10x15(fileName)
    
    archiveImage(fileName_10x15)

    os.system("jhead -mkexif "+fileName+"")
    os.system("jhead -ts"+TimeExif+" "+fileName+"")
    
    os.system('exiftool -artist="Cabine Photos par Alban TREVILLY" '+fileName+' -overwrite_original')
    os.system('exiftool -copyright="Copyright (c) 2019-2020 = Lui, Moi, Nous !!!" '+fileName+' -overwrite_original')
    os.system('exiftool -xmp:dateTimeOriginal="'+TimeExif+'" '+fileName+' -overwrite_original')
    os.system('exiftool -AllDates="'+TimeExif+'" '+fileName+' -overwrite_original')
      
    archiveImage(fileName)

    deleteImages(fileName)

    AfficherPhoto("/home/pi/Photomaton_x1x4x9_fond/accueil.jpg")
    addPreviewOverlay(20,100,35,"--> Rouge = 1 photo ; Noir = 4 photos ; Blanc = vidéos")
    

#lancer une action complète pour 9 photos
def photox9():
    logging.info("Démarrage de la séquence '1 photo'")
    
    pygame.mouse.set_visible(False) # Hide the mouse pointer

    initCamera(camera)
    logging.info("Démarrage de l'aperçu")
    camera.start_preview()

    fileName = time.strftime("%Y-%m-%d_%Hh%Mm%S")+".jpg"
    logging.info("Nom de fichier créé : "+fileName)

    TimeExif = time.strftime("%Y:%m:%d-%H:%M:%S")

    #turn on flash
    GPIO.output(LED_PIN,GPIO.HIGH)

    precapture1(fileName)
    time.sleep(2)
    countdownFrom(PHOTO_DELAY)
    precapture2(fileName)
    canal = son.play()
    
    captureImagex9(IMG1)
    time.sleep(1)
    
    precapture1_bis(fileName)
    time.sleep(2)
    countdownFrom(PHOTO_DELAY_bis)
    precapture2(fileName)
    canal = son.play()
    
    captureImagex9(IMG2)
    time.sleep(1)
        
    precapture1_bis(fileName)
    time.sleep(2)
    countdownFrom(PHOTO_DELAY_bis)
    precapture2(fileName)
    canal = son.play()
    
    captureImagex9(IMG3)
    time.sleep(1)
        
    precapture1_bis(fileName)
    time.sleep(2)
    countdownFrom(PHOTO_DELAY_bis)
    precapture2(fileName)
    canal = son.play()
    
    captureImagex9(IMG4)
    time.sleep(1)
        
    precapture1_bis(fileName)
    time.sleep(2)
    countdownFrom(PHOTO_DELAY_bis)
    precapture2(fileName)
    canal = son.play()
    
    captureImagex9(IMG5)
    time.sleep(1)
        
    precapture1_bis(fileName)
    time.sleep(2)
    countdownFrom(PHOTO_DELAY_bis)
    precapture2(fileName)
    canal = son.play()
    
    captureImagex9(IMG6)
    time.sleep(1)
        
    precapture1_bis(fileName)
    time.sleep(2)
    countdownFrom(PHOTO_DELAY_bis)
    precapture2(fileName)
    canal = son.play()
    
    captureImagex9(IMG7)
    time.sleep(1)
        
    precapture1_bis(fileName)
    time.sleep(2)
    countdownFrom(PHOTO_DELAY_bis)
    precapture2(fileName)
    canal = son.play()
    
    captureImagex9(IMG8)
    time.sleep(1)
        
    #precapture1_bis(fileName)
    #time.sleep(2)
    #countdownFrom(PHOTO_DELAY_bis)
    #precapture2(fileName)
    #canal = son.play()
    
    #captureImagex9(IMG9)
    #time.sleep(1)
        
    camera.stop_preview()
    addPreviewOverlay(100,100,55,"Merci !")
    
    #turn off flash
    GPIO.output(LED_PIN,GPIO.LOW)
    
    convertMergeImages3(IMG1a9)
    os.system("convert -flop "+IMG1a9+" "+IMG1a9+"")

    AfficherPhoto(IMG1a9)
    addPreviewOverlay(100,100,45,"Waouh !!! Jolie photo !!!")
    
    convertMergeImages3_10x15(fileName)

    os.system("jhead -mkexif "+fileName+"")
    os.system("jhead -ts"+TimeExif+" "+fileName+"")

    os.system('exiftool -artist="Cabine Photos par Alban TREVILLY" '+fileName+' -overwrite_original')
    os.system('exiftool -copyright="Copyright (c) 2019-2020 = Lui, Moi, Nous !!!" '+fileName+' -overwrite_original')
    os.system('exiftool -xmp:dateTimeOriginal="'+TimeExif+'" '+fileName+' -overwrite_original')
    os.system('exiftool -AllDates="'+TimeExif+'" '+fileName+' -overwrite_original')
  
    archiveImage(fileName)

    deleteImages(fileName)    

    AfficherPhoto("/home/pi/Photomaton_x1x4x9_fond/accueil.jpg")
    addPreviewOverlay(20,100,35,"--> Rouge = 1 photo ; Noir = 4 photos ; Blanc = vidéos")


def initCamera(camera):
    logging.info("Initialisation de la caméra.")
    #camera settings
    camera.resolution            = (LARGEUR_ECRAN, HAUTEUR_ECRAN)
    camera.framerate             = 24
    camera.sharpness             = 0
    camera.contrast              = 0
    camera.brightness            = 50
    camera.saturation            = 0
    camera.ISO                   = 0
    camera.video_stabilization   = False
    camera.exposure_compensation = 0
    camera.exposure_mode         = 'auto'
    camera.meter_mode            = 'average'
    camera.awb_mode              = 'auto'
    camera.image_effect          = 'none'
    camera.color_effects         = None
    camera.rotation              = 0
    camera.hflip                 = True
    camera.vflip                 = False
    #camera.crop                  = (0.0, 0.0, 1.0, 1.0)
    camera.crop                  = (0.0, 0.0, 0.0, 0.0)

def initLogger(output_dir):
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    # create console handler and set level to info
    handler = logging.StreamHandler()
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    # create error file handler and set level to error
    handler = logging.FileHandler(output_dir+"/"+time.strftime("%Y%m%d")+"_error.log","w", encoding=None, delay="true")
    handler.setLevel(logging.ERROR)
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    # create debug file handler and set level to debug
    handler = logging.FileHandler(output_dir+"/"+time.strftime("%Y%m%d")+"_debug.log","w", encoding=None, delay="true")
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)


def onButtonPress():
    logging.info("Demande faite pour 1 grille de 4 !")
    photox4()
    #Affichage du message d'accueil
    addPreviewOverlay(20,100,45," --> Blanc = 1 photo / Noir = 3 photos / Rouge = 8 photos")

def onButtonPressBis():
    logging.info("Demande faite pour 1 seule grande photo !")
    photox1()
    #Affichage du message d'accueil
    addPreviewOverlay(20,100,45," --> Blanc = 1 photo / Noir = 3 photos / Rouge = 8 photos")

def onButtonPressTer():
    logging.info("Demande faite pour 1 grille de 9 !")
    photox9()
    #Affichage du message d'accueil
    addPreviewOverlay(20,100,45," --> Blanc = 1 photo / Noir = 3 photos / Rouge = 8 photos")
    
def onButtonPress_redemarre():
    logging.info("Redémarrage demandé")
    addPreviewOverlay(80,200,65,"Le système va redémarrer")
    time.sleep(3)
    os.system("sudo reboot")

def onButtonPress_stop():
    logging.info("Arrêt demandé")
    addPreviewOverlay(20,200,65,"  --> Sauvegarde des images ...")
    time.sleep(2)
    os.system("rsync -av /var/www/html/photos/ /media/pi/PHOTOS01/ && rsync -av /var/www/html/photos/ /media/pi/PHOTOS02/ && rm /var/www/html/photos/2020*" )

    addPreviewOverlay(20,200,65,"  --> Arrêt du système dans 5 secondes")
    time.sleep(3)
    countdownFromStop(STOP_DELAI)
    os.system("sudo poweroff")

  
def onButtonDePress():
    logging.info("Bouton relaché !")
    
def onButtonDePressBis():
    logging.info("Bouton relaché !")

def onButtonDePressTer():
    logging.info("Bouton relaché !")

def onButtonDePress_redemarre():
    logging.info("Redémarrage demandé")

def onButtonDePress_stop():
    logging.info("Arrêt demandé")
    

def AfficherPhoto(fileName): # affiche NomPhoto
    logging.info("loading image: " + fileName)
    background = pygame.image.load(fileName);
    background.convert_alpha()
    background = pygame.transform.scale(background,(LARGEUR_ECRAN, HAUTEUR_ECRAN))
    screen.blit(background,(0,0),(0,0,LARGEUR_ECRAN, HAUTEUR_ECRAN))
    pygame.display.flip()
    pygame.display.update()


#Flux initial
with picamera.PiCamera() as camera:
    os.chdir(CurrentWorkingDir)
    dateAff = time.strftime("Nous sommes le %d:%m:%Y Il est %H:%M")

    pygame.mouse.set_visible(False) # Hide the mouse pointer

    try:
        initLogger(logDir)
        logging.info("Démarrage de l'aperçu")
        addPreviewOverlay(20,200,45,"        Bonjour ; merci pour votre téléchargement")
        time.sleep(3)
        addPreviewOverlay(20,200,45,"      "+dateAff+"")
        time.sleep(3)
        addPreviewOverlay(20,200,45,"    N'hésitez pas à faire un petit don sur mon PayPal")
        time.sleep(3)
        addPreviewOverlay(20,200,45,"               Amusez-vous bien !!! ;-) ")
        time.sleep(3)    
  
        AfficherPhoto("/home/pi/Photomaton_x1x4x9_fond/accueil.jpg")
        addPreviewOverlay(20,100,45," --> Blanc = 1 photo / Noir = 3 photos / Rouge = 8 photos")
        
        logging.info("Démarrage de la boucle du programme")
       
        while True:
            input_state = GPIO.input(24)
            input_state2 = GPIO.input(21)
            input_state3= GPIO.input(18)
            input_state_stop = GPIO.input(5)
            input_state_redemarre= GPIO.input(16)
            
            if input_state == False :
                if buttonEvent == False :
                    buttonEvent = True
                    onButtonPress()
            elif buttonEvent == True :
                    buttonEvent = False
                    onButtonDePress()
        
            if input_state2 == False : 
                if buttonEvent2 == False :
                    buttonEvent2 = True
                    onButtonPressBis()
            else :
                if buttonEvent2 == True :
                    buttonEvent2 = False
                    onButtonDePressBis()
      
            if input_state3 == False : 
                if buttonEvent3 == False :
                    buttonEvent3 = True
                    onButtonPressTer()
            else :
                if buttonEvent3 == True :
                    buttonEvent3 = False
                    onButtonDePressTer()

            if input_state_redemarre == False :
                if buttonEvent_redemarre == False :
                    buttonEvent_redemarre = True
                    onButtonPress_redemarre()
            elif buttonEvent_redemarre == True :
                    buttonEvent_redemarre = False
                    onButtonDePress_redemarre()
        
            if input_state_stop == False :
                if buttonEvent_stop == False :
                    buttonEvent_stop = True
                    onButtonPress_stop()
            elif buttonEvent_stop == True :
                    buttonEvent_stop = False
                    onButtonDePress_stop()
        
                    
    except BaseException:
        logging.error("Erreur non gérée : " , exc_info=True)
        camera.close()
        cleanUp()
    finally:
        logging.info("Au revoir ...")
        cleanUp()
        camera.close()

#end
