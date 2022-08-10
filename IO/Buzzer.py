from time import sleep
import pigpio
import threading

class Buzzer:

    DUTY_CYCLE = 50

    def __init__(self, pin):
        self.pin = pin

        self.buzz = pigpio.pi()
        self.buzz.set_mode(pin, pigpio.OUTPUT)


    def on(self, freq):
        self.buzz.hardware_PWM(self.pin, freq, self.DUTY_CYCLE * 10000)

    def off(self):
        self.buzz.hardware_PWM(self.pin, 0, 0)

    def toggle(self):
        if self.state:
            self.off()
        else:
            self.on()

    def __waitOff(self, duration):
        sleep(duration)
        self.off()

    def ring(self, freq, duration, wait=False):
        self.on(freq)
        th = threading.Thread(target=self.__waitOff, args=(duration,))
        th.start()

        if wait:
            th.join()
