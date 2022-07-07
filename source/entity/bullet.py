import pygame
import config


class Bullet():
    def __init__(self, x, y, width, height, speed_x, speed_y):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed_x = speed_x * config.bullet_speed
        self.speed_y = speed_y * config.bullet_speed
        self.pic_bullet = pygame.image.load(config.pic_bullet)
        self.sound_bullet = pygame.mixer.Sound(config.music_bullet)
        self.hit_sound = pygame.mixer.Sound(config.music_hit)
        # 设置判定框
        self.hit_box = (self.x, self.y, self.width, self.height)

    def move(self, monsters, bullets):
        self.x += self.speed_x
        self.y += self.speed_y
        self.hit_box = (self.x, self.y, self.width, self.height)
        for monster in monsters:
            if monster.hit_box[0] <= self.hit_box[0] <= monster.hit_box[0] + monster.hit_box[2] \
                    and monster.hit_box[1] <= self.hit_box[1] <= monster.hit_box[1] + monster.hit_box[3]:
                self.hit(monster, monsters)
                bullets.pop(bullets.index(self))

    def hit(self, monster, monsters):
        self.hit_sound.play()
        if monster.health > 1:
            monster.health -= 1
            monster.left_blood_box[2] = monster.width * \
                ((monster.max_health - monster.health) / monster.max_health)
        else:
            monster.alive = False
            monsters.remove(monster)
