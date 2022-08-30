import TimeManager
import turtle
import random
 
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

cloudTimer = 4
CLOUD_SPAWN_TIME = 6

pipeTimer = 0
DEFAULT_PIPE_SPAWN_TIME = 3

DEFAULT_PIPE_SPEED = 80

PIPE_RECT_WIDTH = 30

JUMP_FORCE = 200

GRAVITY = 130

MAX_LIFE = 3 #MAX_LIFE + 1 = 목숨

playTimer = 0

textTurtle = turtle.Turtle()
cloudTurtle = turtle.Turtle()
pipeTurtle = turtle.Turtle()

beforePipeAir = random.randrange(-HEIGHT / 2, HEIGHT / 2)


def init():
    global isStarting, beforePipeAir, timeutil, player, playTimer, cloudTimer, pipeTimer
    isStarting = False
    cloudList.clear()
    pipeList.clear()

    destroyCloud.clear()
    destroyPipe.clear()

    if timeutil == None:
        timeutil = TimeManager.TimeManager()
    
    if player != None:
        player.destroy()
        player = None

    playTimer = 0
    cloudTimer = 4
    pipeTimer = 0

    beforePipeAir = random.randrange(-HEIGHT / 2, HEIGHT / 2)

class GameObject:
    def update(self):
        pass
 
class PlayerManager(GameObject):
    def __init__(self):
        self.__gameObject = turtle.Turtle()
        self.__gameObject.shape("turtle")
        self.__gameObject.shapesize(1.4)
        self.__life = MAX_LIFE
        init_turtle(self.__gameObject)
        self.__gameObject.showturtle()
        turtle.onkeypress(self.jump, "space")
        turtle.onkeypress(self.jump, "Up")

        self.__jumped = False
        self.__jumpTimer = 0
        
    def update(self):
        me = self.__gameObject
        pos = [me.xcor(), me.ycor()]

        if(self.__jumped):
            self.__jumpTimer += timeutil.deltaTime()
            if self.__jumpTimer > 0.2:
                self.__jumped = False
                self.__jumpTimer = 0
            pos[1] += JUMP_FORCE * timeutil.deltaTime()
        else:
            pos[1] -= GRAVITY * timeutil.deltaTime()
        
        pos[1] = clamp(pos[1], -HEIGHT / 2 + 30, HEIGHT / 2 - 30)

        me.setpos(pos[0], pos[1])
        
    def jump(self):
        self.__jumped = True
        self.__jumpTimer = 0
    
    def destroy(self):
        self.__gameObject.hideturtle()

    def damaged(self):
        self.__life -= 1
    
    def isDie(self):
        return self.__life < 0

    def getX(self):
        return self.__gameObject.xcor()
    
    def getY(self):
        return self.__gameObject.ycor()

class Cloud(GameObject):
    def __init__(self):
        self.x = WIDTH/2
        self.y = random.randrange(-HEIGHT/4, HEIGHT/4)
        self.__CLOUD_SPEED = random.randrange(20, 37) * speedRate
        self.__size = random.randrange(15, 23)
    
    def update(self):
        self.x -= self.__CLOUD_SPEED * timeutil.deltaTime()
    
    def size(self):
        return self.__size
        

class PipeObject(GameObject):
    def __init__(self):
        global beforePipeAir
        self.__size = random.randrange(50, 100)
        self.__pipeAir = clamp(beforePipeAir + random.randrange(-120, 120), -HEIGHT / 2 + self.__size, HEIGHT / 2 - self.__size)
        self.x = WIDTH / 2
        beforePipeAir = self.__pipeAir

    def update(self):
        self.x -= DEFAULT_PIPE_SPEED * speedRate * timeutil.deltaTime()

    def getPipeAir(self):
        return self.__pipeAir

    def getSize(self):
        return self.__size

def clamp(v, min, max):
    if min > max:
        temp = min
        min = max
        max = temp
    
    if v > max: return max
    elif v < min: return min
    return v

def within(v, min, max):
    if min > max:
        temp = min
        min = max
        max = temp
    
    return v >= min and v <= max

def message(m1, m2, color="black"):
    textTurtle.pencolor(color)
    textTurtle.setposition(0, 100)
    textTurtle.write(m1, False, "center", ("", 20))
    textTurtle.setposition(0, -100)
    textTurtle.write(m2, False, "center", ("", 15))
    textTurtle.setpos(0, 100)
 
def main_screen():
    turtle.setup(WIDTH, HEIGHT)
    turtle.title("플러피 버드")
    turtle.bgcolor("lightblue")

    #게임 시작 키보드 입력(Enter)
    turtle.onkeypress(gameStart, "Return")
    turtle.listen()

    #터틀 딜레이 제거
    turtle.delay(0)

    #터틀 업데이트 비활성화(화면 깜빡임 방지)
    turtle.tracer(0, 0)

    #터틀 초기화
    init_turtle(turtle)
    init_turtle(textTurtle)
    init_turtle(cloudTurtle)
    init_turtle(pipeTurtle)

    #게임 메인 화면 텍스트
    message("플러피 버드", "[엔터]로 게임 시작.", "gray")

    
