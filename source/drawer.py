import pygame
import config


def draw_player(win, man):
    # 如果玩家静止
    if man.stand:
        win.blit(man.pic[man.move_status][0], (man.x, man.y))
    else:
        win.blit(man.pic[man.move_status]
                 [man.walk_count // config.player_move_show_rate % man.pic_rate], (man.x, man.y))
        man.walk_count += 1
    # 显示判定框
    if config.hit_box_visible:
        pygame.draw.rect(win, (255, 0, 0), man.hit_box, 2)


def draw_bullet(win, bullets, monsters, max_x, max_y):
    for bullet in bullets:
        if 0 < bullet.x < max_x and 0 < bullet.y < max_y:
            bullet.move(monsters, bullets)
            win.blit(bullet.pic_bullet, (bullet.x, bullet.y))
        else:
            bullets.pop(bullets.index(bullet))
        # 显示判定框
        if config.hit_box_visible:
            pygame.draw.rect(win, (255, 0, 0), bullet.hit_box, 2)


def draw_monster(win, monsters, player_hit_box):
    for monster in monsters:
        monster.move(player_hit_box)
        # 设置交替显示图片
        win.blit(monster.pic[monster.move_status]
                 [monster.walk_count // config.monster_move_show_rate % monster.pic_rate], (monster.x, monster.y))
        # 显示血条
        pygame.draw.rect(win, (255, 0, 0), monster.blood_box)
        pygame.draw.rect(win, (0, 128, 0), monster.left_blood_box)
        # 显示判定框
        if config.hit_box_visible:
            pygame.draw.rect(win, (255, 0, 0), monster.hit_box, 2)
            pygame.draw.circle(
                win, (255, 0, 0), (monster.middle_x, monster.middle_y), 5)


def draw(win, man, monsters, pic_bg, max_x, max_y):
    # 画背景
    win.blit(pic_bg, (0, 0))
    # 画玩家
    draw_player(win, man)
    # 画子弹
    draw_bullet(win, man.bullets, monsters, max_x, max_y)
    # 画敌人
    draw_monster(win, monsters, man.hit_box)
    # 屏幕刷新
    pygame.display.update()
    # print("玩家：(%d,%d)" % (man.hit_box[0], man.hit_box[1]))
