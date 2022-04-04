import pygame.sprite
from gameData import  levels
from support import importFolder
from decoration import Sky

class Node(pygame.sprite.Sprite):
    def __init__(self, pos, status, iconSpeed,path):
        super().__init__()
        self.frames = importFolder(path)
        self.frameIndex = 0
        self.image = self.frames[self.frameIndex]
        if status == 'available':
            self.status = 'available'
        else:
            self.status = 'locked'
        self.rect = self.image.get_rect(center = pos)
        self.detectionZone = pygame.Rect(self.rect.centerx-(iconSpeed/2),self.rect.centery-(iconSpeed/2),iconSpeed,iconSpeed)

    def animate(self):
        self.frameIndex += 0.15
        if self.frameIndex >= len(self.frames):
            self.frameIndex = 0
        self.image = self.frames[int(self.frameIndex)]

    def update(self):
        if self.status == 'available':
            self.animate()
        else:
            tintSurface = self.image.copy()
            tintSurface.fill('black', None, pygame.BLEND_RGBA_MULT)
            self.image.blit(tintSurface,(0,0))

class Icon(pygame.sprite.Sprite):
    def __init__(self,pos):
        self.pos = pos
        super().__init__()
        self.image = pygame.image.load('images/mushroom.png').convert_alpha()
        self.rect = self.image.get_rect(center = pos)

    def update(self):
        self.rect.center = self.pos


class Overworld:
    def __init__(self, startLevel, maxLevel, surface, createLevel):
        self.displaySurface = surface
        self.maxLevel = maxLevel
        self.currentLevel = startLevel
        self.createLevel = createLevel
        self.sky = Sky(8)

        #movement logic
        self.moveDirection = pygame.math.Vector2(0,0)
        self.speed = 8
        self.moving = False

        #sprites
        self.setupNodes()
        self.setupIcon()

        #time
        self.startTime = pygame.time.get_ticks()
        self.allowInput = False
        self.timerLength = 800

    def setupNodes(self):
        self.nodes = pygame.sprite.Group()
        for index,node_data in enumerate(levels.values()):
            if index <= self.maxLevel:
                nodeSprite = Node(node_data['node pos'], 'available', self.speed,node_data['node_graphics'])
            else:
                nodeSprite = Node(node_data['node pos'], 'locked', self.speed, node_data['node_graphics'])
            self.nodes.add(nodeSprite)

    def setupIcon(self):
        self.icon = pygame.sprite.GroupSingle()
        iconSprite = Icon(self.nodes.sprites()[self.currentLevel].rect.center)
        self.icon.add(iconSprite)

    def drawPaths(self):
        if self.maxLevel > 0:
            points = [node['node pos'] for index,node in enumerate(levels.values()) if index <= self.maxLevel]
            pygame.draw.lines(self.displaySurface,'#a04f45', False, points, 6)

    def input(self):
        keys = pygame.key.get_pressed()
        if not self.moving and self.allowInput:
            if keys[pygame.K_RIGHT] and self.currentLevel < self.maxLevel:
                self.moveDirection = self.getMovementData('next')
                self.currentLevel += 1
                print(self.moveDirection)
                self.moving = True
            elif keys[pygame.K_LEFT] and self.currentLevel > 0:
                self.moveDirection = self.getMovementData('previous')
                self.currentLevel -= 1
                print(self.moveDirection)
            elif keys[pygame.K_SPACE]:
                self.createLevel(self.currentLevel)

    def getMovementData(self, target):
        start = pygame.math.Vector2(self.nodes.sprites()[self.currentLevel].rect.center)
        if target == 'next':
            end = pygame.math.Vector2(self.nodes.sprites()[self.currentLevel + 1].rect.center)
        else:
            end = pygame.math.Vector2(self.nodes.sprites()[self.currentLevel - 1].rect.center)

        return (end - start).normalize()

    def updateIconPos(self):
        if self.moving and self.moveDirection:
            self.icon.sprite.pos += self.moveDirection * self.speed
            targetNode = self.nodes.sprites()[self.currentLevel]
            if targetNode.detectionZone.collidepoint(self.icon.sprite.pos):
                self.moving = False
                self.moveDirection = pygame.math.Vector2(0,0)

    def inputTimer(self):
        if not self.allowInput:
            currentTime = pygame.time.get_ticks()
            if currentTime -self.startTime >= self.timerLength:
                self.allowInput = True

    def run(self):
        self.inputTimer()
        self.input()
        self.updateIconPos()
        self.icon.update()
        self.nodes.update()

        self.sky.draw(self.displaySurface)
        self.drawPaths()
        self.nodes.draw(self.displaySurface)
        self.icon.draw(self.displaySurface)






