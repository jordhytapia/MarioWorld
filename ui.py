import pygame

class UI:
    def __init__(self, surface):
        self.displaySurface = surface

        #health
        self.healthBar = pygame.image.load('images/health.png').convert_alpha()
        self.healthBarTopLeft = (54,39)
        self.barMaxWidth = 152
        self.barHeight = 4
        #coins
        self.coin = pygame.image.load('images/Coin.png').convert_alpha()
        self.coinRect = self.coin.get_rect(topleft=(50,61))
        self.font = pygame.font.Font('font/SuperMario256.ttf', 15)

    def showHealth(self,current, full):
        self.displaySurface.blit(self.healthBar,(20,10))
        currentHealthRatio = current/full
        currentBarWidth = self.barMaxWidth * currentHealthRatio
        healthBarRect = pygame.Rect(self.healthBarTopLeft, (currentBarWidth,self.barHeight))
        pygame.draw.rect(self.displaySurface, '#dc4949', healthBarRect)

    def showCoins(self,amount):
        self.displaySurface.blit(self.coin, self.coinRect)
        coinAmountSurface = self.font.render('x' + str(amount), False, '#33323d')
        coinAmountRect = coinAmountSurface.get_rect(midleft=(self.coinRect.right + 5, self.coinRect.centery))
        self.displaySurface.blit(coinAmountSurface, coinAmountRect)

