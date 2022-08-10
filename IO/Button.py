
import RPi.GPIO as GPIO

class Button:

    PRESSED = GPIO.RISING
    RELEASED = GPIO.FALLING


    def __init__(self, pin):
        GPIO.setmode(GPIO.BCM)

        self.pin = pin
        GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        GPIO.add_event_detect(self.pin, Button.RELEASED, bouncetime=200)


    def isTriggered(self):
        return GPIO.event_detected(self.pin)
