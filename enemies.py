import pygame
from tile import AnimatedTile
from random import randint

class Enemies(AnimatedTile):
    def __init__(self,size,x,y,path):
        super().__init__(size, x, y, path)
        self.speed = 1
        offsety = y + size
        self.rect = self.image.get_rect(bottomleft = (x,offsety))

    def move(self):
        self.rect.x += self.speed

    def reverseImage(self):
        if self.speed > 0:
            self.image = pygame.transform.flip(self.image,True,False)

    def reverse(self):
        self.speed *= -1


    def update(self,shift):
        self.rect.x += shift
        self.animate()
        self.move()
        self.reverseImage()