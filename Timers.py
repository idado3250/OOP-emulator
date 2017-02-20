from time import time

class Timers():

    def __init__(self):
        self.__delayTimer = 0
        self.__displayTimer = 0
        self.__time = time()

    def decrement(self):
        currentTime = time()
        if currentTime - self.__time >= 0.016666666666667:
            if self.__delayTimer > 0:
                self.__delayTimer -= 1
            if self.__soundTimer > 0:
                self.__soundTimer -= 1
                self.__buzz.play()