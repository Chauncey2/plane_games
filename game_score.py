import pygame
import random


class GameScore:
    __cls_score = 0

    def __init__(self, font_size):
        self.font = pygame.font.SysFont("SimHei", font_size)
        self.text_obj = self.font.render("分数：0", 1, (255, 255, 255))

    def set_text(self):
        self.__cls_score += 1
        # 随机颜色
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        self.text_obj = self.font.render("分数:%d" % self.__cls_score, 1, (r, g, b))
