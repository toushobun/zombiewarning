import pygame

from entity.player import Player
import config
import drawer
import level

if __name__ == "__main__":
    # 创建surface窗口
    win = pygame.display.set_mode((config.max_x, config.max_y))
    # 设置窗口的标题
    pygame.display.set_caption("Zombie Warning")
    # 设置背景音乐
    pygame.mixer.init()
    pygame.mixer.music.load(config.music_bg)
    pygame.mixer.music.play(-1)
    # 设置字体
    pygame.font.init()
    pygame.font.SysFont(config.font_style, config.font_size, True)
    # 设置屏幕刷新率
    clock = pygame.time.Clock()
    clock.tick(60)
    # 创建一个背景图片和标题文字
    pic_bg = pygame.image.load(config.pic_bg)
    pic_title = pygame.image.load(config.pic_title)
    pic_gameover = pygame.image.load(config.pic_gameover)
    pic_intro = pygame.image.load(config.pic_intro)
    # 创建玩家
    man = Player(config.max_x/2, config.max_y/2, config.player_speed, config.player_width,
                 config.player_height, config.player_pic_path, config.player_pic_rate, config.player_shot_speed)
    # 创建怪物组
    monsters = []
    run = True
    while run:
        # 判断窗口事件
        for event in pygame.event.get():
            # 判断用户是否退出
            if event.type == pygame.QUIT:
                run = False

        # 监听玩家的游戏按键
        man.move(pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s)
        man.shot(pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN)
        if len(monsters) == 0:
            monsters = level.wave(monsters, config.max_x, config.max_y)

        # 刷新屏幕
        drawer.draw(win, man, monsters, pic_bg, config.max_x, config.max_y)
