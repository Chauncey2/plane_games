import pygame


class Bullet(object):

    def __init__(self):
        # 加载子弹图片
        self.bullet_img = pygame.image.load("res/images/bullet_10.png")
        # 图片矩形
        self.bullet_img_rect = self.bullet_img.get_rect()
        # 子弹状态
        self.is_shot = False
        # 子弹移动速度
        self.speed = 5

    def move_up(self):
        """
        子弹向上移动（玩家飞机）
        :return:
        """
        self.bullet_img_rect.move_ip(0, -self.speed)
        if self.bullet_img_rect[1] <= -self.bullet_img_rect[3]:
            self.is_shot = False

    def move_down(self):
        """
        子弹向下移动（敌方飞机）
        :return:
        """
        pass
