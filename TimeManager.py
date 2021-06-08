import time
 
class TimeManager:
    def __init__(self):
        self.__beforeTime = time.time()
        self.__deltaTime = 0

    def update(self):
        now = time.time()
        self.__deltaTime = now - self.__beforeTime
        self.__beforeTime = now

    def deltaTime(self):
        return self.__deltaTime