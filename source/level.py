import random

from entity.monster import Monster
import config


def wave(monsters, max_x, max_y):
    if len(monsters) == 0:
        zombie_num = 1
        skeleton = 1
        for i in range(zombie_num):
            monsters.append(create_monster("zombie", max_x, max_y))
        for i in range(skeleton):
            monsters.append(create_monster("skeleton", max_x, max_y))
    return monsters


def create_monster(monster_type, max_x, max_y):
    monsCreateKey = random.randint(1, 4)
    x = 0
    y = 0
    if monsCreateKey == 1:
        x = 0
        y = random.randint(max_y // 3, max_y // 3 * 2)
    elif monsCreateKey == 2:
        x = max_x
        y = random.randint(max_y // 3, max_y // 3 * 2)
    elif monsCreateKey == 3:
        x = random.randint(max_x // 3, max_x // 3 * 2)
        y = 0
    elif monsCreateKey == 4:
        x = random.randint(max_x // 3, max_x // 3 * 2)
        y = max_y
    if monster_type == "zombie":
        mon = Monster(x, y, config.zombie_speed, config.zombie_width, config.zombie_height,
                      config.zombie_pic_path, config.zombie_pic_rate, config.zombie_pic_white, 3)
    elif monster_type == "skeleton":
        mon = Monster(x, y, config.skeleton_speed, config.skeleton_width, config.skeleton_height,
                      config.skeleton_pic_path, config.skeleton_pic_rate, config.skeleton_pic_white, 2)
    return mon
