import sys
from settings import *
from level import Level
import pygame
from overworld import *
from ui import UI

#MARIO
#Jordhy Tapia
#Rina Watanabe

class Game:
    def __init__(self):
        #game attributes
        self.maxLevel = 0
        self.maxHealth = 100
        self.currentHealth = 100
        self.coins = 0

        #audio
        self.BGMusic = pygame.mixer.Sound('audio/mainTheme.wav')
        self.deathSound = pygame.mixer.Sound('audio/Death.wav')

        #overworld
        self.overworld = Overworld(0, self.maxLevel, screen, self.createLevel)
        self.status = 'overworld'
        self.BGMusic.play(loops= -1)

        #ui
        self.ui = UI(screen)


    def createLevel(self, currentLevel):
        self.level = Level(currentLevel, screen, self.createOverworld,self.changeCoins,self.changeHealth)
        self.status = 'level'

    def createOverworld(self, currentLevel, newMaxLevel):
        if newMaxLevel > self.maxLevel:
            self.maxLevel = newMaxLevel
        self.overworld = Overworld(currentLevel, self.maxLevel, screen, self.createLevel)
        self.status = 'overworld'

    def changeCoins(self,ammount):
        self.coins += ammount

    def changeHealth(self,ammount):
        self.currentHealth += ammount
        print(self.currentHealth)

    def checkGameOver(self):
        if self.currentHealth <= 0:
            self.currentHealth = 100
            self.coins = 0
            self.maxLevel = 0
            self.overworld = Overworld(0, self.maxLevel, screen, self.createLevel)
            self.status = 'overworld'
            self.BGMusic.stop()
            self.deathSound.play()


    def run(self):
        if self.status == 'overworld':
            self.overworld.run()
        else:
            self.level.run()
            self.ui.showHealth(self.currentHealth,self.maxHealth)
            self.ui.showCoins(self.coins)
            self.checkGameOver()

pygame.init()
screen = pygame.display.set_mode((screenWidth, screenHeight))
clock = pygame.time.Clock()
game = Game()


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    screen.fill('grey')
    game.run()

    pygame.display.update()
    clock.tick(60)
