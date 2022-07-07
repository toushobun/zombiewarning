import random

from entity.person import Person
import config


class Monster(Person):
    def __init__(self, x, y, speed, width, height, pic_path, pic_rate, pic_white, health):
        """初始化怪物

        Args:
            x (int): 怪物的x坐标
            y (int): 怪物的y坐标
            speed (int): 怪物一次移动的距离
            width (int): 怪物的宽度
            height (int): 怪物的高度
            pic_path (string): 怪物图片路径
            pic_rate (int): 怪物图片帧率
            pic_white (int): 怪物图片留白
            health (int): 怪物血量
        """
        super().__init__(x, y, speed, width, height, pic_path, pic_rate)
        self.pic_white = pic_white
        self.middle_x = self.x + width // 2
        # 图片有留白，需调整
        self.middle_y = self.y + height // 2 + self.pic_white
        # 默认移动方式是先定位x轴再定位y轴
        self.move_way = 1
        # 设置血量
        self.max_health = health
        self.health = health
        # 设置判定框
        self.hit_box = (self.x, self.y + self.pic_white,
                        self.width, self.height)
        # 设置血条
        self.blood_box = [self.hit_box[0], self.hit_box[1], 36, 4]
        self.left_blood_box = [self.hit_box[0], self.hit_box[1], 36, 4]

    def move(self, player_hit_box):
        # 每行动50格，随即便换一次行动方式
        if self.walk_count % config.move_way_key == 0:
            self.move_way = random.randint(1, 2)
        # 怪物一次走2格，如果只判断玩家坐标，容易左右摇摆，需要设置缓冲，判断中心点坐标是否进入角色判定框
        if self.move_way == 1:
            # 如果怪物在玩家判定框右边
            if self.middle_x >= player_hit_box[0] + player_hit_box[2]:
                self.middle_x -= self.speed
                self.x -= self.speed
                self.move_status = "walk_left"
            # 如果怪物在玩家判定框左边
            elif self.middle_x <= player_hit_box[0]:
                self.middle_x += self.speed
                self.x += self.speed
                self.move_status = "walk_right"
            # 如果怪物在玩家判定框上边
            elif self.middle_y >= player_hit_box[1] + player_hit_box[3]:
                self.middle_y -= self.speed
                self.y -= self.speed
                self.move_status = "walk_up"
            # 如果怪物在玩家判定框下边
            elif self.middle_y <= player_hit_box[1]:
                self.middle_y += self.speed
                self.y += self.speed
                self.move_status = "walk_down"
            self.move_record()
        elif self.move_way == 2:
            # 如果怪物在玩家判定框上边
            if self.middle_y >= player_hit_box[1] + player_hit_box[3]:
                self.middle_y -= self.speed
                self.y -= self.speed
                self.move_status = "walk_up"
            # 如果怪物在玩家判定框下边
            elif self.middle_y <= player_hit_box[1]:
                self.middle_y += self.speed
                self.y += self.speed
                self.move_status = "walk_down"
            # 如果怪物在玩家判定框右边
            elif self.middle_x >= player_hit_box[0] + player_hit_box[2]:
                self.middle_x -= self.speed
                self.x -= self.speed
                self.move_status = "walk_left"
            # 如果怪物在玩家判定框左边
            elif self.middle_x <= player_hit_box[0]:
                self.middle_x += self.speed
                self.x += self.speed
                self.move_status = "walk_right"
            self.move_record()

    def move_record(self):
        self.walk_count += 1
        # 更新判定框
        self.hit_box = (self.x, self.y + self.pic_white,
                        self.width, self.height)
        # 更新血条
        self.blood_box = [self.hit_box[0], self.hit_box[1], self.width, 4]
        self.left_blood_box = [self.hit_box[0], self.hit_box[1], self.width, 4]
