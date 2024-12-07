import random
import pygame

# 初始化pyGame对象

pygame.init()
# 创建surface窗口对象
win = pygame.display.set_mode((800, 600))
# 设置窗口的标题
pygame.display.set_caption("Zombie warning")
# 创建一个背景图片和标题文字
bg = pygame.image.load("img/background.png")
titlePicture = pygame.image.load('img/titlePicture.png')
overPicture = pygame.image.load('img/overPicture.png')
introPicture = pygame.image.load('img/introPicture.png')
# 设置屏幕刷新率
clock = pygame.time.Clock()
# 设置子弹音效，击打音效和背景音乐
bulletSound = pygame.mixer.Sound('music/bullet.mp3')
hitSound = pygame.mixer.Sound('music/hit.mp3')
pygame.mixer.music.load('music/Blue Space.mp3')
pygame.mixer.music.play(-1)
# 设置各个按钮和标题
playButton = pygame.image.load('buttons/playButton.png')
howToPlayButton = pygame.image.load('buttons/howToPlayButton.png')
exitButton = pygame.image.load('buttons/exitButton.png')
scoreButton = pygame.image.load('buttons/scoreButton.png')
startButton = pygame.image.load('buttons/startButton.png')
retryButton = pygame.image.load('buttons/retryButton.png')
# 设置fps
fps = 60
# 调试用：设置判定框是否可见
hitBoxVisible = False


