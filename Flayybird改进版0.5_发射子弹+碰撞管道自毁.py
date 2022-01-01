import sys  # 导入sys模块
import pygame  # 导入pygame模块
import random
import time
import os

path='E:\Python文件\GAME'
os.chdir(path)

class Bird(object):
    """定义一个鸟类"""
    def __init__(self):
        """定义初始化方法"""
        self.birdRect = pygame.Rect(65,50,50,50)  #鸟的矩形
        #定义鸟的三种状态列表
        self.birdStatus = [pygame.image.load("assets/1.png"),
                           pygame.image.load("assets/2.png"),
                           pygame.image.load("assets/dead.png")]
        self.status = 0      # 默认飞行状态
        self.birdX = 120     # 鸟所在X轴坐标,即是向右飞行的速度
        self.birdY = 350     # 鸟所在Y轴坐标,即上下飞行高度
        self.dead = False    # 默认小鸟生命状态为活着
        self.birdRect[0]=self.birdX                         
        self.birdRect[1]=self.birdY


class Bullets(object):
    def __init__(self):
        self.x=120
        self.y=350
        self.picture = pygame.image.load("assets/子弹.png")
        self.moving = False
    
    def updateBullets(self):
        self.x +=5
        if self.x > 500:
            self.moving = False
            

class Pipeline(object):
    """定义一个管道类"""
    def __init__(self):
        """定义初始化方法"""
        self.wallx = 400  # 管道所在X轴坐标
        self.pineUp = pygame.image.load("assets/top.png")
        self.pineDown = pygame.image.load("assets/bottom.png")

    def updatePipeline(self):
        """"管道移动方法"""
        self.wallx -= 5  # 管道X轴坐标递减，即管道向左移动
        # 当管道运行到一定位置，即小鸟飞越管道，分数加1，并且重置管道
        if self.wallx < -80:
            global score
            score += 1
            self.wallx = 400

class Coin(object):
    def __init__(self):
        self.x=300
        self.y=250
        self.picture = pygame.image.load("assets/0.png")
        self.dead = False

    def updatecoin_posx(self):
        self.x -=5
        if self.dead or self.x < 0:
            self.dead = False
            self.x=random.randrange(300,350,10)
            self.y=random.randrange(0,400,20)


def createMap():
    """定义创建地图的方法"""
    screen.fill((255, 255, 255))  # 填充颜色(screen还没定义不要着急)
    screen.blit(background, (0, 0))  # 填入到背景

    # 显示管道
    screen.blit(Pipeline.pineUp, (Pipeline.wallx, s1))   # 上管道坐标位置
    screen.blit(Pipeline.pineDown, (Pipeline.wallx, s2))  # 下管道坐标位置
    Pipeline.updatePipeline()  # 管道移动

    screen.blit(Coin.picture, (Coin.x, Coin.y))
    
    Coin.updatecoin_posx()    #金币移动

     # 显示小鸟
    if Bird.dead:              # 撞管道状态
        Bird.status = 2

    screen.blit(Bird.birdStatus[Bird.status], (Bird.birdX, Bird.birdY))              # 设置小鸟的坐标

    if Bullets.moving:
        screen.blit(Bullets.picture, (Bullets.x, Bullets.y))  # 子弹坐标位置
        Bullets.updateBullets()  # 子弹移动

    # 显示分数
    screen.blit(font.render('Score:' + str(score), -1, (255, 255, 255)), (100, 50))  # 设置颜色及坐标位置
    pygame.display.update()  # 更新显示


def checkDead():
    # 上方管子的矩形位置
    upRect = pygame.Rect(Pipeline.wallx, s1,
                         Pipeline.pineUp.get_width(),
                         Pipeline.pineUp.get_height())

    # 下方管子的矩形位置
    downRect = pygame.Rect(Pipeline.wallx, s2+15,
                           Pipeline.pineDown.get_width(),
                           Pipeline.pineDown.get_height())
     # 金币的矩形位置
    coinRect = pygame.Rect(Coin.x, Coin.y,
                         Coin.picture.get_width(),
                         Coin.picture.get_height())
    # 子弹的矩形位置
    bulletsRect = pygame.Rect(Bullets.x, Bullets.y,
                         Bullets.picture.get_width(),
                         Bullets.picture.get_height())
    # 检测小鸟与上下方管子是否碰撞
    if upRect.colliderect(Bird.birdRect) or downRect.colliderect(Bird.birdRect):
        Bird.dead = True
    # 检测小鸟与金币是否碰撞
    if coinRect.colliderect(Bird.birdRect):
        Coin.dead = True
        global score
        score += 1
    # 检测子弹是否与管道碰撞
    if upRect.colliderect(bulletsRect) or downRect.colliderect(bulletsRect):
        Bullets.moving = False
    # 检测小鸟是否飞出上下边界
    if not -15 < Bird.birdRect[1] < height:
        Bird.dead = True
        return True
    else:
        return False