def init_turtle(t):
    t.speed(0)
    t.hideturtle()
    t.penup()
 
def gameStart():
    global isStarting
    if isStarting: return
    global player
    player = PlayerManager()
    isStarting = True
    playTimer = 0
    textTurtle.clear()

def spawnCloud():
    global cloudTimer
    cloudTimer += timeutil.deltaTime()
    if cloudTimer >= CLOUD_SPAWN_TIME:
        cloudList.append(Cloud())
        cloudTimer = 0

def spawnPipe():
    global pipeTimer
    pipeTimer += timeutil.deltaTime()
    if pipeTimer >= DEFAULT_PIPE_SPAWN_TIME / speedRate:
        pipeList.append(PipeObject())
        pipeTimer = 0

def speedRateChange():
    global playTimer, speedRate
    playTimer += timeutil.deltaTime()

    if playTimer >= 120 and speedRate < 5: speedRate = 5
    elif playTimer >= 90 and speedRate < 3: speedRate = 3
    elif playTimer >= 60 and speedRate < 2: speedRate = 2
    elif playTimer >= 40 and speedRate < 1.8: speedRate = 1.8
    elif playTimer >= 30 and speedRate < 1.4: speedRate = 1.4
    elif playTimer >= 15 and speedRate < 1.2: speedRate = 1.2

def collider():
    for pip in pipeList:
        #플레이어 캐릭터의 위치가 파이프의 빈공간(Y)에 있다면
        if within(player.getY(), pip.getPipeAir() - pip.getSize(), pip.getPipeAir() + pip.getSize()):
            #파이프 다음 확인
            continue
        #플레이어 캐릭터의 위치가 파이프의 x축 범위 내에 있지 않다면
        if not within(player.getX(), pip.x - PIPE_RECT_WIDTH, pip.x + PIPE_RECT_WIDTH):
            #파이프 다음 확인
            continue

        #충돌
        player.damaged()
        destroyPipe.append(pip)

        #플레이어가 죽었다면
        if player.isDie():
            message("사망하셨습니다.", "버틴시간: {:.2f}s".format(playTimer))
            init()
 
def gameLoop():
    global isPlaying
    global player
    isPlaying = True
    while isPlaying:
        mainUpdate() #update 실행
        render() #프레임 그리기
        collider() #플레이어 파이프 충돌 체크
        destroy() #오브젝트 삭제
        timeutil.update() #deltaTime 새로 고침
 
def mainUpdate():
    speedRateChange() #난이도 상승
    spawnCloud()
    if isStarting: spawnPipe()
    if player != None:
        player.update()
    for cloud in cloudList:
        cloud.update()
    for pip in pipeList:
        pip.update()
 
def render():
    cloudTurtle.clear()
    pipeTurtle.clear()

    for cloud in cloudList:
        cloudTurtle.fillcolor("white")
        cloudTurtle.setposition(cloud.x - cloud.size() / 2, cloud.y)
        cloudTurtle.begin_fill()
        cloudTurtle.circle(cloud.size() * 0.8)
        cloudTurtle.end_fill()
        cloudTurtle.setposition(cloud.x + cloud.size() / 2, cloud.y)
        cloudTurtle.begin_fill()
        cloudTurtle.circle(cloud.size())
        cloudTurtle.end_fill()
        if cloud.x < -WIDTH / 2 - cloud.size() / 2:
            destroyCloud.append(cloud)

    for pip in pipeList:
        pipeTurtle.fillcolor("green")
        pipeTurtle.setpos(pip.x - PIPE_RECT_WIDTH, HEIGHT / 2)
        pipeTurtle.begin_fill()
        pipeTurtle.setpos(pip.x - PIPE_RECT_WIDTH, pip.getPipeAir() + pip.getSize())
        pipeTurtle.setpos(pip.x + PIPE_RECT_WIDTH, pip.getPipeAir() + pip.getSize())
        pipeTurtle.setpos(pip.x + PIPE_RECT_WIDTH, HEIGHT / 2)
        pipeTurtle.end_fill()

        pipeTurtle.setpos(pip.x - PIPE_RECT_WIDTH, -HEIGHT / 2)
        pipeTurtle.begin_fill()
        pipeTurtle.setpos(pip.x - PIPE_RECT_WIDTH, pip.getPipeAir() - pip.getSize())
        pipeTurtle.setpos(pip.x + PIPE_RECT_WIDTH, pip.getPipeAir() - pip.getSize())
        pipeTurtle.setpos(pip.x + PIPE_RECT_WIDTH, -HEIGHT / 2)
        pipeTurtle.end_fill()

        if pip.x < -WIDTH / 2 - 10:
            destroyPipe.append(pip)
    
    turtle.Screen().update()

def destroy():
    for cloud in destroyCloud:
        cloudList.remove(cloud)
    for pip in destroyPipe:
        pipeList.remove(pip)

    destroyCloud.clear()
    destroyPipe.clear()
 
if __name__ == "__main__":
    #threading.Thread(target=gameLoop).start()
    init()
    main_screen()
    gameLoop()
    turtle.mainloop()
