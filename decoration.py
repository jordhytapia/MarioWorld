import pygame
from settings import *
from random import randint
from tile import StaticTile
from support import importFolder

class Sky:
    def __init__(self, horizon):
        self.top = pygame.image.load('images/sky.png').convert()
        self.horizon = horizon

        self.top = pygame.transform.scale(self.top,(screenWidth,verticalTileSize))

    def draw(self,surface):
        for row in range(verticalTileNumber):
            y = row * verticalTileSize
            surface.blit(self.top,(0,y))

class Cloud:
    def __init__(self, horizon, levelWidth,cloudNumber):
        clouds = pygame.image.load('images/cloud.png').convert()
        minx = -screenWidth
        maxx = levelWidth + screenWidth
        miny = 0
        maxy = horizon
        self.cloudSprites = pygame.sprite.Group()
        for cloud in range(cloudNumber):
            cloud = clouds
            x = randint(minx, maxx)
            y = randint(miny, maxy)
            sprite = StaticTile(0,x,y,cloud)
            self.cloudSprites.add(sprite)
    def draw(self,surface,shift):
        self.cloudSprites.update(shift)
        self.cloudSprites.draw(surface)