def getResutl():
    final_text1 = "Game Over"
    final_text2 = "Your final score is:  " + str(score)
    ft1_font = pygame.font.SysFont("Arial", 70)                                      # 设置第一行文字字体
    ft1_surf = font.render(final_text1, 1, (242, 3, 36))                             # 设置第一行文字颜色
    ft2_font = pygame.font.SysFont("Arial", 50)                                      # 设置第二行文字字体
    ft2_surf = font.render(final_text2, 1, (253, 177, 6))                            # 设置第二行文字颜色
    screen.blit(ft1_surf, [screen.get_width() / 2 - ft1_surf.get_width() / 2, 100])  # 设置第一行文字显示位置
    screen.blit(ft2_surf, [screen.get_width() / 2 - ft2_surf.get_width() / 2, 200])  # 设置第二行文字显示位置
    pygame.display.flip()                                                            # 更新整个待显示的Surface对象到屏幕上

if __name__ == '__main__':
    """主程序"""
    pygame.init()                            # 初始化pygame
    pygame.font.init()                       # 初始化字体
    font = pygame.font.SysFont("Arial", 50)  # 设置字体和大小
    size = width, height = 400, 650          # 设置窗口
    screen = pygame.display.set_mode(size)   # 显示窗口
    clock = pygame.time.Clock()              # 设置时钟
    Pipeline = Pipeline()                    # 实例化管道类
    Bird = Bird()                            # 实例化鸟类
    Coin=Coin()                              # 实例化金币类
    Bullets=Bullets()                        # 实例化子弹类
    score = 0
    
    gap=200
    s1=random.randrange(-400,-200,20)
    s2=s1+Pipeline.pineDown.get_height()+gap

    coin_posx=random.randrange(300,350,10)
    coin_posy=random.randrange(0,400,20)

    background=pygame.image.load('assets/background.png')
    mouse_cursor=pygame.image.load('assets/1.png')
    #创建了一个窗口,设置分辨率,第一个元祖是分辨率,第二个是不具有特性就设置成0,第三个为色深
    screen=pygame.display.set_mode((400,650),0,32)
    #设置了一个窗口
    pygame.display.set_caption('This is a game')

    while True:
        clock.tick(60)                       # 每秒执行60次
        # 轮询事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()  
            x,y=pygame.mouse.get_pos()
            x-=mouse_cursor.get_width()/2
            y-=mouse_cursor.get_height()/2  
            if not Bird.dead:
                #计算光标的左上角位置
                screen.blit(mouse_cursor,(x,y))
                #把光标画上去
                pygame.display.update()
                Bird.birdX=x
                Bird.birdY=y
                Bird.birdRect[0]=Bird.birdX                         
                Bird.birdRect[1]=Bird.birdY
            if event.type == pygame.MOUSEBUTTONDOWN:
                Bullets.x = Bird.birdX
                Bullets.y = Bird.birdY
                Bullets.moving = True
        background = pygame.image.load("assets/background.png")  # 加载背景图片
        if Bird.dead:
            Bird.birdY +=10
            Bird.birdRect[1]=Bird.birdY
        if checkDead():                         # 检测小鸟生命状态
            getResutl()                      # 如果小鸟死亡，显示游戏总分数     
        else:
            if Pipeline.wallx < -79:
                s1=random.randrange(-400,-200,20)
                s2=s1+Pipeline.pineDown.get_height()+gap
            if Coin.dead:
                coin_posx=random.randrange(300,350,10)
                coin_posy=random.randrange(0,400,20)
            createMap()                             # 创建地图
    pygame.quit()