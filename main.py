import TimeManager
import turtle
import threading
import time
 
isPlaying = False
isStarting = False

cloudList = []
pipeList = []

destroyCloud = []
destroyPipe = []

WIDTH = 450
HEIGHT = 600
 
timeutil = TimeManager.TimeManager()
player = None

speedRate = 1

cloudTimer = 0
CLOUD_SPAWN_TIME = 5

class GameObject:
    width = 4
    height = 4
 
class PlayerManager(GameObject):
    def __init__(self):
        self.gameObject = turtle.Turtle()
        self.gameObject.shape("turtle")
        self.gameObject.shapesize(1.4)
        turtle.onkeypress(self.jump, "space")
        
    def update(self):
        me = self.gameObject
        
    def jump(self):
        pass

class Cloud:
    CLOUD_SPEED = 2
    def __init__(self):
        self.x = WIDTH/2
        self.y = HEIGHT/4
        self.CLOUD_SPEED *= speedRate
    
    def update(self):
        self.x -= self.CLOUD_SPEED * timeutil.deltaTime()
 
      
 
def message(m1, m2, color="black"):
    turtle.pencolor(color)
    turtle.setposition(0, 100)
    turtle.write(m1, False, "center", ("", 20))
    turtle.setposition(0, -100)
    turtle.write(m2, False, "center", ("", 15))
    turtle.home()
 
def main_screen():
    global isTurtleReady
    turtle.setup(WIDTH, HEIGHT)
    turtle.title("플러피 버드")
    turtle.speed(0)
    turtle.delay(0)
    turtle.hideturtle()
    turtle.bgcolor("lightblue")
    turtle.penup()
    turtle.onkeypress(gameStart, "Return")
    turtle.listen()
 
def gameStart():
    global isStarting
    global player
    player = PlayerManager()
    isStarting = True

def spawnCloud():
    global cloudTimer
    cloudTimer += timeutil.deltaTime()
    print(timeutil.deltaTime())
    if cloudTimer >= CLOUD_SPAWN_TIME:
        cloudList.append(Cloud())
        cloudTimer = 0
 
def gameLoop():
    global isPlaying
    global player
    isPlaying = True
    while isPlaying:
        mainUpdate()
        render()
        destroy()
        time.sleep(0.015)
        timeutil.update()
 
def mainUpdate():
    spawnCloud()
    if player != None:
        player.update()
 
def render():
    turtle.clear()
    if not isStarting:
        message("플러피 버드", "[엔터]로 게임 시작.", "gray")
    for cloud in cloudList:
        turtle.fillcolor("white")
        turtle.setposition(cloud.x - 7, cloud.y)
        turtle.begin_fill()
        turtle.circle(12)
        turtle.end_fill()
        turtle.setposition(cloud.x + 7, cloud.y)
        turtle.begin_fill()
        turtle.circle(12)
        turtle.end_fill()
        if cloud.x < -WIDTH / 2 - 100:
            destroyCloud.append(cloud)

def destroy():
    pass
 
if __name__ == "__main__":
    #threading.Thread(target=gameLoop).start()
    main_screen()
    gameLoop()
    turtle.mainloop()
