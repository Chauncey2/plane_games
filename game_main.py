import game_map, planes, game_score
import pygame
import sys

WINDOW_WIDTH = 512

WINDOW_HEIGHT = 768


class GameWindow(object):

    def __init__(self):
        # 实例化pygame
        pygame.init()
        # 创建游戏窗口
        self.window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), 0)
        # 添加游戏标题
        pygame.display.set_caption("飞机大战")
        # 设置窗口的图标icon
        image_icon = pygame.image.load("./res/images/app.ico")
        pygame.display.set_icon(image_icon)

        # 创建地图实例
        self.game_map = game_map.GameMap()
        # 创建玩家飞机
        self.hero_plane = planes.HeroPlane()

        # 创建一波敌机
        self.enemy_list = [planes.EnemyPlane() for _ in range(6)]

        # 添加背景音乐
        pygame.mixer_music.load('res/musics/bg2.ogg')
        pygame.mixer_music.play(-1)
        # 加载碰撞音效
        self.boom_sound = pygame.mixer.Sound('res/musics/bomb.wav')

        # 加载分数
        self.game_score = game_score.GameScore(35)

    def run(self):

        while True:
            self.__action()
            self.__draw()
            self.__event()
            self.__update()
            self.__hit_enemy()

    def __action(self):
        """
        处理各种矩形坐标移动
        :return:
        """
        self.game_map.move_down()
        # 遍历子弹
        for bullet in self.hero_plane.bullet_list:
            if bullet.is_shot:
                bullet.move_up()

        # 敌机做自由落体运动
        for enemy in self.enemy_list:
            enemy.move_down()

    def __draw(self):
        """
        根据矩形坐标对元素进行回测
        :return:
        """
        # 添加背景图片
        self.window.blit(self.game_map.img_1, (0, self.game_map.img1_y))
        self.window.blit(self.game_map.img_2, (0, self.game_map.img2_y))

        # 添加英雄飞机
        self.window.blit(self.hero_plane.img, (self.hero_plane.img_rect[0], self.hero_plane.img_rect[1]))

        # 添加子弹
        for bul in self.hero_plane.bullet_list:
            if bul.is_shot:
                self.window.blit(bul.bullet_img, (bul.bullet_img_rect[0], bul.bullet_img_rect[1]))

        # 添加敌机
        for enemy in self.enemy_list:
            self.window.blit(enemy.img, (enemy.img_rect[0], enemy.img_rect[1]))

        # 添分数文字
        self.window.blit(self.game_score.text_obj, (10, 10))

    def __event(self):
        """
        处理窗口的监听事件
        :return:
        """
        # 获取所有窗口的事件监听
        event_list = pygame.event.get()
        for event in event_list:
            # 鼠标单击关闭事件
            if event.type == pygame.QUIT:
                self.game_over()

            # 监听按下事件
            if event.type == pygame.KEYDOWN:
                # 是否按下的是Esc
                if event.key == pygame.K_ESCAPE:
                    self.game_over()
                # 是否按下的是空格
                if event.key == pygame.K_SPACE:
                    self.hero_plane.shoot()

        # 监听长按事件 -> 元组(0没按下，1长按了) 字母对应阿斯克码
        pressed_keys = pygame.key.get_pressed()

        if pressed_keys[pygame.K_UP] or pressed_keys[pygame.K_w]:
            self.hero_plane.move_up()

        if pressed_keys[pygame.K_DOWN] or pressed_keys[pygame.K_s]:
            self.hero_plane.move_down()

        if pressed_keys[pygame.K_LEFT] or pressed_keys[pygame.K_a]:
            self.hero_plane.move_left()

        if pressed_keys[pygame.K_RIGHT] or pressed_keys[pygame.K_d]:
            self.hero_plane.move_right()

    def __update(self):
        """
        刷新页面
        :return:
        """
        pygame.display.update()

    def __hit_enemy(self):
        """
        碰撞检测
        :return:
        """
        for bullet in self.hero_plane.bullet_list:
            if bullet.is_shot:
                for enemy in self.enemy_list:
                    is_hit = pygame.Rect.colliderect(bullet.bullet_img_rect, enemy.img_rect)
                    if is_hit:
                        bullet.is_shot = False
                        enemy.reset()
                        # 播放爆炸音效
                        self.boom_sound.play()
                        # 更新分数
                        self.game_score.set_text()

    def game_over(self):
        # 停止背景音乐
        pygame.mixer.music.stop()
        # 停止音效
        self.boom_sound.stop()
        # 停止游戏引擎
        pygame.quit()
        # 关闭窗口，退出游戏，
        sys.exit()
