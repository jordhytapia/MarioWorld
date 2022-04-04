import pygame
from support import importCsvLayout, importCutGraphics
from settings import*
from tile import Tile, StaticTile, AnimatedTile
from enemies import Enemies
from decoration import *
from player import Player
from overworld import *
from gameData import *

class Level:
    def __init__(self, currentLevel, surface, createOverworld, changeCoins, changeHealth):
        self.displaySurface = surface
        self.worldShift = -1

        #audio
        self.stompSound = pygame.mixer.Sound('audio/stomp.wav')
        self.deathSound = pygame.mixer.Sound('audio/Death.wav')

        #overworld connection
        self.createOverworld = createOverworld
        self.currentLevel = currentLevel
        levelData = levels[self.currentLevel]
        self.newMaxLevel = levelData['unlock']

        #player layout
        playerLayout = importCsvLayout(levelData['player'])
        self.player = pygame.sprite.GroupSingle()
        self.goal = pygame.sprite.GroupSingle()
        self.playerSetUp(playerLayout,changeHealth)

        #user interface
        self.changeCoins = changeCoins

        #terrain layout
        terrainLayout = importCsvLayout(levelData['terrain'])
        self.terrainSprites = self.createTileGroup(terrainLayout, 'terrain')

        #bricks layout
        bricksLayout = importCsvLayout(levelData['bricks'])
        self.bricksSprites = self.createTileGroup(bricksLayout, 'bricks')

        #gold layout
        goldLayout = importCsvLayout(levelData['gold'])
        self.goldSprites = self.createTileGroup(goldLayout, 'gold')

        #enemies layout
        enemiesLayout = importCsvLayout(levelData['enemies'])
        self.enemiesSprites = self.createTileGroup(enemiesLayout, 'enemies')

        #constraints
        constraintsLayout = importCsvLayout(levelData['constraints'])
        self.constraintsSprites = self.createTileGroup(constraintsLayout, 'constraints')

        #decorations
        self.sky = Sky(8)
        levelWidth = len(terrainLayout[0]) * verticalTileSize
        self.clouds = Cloud(100,levelWidth,20)


    def createTileGroup(self, layout, type):
        spriteGroup = pygame.sprite.Group()
        for rowIndex, row in enumerate(layout):
            for colIndex, val in enumerate(row):
                if val != '-1':
                    x = colIndex * verticalTileSize
                    y = rowIndex * verticalTileSize

                    if type == 'terrain':
                        blockTypeList = importCutGraphics('images/tiles.png')
                        tileSurface = blockTypeList[int(val)]
                        sprite = StaticTile(verticalTileSize, x, y, tileSurface)
                    if type == 'bricks':
                        bricksTypeList = importCutGraphics('images/tiles.png')
                        tileSurface = bricksTypeList[int(val)]
                        sprite = StaticTile(verticalTileSize, x, y, tileSurface)
                    if type == 'gold':
                        goldTypeList = importCutGraphics('images/tiles.png')
                        tileSurface = goldTypeList[int(val)]
                        sprite = StaticTile(verticalTileSize, x, y, tileSurface)
                    if type == 'enemies':
                        if val == '3':
                            sprite = Enemies(verticalTileSize, x, y,'images/enemies')
                        if val == '2':
                            sprite = Enemies(verticalTileSize, x, y, 'images/shell')
                    if type == 'constraints':
                        sprite = Tile(verticalTileSize, x, y)

                    spriteGroup.add(sprite)
        return spriteGroup

    def playerSetUp(self,layout, changeHealth):
        spriteGroup = pygame.sprite.Group()
        for rowIndex, row in enumerate(layout):
            for colIndex, val in enumerate(row):
                x = colIndex * verticalTileSize
                y = rowIndex * verticalTileSize
                if val == '28':
                    sprite = Player((x,y), self.displaySurface, changeHealth)
                    self.player.add(sprite)
                if val == '27':
                    flagSurface = pygame.image.load('images/finish.png').convert_alpha()
                    sprite = StaticTile(verticalTileSize,x,y,flagSurface)
                    self.goal.add(sprite)

    def enemyCollissionReverse(self):
        for enemy in self.enemiesSprites.sprites():
            if pygame.sprite.spritecollide(enemy, self.constraintsSprites, False):
                enemy.reverse()

    def horizontalMovementCollision(self):
        player = self.player.sprite
        player.rect.x += player.direction.x * player.speed
        collide = self.terrainSprites.sprites() + self.bricksSprites.sprites() + self.goldSprites.sprites()
        for sprite in collide:
            if sprite.rect.colliderect(player.rect):
                if player.direction.x < 0:
                    player.rect.left = sprite.rect.right
                    player.onLeft = True
                    self.current_x = player.rect.left
                elif player.direction.x > 0:
                    player.rect.right = sprite.rect.left
                    player.onRight = True
                    self.current_x = player.rect.right

        if player.onLeft and (player.rect.left < self.current_x or player.direction.x >= 0):
            player.onLeft = False
        if player.onRight and (player.rect.right > self.current_x or player.direction.x <= 0):
            player.onRight = False

    def verticalMovementCollision(self):
        player = self.player.sprite
        player.applyGravity()
        collide = self.terrainSprites.sprites() + self.bricksSprites.sprites() + self.goldSprites.sprites()
        for sprite in collide:
            if sprite.rect.colliderect(player.rect):
                if player.direction.y > 0:
                    player.rect.bottom = sprite.rect.top
                    player.direction.y = 0
                    player.onGround = True
                elif player.direction.y < 0:
                    player.rect.top = sprite.rect.bottom
                    player.direction.y = 0
                    player.onCeiling = True

        if player.onGround and player.direction.y < 0 or player.direction.y > 1:
            player.onGround = False
        if player.onCeiling and player.direction.y > 0:
            player.onCeiling = False

    def scrollX(self):
        player = self.player.sprite
        playerX = player.rect.centerx
        directionX = player.direction.x

        if playerX < screenWidth / 2 and directionX < 0:
            self.worldShift = 2
            player.speed = 0
        elif playerX > screenWidth - (screenWidth / 2) and directionX > 0:
            self.worldShift = -2
            player.speed = 0
        else:
            self.worldShift = 0
            player.speed = 8

    def checkDeath(self):
        if self.player.sprite.rect.top > screenHeight:
            self.createOverworld(self.currentLevel, 0)
            self.deathSound.play()

    def checkWin(self):
        if pygame.sprite.spritecollide(self.player.sprite, self.goal, False):
            self.createOverworld(self.currentLevel, 0)

    def checkCoinCollisions(self):
        collidedCoinsList = pygame.sprite.spritecollide(self.player.sprite,self.enemiesSprites, True)
        if collidedCoinsList:
            for coin in collidedCoinsList:
                self.changeCoins(1)

    def checkEnemyCollisions(self):
        enemyColissions = pygame.sprite.spritecollide(self.player.sprite,self.enemiesSprites, False)
        if enemyColissions:
            for enemy in enemyColissions:
                enemyCenter = enemy.rect.centery
                enemytop = enemy.rect.top
                playerBottom = self.player.sprite.rect.bottom
                if enemytop < playerBottom < enemyCenter and self.player.sprite.direction.y >= 0:
                    self.stompSound.play()
                    self.player.sprite.direction.y = -10
                    enemy.kill()
                    self.changeCoins(100)
                else:
                    self.player.sprite.getDamage()

    def run(self):
        self.sky.draw(self.displaySurface)
        self.clouds.draw(self.displaySurface,self.worldShift)

        self.terrainSprites.update(self.worldShift)
        self.terrainSprites.draw(self.displaySurface)

        self.bricksSprites.update(self.worldShift)
        self.bricksSprites.draw(self.displaySurface)

        self.goldSprites.update(self.worldShift)
        self.goldSprites.draw(self.displaySurface)

        self.enemiesSprites.update(self.worldShift)
        self.constraintsSprites.update(self.worldShift)
        self.enemyCollissionReverse()
        self.enemiesSprites.draw(self.displaySurface)

        self.player.update()
        self.horizontalMovementCollision()
        self.verticalMovementCollision()
        self.scrollX()
        self.player.draw(self.displaySurface)
        self.goal.update(self.worldShift)
        self.goal.draw(self.displaySurface)

        self.checkDeath()
        self.checkWin()

        #self.checkCoinCollisions()
        self.checkEnemyCollisions()



