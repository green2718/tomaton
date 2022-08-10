from time import sleep
import threading

class Countdown:

    def __init__(self):
        self.num = 0
        self.numstr = ""

    def isRunning(self):
        return self.num > 0
    
    def startCount(self, num):
        # Restart thread only if not already started
        startMe = self.num == 0
        self.num = num
        self.numstr = f"{self.num}"
        if startMe:
            th = threading.Thread(target=self.__count, args=(1,))
            th.start()

    def __count(self, duration):
        while self.num > 0:
            sleep(duration)
            self.num -= 1
            self.numstr = f"{self.num}"
