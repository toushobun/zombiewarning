import pygame

from entity.person import Person
from entity.bullet import Bullet
import config


class Player(Person):
    def __init__(self, x, y, speed, width, height, pic_path, pic_rate, shot_speed):
        """初始化玩家

        Args:
            x (int): 玩家的x坐标
            y (int): 玩家的y坐标
            speed (int): 玩家一次移动的距离
            width (int): 玩家的宽度
            height (int): 玩家的高度
            pic_path (string): 玩家图片路径
            pic_rate (int): 玩家图片帧率
            shot_speed (int): 玩家子弹射速、0 <= shot_speed <= 100
        """
        super().__init__(x, y, speed, width, height, pic_path, pic_rate)
        self.shot_speed = shot_speed
        # 用于记录分数
        self.score = 0
        # 用于记录子弹发射间隔
        self.shot_gap = 100 - self.shot_speed
        # 创建一个子弹组
        self.bullets = []

    def move(self, K_a, K_d, K_w, K_s):
        self.stand = True
        # 获取判定框区域
        self.hit_box = (self.x, self.y, self.width, self.height)
        # 获取键盘上所有按键的状态 是否被按下
        keys = pygame.key.get_pressed()
        if keys[K_a]:
            self.move_status = "walk_left"
            self.stand = False
            # 如果下一步要超出界限了，就把坐标设置成极限值
            if self.hit_box[0] - self.speed >= 0:
                self.x -= self.speed
            else:
                self.x = 0
        if keys[K_d]:
            self.move_status = "walk_right"
            self.stand = False
            if self.hit_box[0] + self.speed <= config.max_x - self.hit_box[2]:
                self.x += self.speed
            else:
                self.x = config.max_x - self.hit_box[2]
        if keys[K_w]:
            self.move_status = "walk_up"
            self.stand = False
            if self.hit_box[1] - self.speed >= 0:
                self.y -= self.speed
            else:
                self.y = 0
        if keys[K_s]:
            self.move_status = "walk_down"
            self.stand = False
            if self.hit_box[1] + self.speed <= config.max_y - self.hit_box[3]:
                self.y += self.speed
            else:
                self.y = config.max_y - self.hit_box[3]

    def shot(self, K_LEFT, K_RIGHT, K_UP, K_DOWN):
        keys = pygame.key.get_pressed()
        if keys[K_LEFT]:
            self.move_status = "walk_left"
            self.createBullet(self.move_status)
        elif keys[K_RIGHT]:
            self.move_status = "walk_right"
            self.createBullet(self.move_status)
        elif keys[K_UP]:
            self.move_status = "walk_up"
            self.createBullet(self.move_status)
        elif keys[K_DOWN]:
            self.move_status = "walk_down"
            self.createBullet(self.move_status)

    def createBullet(self, move_status):
        if move_status == "walk_left":
            speed_x, speed_y = -1, 0
        if move_status == "walk_right":
            speed_x, speed_y = 1, 0
        if move_status == "walk_up":
            speed_x, speed_y = 0, -1
        if move_status == "walk_down":
            speed_x, speed_y = 0, 1
        if self.shot_gap % (100 - self.shot_speed) == 0:
            bullet = Bullet(self.x + self.width // 2, self.y + self.height //
                            2, config.bullet_width, config.bullet_height, speed_x, speed_y)
            self.bullets.append(bullet)
            bullet.sound_bullet.play()
        self.shot_gap = (self.shot_gap + 1) % 1000
