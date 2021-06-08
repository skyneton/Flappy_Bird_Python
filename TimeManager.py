import time
 
class TimeManager:
    def __init__(self):
        self.beforeTime = time.time()

    def update(self):
        self.beforeTime = time.time()

    def deltaTime(self):
        now = time.time()
        return (now - self.beforeTime) / 1000