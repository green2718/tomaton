
import RPi.GPIO as GPIO

class LED:

    def __init__(self, pin):
        GPIO.setmode(GPIO.BCM)
        self.pin = pin
        self.state = False
        GPIO.setup(self.pin, GPIO.OUT)

    def on(self):
        self.state = True
        GPIO.output(self.pin, GPIO.HIGH)

    def off(self):
        self.state = False
        GPIO.output(self.pin, GPIO.LOW)

    def toggle(self):
        if self.state:
            self.off()
        else:
            self.on()
