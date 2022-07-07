import pygame


class Person():
    def __init__(self, x, y, speed, width, height, pic_path, pic_rate):
        """初始化角色

        Args:
            x (int): 角色的x坐标
            y (int): 角色的y坐标
            speed (int): 角色一次移动的距离
            width (int): 角色的宽度
            height (int): 角色的高度
            pic_path (string): 角色图片路径
            pic_rate (int): 角色图片帧率
        """
        self.x, self.y = x, y
        # 人物一次移动的距离
        self.speed = speed
        # 人物的宽度和高度
        self.width, self.height = width, height
        # 四个方向走动的图片列表
        self.pic = {
            "stand": pygame.image.load(pic_path + "/0.png"),
            "walk_left": [],
            "walk_right": [],
            "walk_up": [],
            "walk_down": [],
        }
        self.pic_rate = pic_rate
        # 读取四个方向走的图片
        for i in range(0, self.pic_rate):
            self.pic["walk_left"].append(
                pygame.image.load(pic_path + "/a%d.png" % i))
            self.pic["walk_right"].append(
                pygame.image.load(pic_path + "/d%d.png" % i))
            self.pic["walk_up"].append(
                pygame.image.load(pic_path + "/w%d.png" % i))
            self.pic["walk_down"].append(
                pygame.image.load(pic_path + "/s%d.png" % i))
        # 走到第几步
        self.walk_count = 0
        # 是否在静止
        self.stand = True
        # 行动状态
        self.move_status = "walk_down"
        # 碰撞检测区(左上角x，左上角y，宽度，高度）
        self.hit_box = (self.x, self.y, self.width, self.height)
        # 设置是否存活
        self.alive = True
        # 设置判定框
        self.hit_box = (self.x, self.y, self.width, self.height)
        # 设置图片留白
        self.pic_white = 0