# 角色类
class Player(object):
    def __init__(self, x, y):
        # 设置人物初始坐标为400,300
        self.x, self.y = x, y
        # 设置人物一次移动的距离
        self.vel = 2.5
        # 人物的宽度和高度
        self.width, self.height = 24, 24
        # 四个方向走动的图片列表
        self.walkLeft = []
        self.walkRight = []
        self.walkUp = []
        self.walkDown = []
        # 记录子弹发射间隔
        self.bulletSpeed = 16
        # 记录子弹数量
        self.count = 0
        # 记录闯到的怪物的波数
        self.monsWave = 0
        # 记录每波怪物的数量，初始为0
        self.mon1Num = 1
        self.mon2Num = 0

        # 读取向左走的图片
        for i in range(1, 4):
            name = "Player/pL%d.png" % i
            self.walkLeft.append(pygame.image.load(name))

        # 读取向右走的图片
        for i in range(1, 4):
            name = "Player/pR%d.png" % i
            self.walkRight.append(pygame.image.load(name))

        # 读取向上走的图片
        for i in range(1, 4):
            name = "Player/pU%d.png" % i
            self.walkUp.append(pygame.image.load(name))

        # 读取向下走的图片
        for i in range(1, 4):
            name = "Player/pD%d.png" % i
            self.walkDown.append(pygame.image.load(name))
        # 记录走到第几步
        self.walkCount = 0
        # 记录上下左右走和站着不动
        self.left = False
        self.right = False
        self.up = False
        self.down = False
        self.standing = True
        # 创建一个人物surface对象
        self.char = pygame.image.load("Player/pStanding.png")
        # 创建一个子弹组
        self.bullets = []
        # 碰撞检测区(左上角x，左上角y，宽度，高度）
        self.hitBox = (self.x, self.y, 24, 24)
        # 得分
        self.score = 0
        # 最高分
        self.highestScore = getHScore()
        # 使游戏暂停设置为False
        self.gamePause = False

    def control(self, K_a, K_d, K_w, K_s,
                K_LEFT, K_RIGHT, K_UP, K_DOWN):
        # 获取键盘上所有按键的状态 是否被按下
        keys = pygame.key.get_pressed()
        # A键按下
        self.standing = True
        if keys[K_a] and self.x > self.vel:
            self.left, self.right, self.up, self.down = True, False, False, False
            self.standing = False
            self.x -= self.vel
        # D键按下
        if keys[K_d] and self.x < 800 - self.width - self.vel:
            self.left, self.right, self.up, self.down = False, True, False, False
            self.standing = False
            self.x += self.vel
        # W键按下
        if keys[K_w] and self.y > self.vel:
            self.left, self.right, self.up, self.down = False, False, True, False
            self.standing = False
            self.y -= self.vel
        # S键按下
        if keys[K_s] and self.y < 600 - self.width - self.vel:
            self.left, self.right, self.up, self.down = False, False, False, True
            self.standing = False
            self.y += self.vel
        # 子弹左键按下
        if keys[K_LEFT]:
            self.left = True
            self.right = False
            self.up = False
            self.down = False
            self.standing = False
            facingX = -1
            facingY = 0
            if len(self.bullets) < 1000:
                self.count = (self.count + 1) % 1000
                if self.count % self.bulletSpeed == 0:
                    self.bullets.append(
                        projectile(round(self.x + self.width // 2),
                                   round(self.y + self.height // 2),
                                   facingX, facingY)
                    )
                    bulletSound.play()
        # 子弹右键按下
        elif keys[K_RIGHT]:
            self.left = False
            self.right = True
            self.up = False
            self.down = False
            self.standing = False
            facingX = 1
            facingY = 0
            if len(self.bullets) < 1000:
                self.count = (self.count + 1) % 1000
                if self.count % self.bulletSpeed == 0:
                    self.bullets.append(
                        projectile(round(self.x + self.width // 2),
                                   round(self.y + self.height // 2),
                                   facingX, facingY)
                    )
                    bulletSound.play()
        # 子弹上键按下
        elif keys[K_UP]:
            self.left = False
            self.right = False
            self.up = True
            self.down = False
            self.standing = False
            facingX = 0
            facingY = -1
            if len(self.bullets) < 1000:
                self.count = (self.count + 1) % 1000
                if self.count % self.bulletSpeed == 0:
                    self.bullets.append(
                        projectile(round(self.x + self.width // 2),
                                   round(self.y + self.height // 2),
                                   facingX, facingY)
                    )
                    bulletSound.play()
        # 子弹下键按下
        elif keys[K_DOWN]:
            self.left = False
            self.right = False
            self.up = False
            self.down = True
            self.standing = False
            facingX = 0
            facingY = 1
            if len(self.bullets) < 1000:
                self.count = (self.count + 1) % 1000
                if self.count % self.bulletSpeed == 0:
                    self.bullets.append(
                        projectile(round(self.x + self.width // 2),
                                   round(self.y + self.height // 2),
                                   facingX, facingY)
                    )
                    bulletSound.play()

    def draw(self, win):
        if self.walkCount + 1 >= 12:
            self.walkCount = 0
        # 判断如果在移动中
        if not self.standing:
            self.walkCount += 1
            if self.left:
                win.blit(self.walkLeft[self.walkCount // 4], (self.x, self.y))
            if self.right:
                win.blit(self.walkRight[self.walkCount // 4], (self.x, self.y))
            if self.up:
                win.blit(self.walkUp[self.walkCount // 4], (self.x, self.y))
            if self.down:
                win.blit(self.walkDown[self.walkCount // 4], (self.x, self.y))
        # 判断如果在站立中
        else:
            if self.right:
                win.blit(self.walkRight[0], (self.x, self.y))
            elif self.left:
                win.blit(self.walkLeft[0], (self.x, self.y))
            elif self.up:
                win.blit(self.walkUp[0], (self.x, self.y))
            elif self.down:
                win.blit(self.walkDown[0], (self.x, self.y))
            else:
                win.blit(self.char, (self.x, self.y))

        for mon in mons:
            for bullet in self.bullets:
                # 判断如果子弹在怪物判定框内
                if bullet.x + 2 > mon.hitBox[0] and bullet.x < mon.hitBox[0] + mon.hitBox[2]:
                    if bullet.y + 2 > mon.hitBox[1] and bullet.y < mon.hitBox[1] + mon.hitBox[3]:
                        if mon.alive:
                            self.score += mon.hit() * 10
                            self.bullets.pop(self.bullets.index(bullet))
                        else:
                            del mon
        for bullet in self.bullets:
            if 0 < bullet.x < 800 and 0 < bullet.y < 600:
                bullet.x += bullet.velX
                bullet.y += bullet.velY
                bullet.draw(win)
            else:
                self.bullets.pop(self.bullets.index(bullet))

        self.hitBox = (self.x, self.y, 24, 24)
        if hitBoxVisible:
            pygame.draw.rect(win, (255, 0, 0), self.hitBox, 2)

    def hit(self):

        self.gamePause = True


# 子弹类
class projectile(object):
    def __init__(self, x, y, facingX, facingY):
        self.x = x
        self.y = y
        """
        # 设置半径
        self.radius = 3
        # 设置颜色
        self.color = (193, 210, 240)
        """
        # 设置朝向
        self.facingX = facingX
        self.facingY = facingY
        # 子弹移动的速度
        self.velX = facingX * 3
        self.velY = facingY * 3

    def draw(self, win):
        self.bullet = pygame.image.load("img/bullet.png")
        win.blit(self.bullet, (self.x, self.y))
        """ 
        pygame.draw.circle(win, self.color,
                           (self.x, self.y),
                           self.radius)
        """


# 敌人类1
class Monster1(object):
    def __init__(self, number, x, y):
        # 设置怪物的编号
        self.number = number
        # 设置怪物是否存活
        self.alive = True
        # 设置怪物的位置
        self.x = x
        self.y = y
        # 设置怪物的移动速度
        self.vel = 1.5
        # 设置怪物的宽度和高度
        self.width, self.height = 32, 48
        # 设置怪物的行动方式
        self.moveWay = random.randint(1, 2)
        # 设置决定怪物行动方式的距离判断，每行动50个像素随机变更一次
        self.moveWayKey = 0
        # 四个方向走的图片列表
        self.walkLeft = []
        self.walkRight = []
        self.walkUp = []
        self.walkDown = []
        # 读取向左走的图片
        for i in range(1, 4):
            name = "Monster/Zombie1/z1L%d.png" % i
            self.walkLeft.append(pygame.image.load(name))
        # 读取向右走的图片
        for i in range(1, 4):
            name = "Monster/Zombie1/z1R%d.png" % i
            self.walkRight.append(pygame.image.load(name))
        # 读取向上走的图片
        for i in range(1, 4):
            name = "Monster/Zombie1/z1U%d.png" % i
            self.walkUp.append(pygame.image.load(name))
        # 读取向下走的图片
        for i in range(1, 4):
            name = "Monster/Zombie1/z1D%d.png" % i
            self.walkDown.append(pygame.image.load(name))

        # 记录走到第几步
        self.walkCount = 0
        # 记录上下左右走和站着不动
        self.left = False
        self.right = False
        self.up = False
        self.down = False
        self.hitBox = (self.x, self.y + 20, 32, 48)
        # 血量
        self.health = 3

    def move1(self):
        # 设置个缓冲以防卡在原地
        if self.x - 16 > man.x - man.width and abs(self.x - man.x) > 8:
            self.left, self.right, self.up, self.down = True, False, False, False
            self.x -= self.vel
            self.moveWayKey += 1
        elif self.x - 16 < man.x - man.width and abs(self.x - man.x) > 8:
            self.left, self.right, self.up, self.down = False, True, False, False
            self.x += self.vel
            self.moveWayKey += 1
        elif self.y + 32 > man.y:
            self.left, self.right, self.up, self.down = False, False, True, False
            self.y -= self.vel
            self.moveWayKey += 1
        elif self.y + 32 < man.y:
            self.left, self.right, self.up, self.down = False, False, False, True
            self.y += self.vel
            self.moveWayKey += 1

    def move2(self):
        # 设置个缓冲以防卡在原地
        if self.y + 32 > man.y and abs(self.y + 32 - man.y) > 1:
            self.left, self.right, self.up, self.down = False, False, True, False
            self.y -= self.vel
            self.moveWayKey += 1
        elif self.y + 32 < man.y and abs(self.y + 32 - man.y) > 1:
            self.left, self.right, self.up, self.down = False, False, False, True
            self.y += self.vel
            self.moveWayKey += 1
        elif self.x - 16 > man.x - man.width:
            self.left, self.right, self.up, self.down = True, False, False, False
            self.x -= self.vel
            self.moveWayKey += 1
        elif self.x - 16 < man.x - man.width:
            self.left, self.right, self.up, self.down = False, True, False, False
            self.x += self.vel
            self.moveWayKey += 1

        # print('玩家的y坐标：', man.y, '怪物的y坐标：', self.y)

    def draw(self, win):
        # 每行动50格，随即便换一次行动方式
        if self.moveWayKey % 50 == 0:
            self.moveWay = random.randint(1, 2)
        if self.moveWay == 1:
            self.move1()
        else:
            self.move2()
        if self.walkCount + 1 >= 12:
            self.walkCount = 0
        self.walkCount += 1
        if self.left:
            win.blit(self.walkLeft[self.walkCount // 6], (self.x, self.y))
        elif self.right:
            win.blit(self.walkRight[self.walkCount // 6], (self.x, self.y))
        elif self.up:
            win.blit(self.walkUp[self.walkCount // 6], (self.x, self.y))
        elif self.down:
            win.blit(self.walkDown[self.walkCount // 6], (self.x, self.y))
        if hitBoxVisible:
            pygame.draw.rect(win, (255, 0, 0), self.hitBox, 2)
        # 设置怪物的判定区
        self.hitBox = (self.x, self.y + 20, 32, 48)
        # 设置怪物的血条（长度36，一次减少12，宽度为4
        self.bloodBox = [self.hitBox[0], self.hitBox[1] - 5, 36, 4]
        pygame.draw.rect(win, (255, 0, 0), self.bloodBox)
        self.bloodBox[2] = 36 - (12 * (3 - self.health))
        pygame.draw.rect(win, (0, 128, 0), self.bloodBox)
        # 判断怪物中心追上人的判定框
        if abs(self.hitBox[0] - man.hitBox[0]) < man.hitBox[2] / 2 and \
                abs(self.hitBox[1] - man.hitBox[1]) < man.hitBox[3]:
            man.hit()

    def hit(self):
        score = 0
        hitSound.play()
        if self.health > 1:
            self.health -= 1
        else:
            score = 1
            self.alive = False
            mons.remove(self)
        return score


# 敌人类2
class Monster2(object):
    def __init__(self, number, x, y):
        # 设置怪物的编号
        self.number = number
        # 设置怪物是否存活
        self.alive = True
        # 设置怪物的位置
        self.x = x
        self.y = y
        # 设置怪物的移动速度
        self.vel = 3
        # 设置怪物的宽度和高度
        self.width, self.height = 32, 48
        # 设置怪物的行动方式
        self.moveWay = random.randint(1, 2)
        # 设置决定怪物行动方式的距离判断，每行动50个像素随机变更一次
        self.moveWayKey = 0
        # 四个方向走的图片列表
        self.walkLeft = []
        self.walkRight = []
        self.walkUp = []
        self.walkDown = []
        # 读取向左走的图片
        for i in range(1, 4):
            name = "Monster/Zombie2/z2L%d.png" % i
            self.walkLeft.append(pygame.image.load(name))
        # 读取向右走的图片
        for i in range(1, 4):
            name = "Monster/Zombie2/z2R%d.png" % i
            self.walkRight.append(pygame.image.load(name))
        # 读取向上走的图片
        for i in range(1, 4):
            name = "Monster/Zombie2/z2U%d.png" % i
            self.walkUp.append(pygame.image.load(name))
        # 读取向下走的图片
        for i in range(1, 4):
            name = "Monster/Zombie2/z2D%d.png" % i
            self.walkDown.append(pygame.image.load(name))

        # 记录走到第几步
        self.walkCount = 0
        # 记录上下左右走和站着不动
        self.left = False
        self.right = False
        self.up = False
        self.down = False
        self.hitBox = (self.x, self.y + 20, 32, 48)
        # 血量
        self.health = 2

    def move1(self):
        # 设置个缓冲以防卡在原地
        if self.x - 16 > man.x - man.width and abs(self.x - man.x) > 8:
            self.left, self.right, self.up, self.down = True, False, False, False
            self.x -= self.vel
        elif self.x - 16 < man.x - man.width and abs(self.x - man.x) > 8:
            self.left, self.right, self.up, self.down = False, True, False, False
            self.x += self.vel
        elif self.y + 32 > man.y:
            self.left, self.right, self.up, self.down = False, False, True, False
            self.y -= self.vel
        elif self.y + 32 < man.y:
            self.left, self.right, self.up, self.down = False, False, False, True
            self.y += self.vel

    def move2(self):
        # 设置个缓冲以防卡在原地
        if self.y + 32 > man.y and abs(self.y + 32 - man.y) > 1.5:
            self.left, self.right, self.up, self.down = False, False, True, False
            self.y -= self.vel
        elif self.y + 32 < man.y and abs(self.y + 32 - man.y) > 1.5:
            self.left, self.right, self.up, self.down = False, False, False, True
            self.y += self.vel
        elif self.x - 16 > man.x - man.width:
            self.left, self.right, self.up, self.down = True, False, False, False
            self.x -= self.vel
        elif self.x - 16 < man.x - man.width:
            self.left, self.right, self.up, self.down = False, True, False, False
            self.x += self.vel

        # print('玩家的y坐标：', man.y, '怪物的y坐标：', self.y)

    def draw(self, win):
        # 每行动50格，随即便换一次行动方式
        if self.moveWayKey % 50 == 0:
            self.moveWay = random.randint(1, 2)
        if self.moveWay == 1:
            self.move1()
        else:
            self.move2()
        if self.walkCount + 1 >= 12:
            self.walkCount = 0
        self.walkCount += 1
        if self.left:
            win.blit(self.walkLeft[self.walkCount // 6], (self.x, self.y))
        elif self.right:
            win.blit(self.walkRight[self.walkCount // 6], (self.x, self.y))
        elif self.up:
            win.blit(self.walkUp[self.walkCount // 6], (self.x, self.y))
        elif self.down:
            win.blit(self.walkDown[self.walkCount // 6], (self.x, self.y))
        if hitBoxVisible:
            pygame.draw.rect(win, (255, 0, 0), self.hitBox, 2)
        # 设置怪物的判定区
        self.hitBox = (self.x, self.y + 20, 32, 48)
        # 设置怪物的血条（长度36，一次减少12，宽度为4
        self.bloodBox = [self.hitBox[0], self.hitBox[1] - 5, 36, 4]
        pygame.draw.rect(win, (255, 0, 0), self.bloodBox)
        self.bloodBox[2] = 36 - (18 * (2 - self.health))
        pygame.draw.rect(win, (0, 128, 0), self.bloodBox)
        # 判断怪物中心追上人的判定框
        if abs(self.hitBox[0] - man.hitBox[0]) < man.hitBox[2] / 2 and \
                abs(self.hitBox[1] - man.hitBox[1]) < man.hitBox[3]:
            man.hit()

    def hit(self):
        score = 0
        hitSound.play()
        if self.health > 1:
            self.health -= 1
        else:
            score = 2
            self.alive = False
            mons.remove(self)
        return score

# 通过文件读写来读取和写入最大得分
def getHScore():
    f = open('highestScore.txt')
    s = f.readline()
    return int(s)

def setHScore(score):
    f = open('highestScore.txt', 'w')
    f.write(str(score))
    return True

def redrawWin(man, win):
    # 将背景图从0，0位置画在窗口上
    score = 0
    win.blit(bg, (0, 0))
    man.draw(win)
    score += man.score
    for mon in mons:
        if mon.alive:
            mon.draw(win)
    font1 = pygame.font.SysFont("宋体", 30, True)
    text0 = font1.render('Highest Score:%d' % man.highestScore, 1, (200, 246, 143))
    text1 = font1.render('Score:%d' % score, 1, (255, 246, 143))
    font2 = pygame.font.SysFont("宋体", 20, True)
    text2 = font2.render("Wave: %d" % man.monsWave, 1, (255, 246, 143))
    text3 = font2.render("Zombies Left: %d" % len(mons), 1, (255, 246, 143))
    text4 = font2.render("Gun Speed Level: %d" % (17 - man.bulletSpeed), 1, (255, 246, 143))
    win.blit(text0, (300, 10))
    win.blit(text1, (360, 30))
    win.blit(text2, (10, 10))
    win.blit(text3, (10, 26))
    win.blit(text4, (10, 42))
    # 每5波怪物2数量加一，否则每波怪物1数量加二
    if len(mons) == 0:
        man.monsWave += 1
        if man.monsWave % 5 == 0:
            man.mon2Num += 1
        elif man.monsWave % 2 == 0:
            man.mon1Num += 1
        else:
            pass
        # 无尽模式
        Wave(man.mon1Num, man.mon2Num)
        # 每10波升级一次子弹速度，满速为5级
        if man.monsWave % 10 == 0 and man.bulletSpeed > 12:
            man.bulletSpeed -= 1
    # 屏幕刷新
    pygame.display.update()


# 怪物1和2的数量，生成怪物
def Wave(monsNum1, monsNum2):
    for i in range(monsNum1):
        monsCreateKey = random.randint(1, 4)
        # 从左边生成
        if monsCreateKey == 1:
            monsCreateX = -100
            monsCreateY = random.randint(200, 400)
        # 从右边生成
        if monsCreateKey == 2:
            monsCreateX = 800
            monsCreateY = random.randint(200, 400)
        # 从上边生成
        if monsCreateKey == 3:
            monsCreateX = random.randint(300, 500)
            monsCreateY = -100
        # 从下边生成
        if monsCreateKey == 4:
            monsCreateX = random.randint(300, 500)
            monsCreateY = 600
        mon = Monster1(i, monsCreateX, monsCreateY)
        mons.append(mon)
    for i in range(monsNum2):
        monsCreateKey = random.randint(1, 4)
        # 从左边生成
        if monsCreateKey == 1:
            monsCreateX = -100
            monsCreateY = random.randint(200, 400)
        # 从右边生成
        if monsCreateKey == 2:
            monsCreateX = 800
            monsCreateY = random.randint(200, 400)
        # 从上边生成
        if monsCreateKey == 3:
            monsCreateX = random.randint(300, 500)
            monsCreateY = -100
        # 从下边生成
        if monsCreateKey == 4:
            monsCreateX = random.randint(300, 500)
            monsCreateY = 600
        mon = Monster2(i, monsCreateX, monsCreateY)
        mons.append(mon)


# 创建玩家对象
man = Player(400, 300)
# 创建怪物表
mons = []
# 使游戏持续运行
run = True
# 使封面持续运行
runFirstPage = True
runIntroPage = False

while runFirstPage:
    # 设置屏幕刷新率
    clock.tick(fps)
    buttons = pygame.mouse.get_pressed()
    x1, y1 = pygame.mouse.get_pos()

    # 显示背景和各种窗口
    win.blit(bg, (0, 0))
    # 宽为屏幕宽800/2-图片宽/2
    win.blit(titlePicture, (80, 120))
    win.blit(playButton, (358, 329))
    win.blit(howToPlayButton, (300, 389))
    win.blit(exitButton, (366.5, 454))

    # (x, y, width, height)
    # buttonBox = (366.5, 454, 67, 61)
    # pygame.draw.rect(win, (255, 0, 0), buttonBox, 2)

    if 358 <= x1 <= 440 and 329 <= y1 <= 391:
        win.blit(playButton, (358 + 1, 329 + 1))
        win.blit(playButton, (358 + 2, 329 + 2))
        if buttons[0]:
            runFirstPage = False
    if 300 <= x1 <= 513 and 389 <= y1 <= 450:
        win.blit(howToPlayButton, (300 + 1, 389 + 1))
        win.blit(howToPlayButton, (300 + 2, 389 + 2))
        if buttons[0]:
            runFirstPage = False
            # 使介绍页持续运行
            runIntroPage = True
    if 366.5 <= x1 <= 433.5 and 454 <= y1 <= 515:
        win.blit(exitButton, (366.5 + 1, 454 + 1))
        win.blit(exitButton, (366.5 + 2, 454 + 2))
        if buttons[0]:
            pygame.quit()
            quit()

    for event in pygame.event.get():  # 判断窗口事件
        if event.type == pygame.QUIT:  # 判断用户是否退出
            pygame.quit()
            quit()
    pygame.display.update()

while runIntroPage:

    # 显示背景和各种窗口
    win.blit(bg, (0, 0))
    win.blit(introPicture, ((800 - introPicture.get_width())/2, 20))
    win.blit(startButton, (360.5, 530))  # 79*54
    buttons2 = pygame.mouse.get_pressed()
    x12, y12 = pygame.mouse.get_pos()
    if 360.5 <= x12 <= 439.5 and 530 <= y12 <= 584:
        win.blit(startButton, (360.5 + 1, 530 + 1))
        win.blit(startButton, (360.5 + 2, 530 + 2))
        if buttons2[0]:
            runIntroPage = False
    for event in pygame.event.get():  # 判断窗口事件
        if event.type == pygame.QUIT:  # 判断用户是否退出
            pygame.quit()
            quit()
    pygame.display.update()

# 游戏主循环
while run:
    # 设置屏幕刷新率
    clock.tick(fps)
    for event in pygame.event.get():  # 判断窗口事件
        if event.type == pygame.QUIT:  # 判断用户是否退出
            run = False  # 将run设置False 退出循环

    # 设置玩家1和玩家2的游戏按键4
    man.control(pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s,
                pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN)

    redrawWin(man, win)

    while man.gamePause:
        for event in pygame.event.get():  # 判断窗口事件
            if event.type == pygame.QUIT:  # 判断用户是否退出
                pygame.quit()  # 退出游戏
                quit()# 设置游戏结束
        # 宽为屏幕宽800/2-图片宽/2
        win.blit(bg, (0, 0))

        fontScore = pygame.font.SysFont("仿宋", 30, True)
        textScore = fontScore.render('%d' % man.score, 1, (188, 2, 0))

        savedScore = pygame.font.SysFont("仿宋", 24, True)
        savedText = savedScore.render('Successfully saved... ', 1, (188, 2, 0))
        win.blit(overPicture, (400-overPicture.get_width()/2, 200))
        win.blit(scoreButton, (351.5, 300))
        win.blit(textScore, (400-textScore.get_width()/2, 360))

        if man.score > man.highestScore:
            if setHScore(man.score):
                win.blit(savedText, (800-savedText.get_width(), 600-savedText.get_height()))
        win.blit(retryButton, (353, 400))
        buttons1 = pygame.mouse.get_pressed()
        x11, y11 = pygame.mouse.get_pos()
        if 353 <= x11 <= 447 and 400 <= y11 <= 465:
            win.blit(retryButton, (353 + 1, 400 + 1))
            win.blit(retryButton, (353 + 2, 400 + 2))
            if buttons1[0]:
                man.gamePause = False
                del man
                del mons
                man = Player(400, 300)
                mons = []
        pygame.display.update()

# 退出游戏
pygame.quit()
quit()
