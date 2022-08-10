
from time import sleep
from gpiozero import LED, Button

import RPi.GPIO as GPIO

import pigpio

BTN_PIC = 18
BUZZER = 12
LED_RETARD = 14

FREQ = 2000
DUREE = 2



if __name__ == "__main__":
    print("miaou")

    btnPic = Button(BTN_PIC)
    ledRetard = LED(LED_RETARD)

    for k in range(4):
        ledRetard.toggle()
        sleep(0.4)

    notTrigged = True

    print("Wait trig")

    for k in range(4):
        btnPic.wait_for_press()
        btnPic.wait_for_release()
        ledRetard.toggle()


    print("Trigged!")

    
    print("Test buzzer")

    nb_iter = DUREE * FREQ
    period = 1.0/(FREQ*2)

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(BUZZER, GPIO.OUT)

    #buzz = GPIO.PWM(BUZZER, FREQ)
    buzz = pigpio.pi()
    buzz.set_mode(BUZZER, pigpio.OUTPUT)
    
    buzz.hardware_PWM(BUZZER, FREQ, 50 * 10000)

    #buzz.start(50)

    sleep(DUREE)

    #buzz.ChangeFrequency(FREQ // 2)
    buzz.hardware_PWM(BUZZER, FREQ // 2, 50 * 10000)

    sleep(DUREE)

    buzz.hardware_PWM(BUZZER, 0, 0)
    #buzz.stop()
    

    print("Done")


def noway():


    # with picamera.PiCamera() as camera:
    #     initCamera(camera)

    #     x = (screen.get_width() - camera.resolution[0]) / 2
    #     y = (screen.get_height() - camera.resolution[1]) / 2

    #     rgb = bytearray(camera.resolution[0] * camera.resolution[1] * 3)
    #     #camera.start_preview()
    #     sleep(5)
    #     # camera.capture(imageName, resize=(LARGEUR_PHOTO, HAUTEUR_PHOTO))
    #     # precapture1(fileName)
    #     exitFlag = True

    #     stream = io.BytesIO()

    #     while(exitFlag):
    #         for event in pygame.event.get():
    #             if(event.type is pygame.MOUSEBUTTONDOWN or 
    #                event.type is pygame.QUIT):
    #                 exitFlag = False

    #         stream.seek(0)
    #         camera.capture(stream, use_video_port=True, format='rgb')
    #         stream.seek(0)
    #         stream.readinto(rgb)
    #         img = pygame.image.frombuffer(rgb[0:
    #             (camera.resolution[0] * camera.resolution[1] * 3)],
    #             camera.resolution, 'RGB')

    #         screen.fill(0)
    #         if img:
    #             screen.blit(img, (x,y))

    #         pygame.display.update()

    #     stream.close()


    print("miaou")

    #btnPic = Button(BTN_3)
    ledRetard = LED(LED_VERTE)
    buzz = Buzzer(BUZZER)

    for k in range(4):
        ledRetard.toggle()
        sleep(0.4)

    notTrigged = True

    print("Wait trig")

    for k in range(4):
        btnPic.wait_for_press()
        btnPic.wait_for_release()
        ledRetard.toggle()


    print("Trigged!")

    
    print("Test buzzer")

    nb_iter = DUREE * FREQ
    period = 1.0/(FREQ*2)

    
    

    #buzz.start(50)
    buzz.ring(FREQ, DUREE)
    print("Riiiiing")
    sleep(DUREE + 1)
    buzz.ring(FREQ // 2, DUREE, wait=True)

    print("Done")

    # pygame.display.quit()
