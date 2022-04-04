import pygame
from support import importFolder
from math import sin

class Player(pygame.sprite.Sprite):
    def __init__(self,pos,surface,changeHealth):
        super().__init__()
        self.importCharacterAssets()
        self.frameIndex = 0
        self.animationSpeed = 0.15
        self.status = 'idle'
        self.image = self.animations[self.status][self.frameIndex]
        self.rect = self.image.get_rect(topleft = pos)

        #audio
        self.jumpSound = pygame.mixer.Sound('audio/Jump.wav')
        self.hitSound = pygame.mixer.Sound('audio/hit.wav')
        self.deathSound = pygame.mixer.Sound('audio/Death.wav')


        #player movement
        self.direction = pygame.math.Vector2(0,0)
        self.speed = 8
        self.gravity = 0.8
        self.jumpSpeed = -13

        self.status = 'idle'
        self.facingRight = True
        self.onGround = False
        self.onCeiling = False
        self.onLeft = False
        self.onRight = False

        self.changeHealth = changeHealth
        self.invincible = False
        self.invincibilityDuration = 500
        self.hurtTime = 0


    def importCharacterAssets(self):
        self.animations = {'die':[],'idle':[], 'jump':[], 'run':[], 'slide':[]}
        dieImages = [pygame.transform.rotozoom(pygame.image.load(f'images/die/{n}.png'), 0, 1.2) for n in range(1)]
        idleImages = [pygame.transform.rotozoom(pygame.image.load(f'images/idle/{n}.png'), 0, 1.2) for n in range(1)]
        jumpImages = [pygame.transform.rotozoom(pygame.image.load(f'images/jump/{n}.png'), 0, 1.2) for n in range(1)]
        runImages = [pygame.transform.rotozoom(pygame.image.load(f'images/run/{n}.png'), 0, 1.2) for n in range(4)]
        slideImages = [pygame.transform.rotozoom(pygame.image.load(f'images/slide/{n}.png'), 0, 1.2) for n in range(1)]

        self.animations['die'] = dieImages
        self.animations['idle'] = idleImages
        self.animations['jump'] = jumpImages
        self.animations['run'] = runImages
        self.animations['slide'] = slideImages
        print(self.animations['run'][0])


    def animate(self):
        animations = self.animations[self.status]

        self.frameIndex += self.animationSpeed
        if self.frameIndex >= len(animations):
            self.frameIndex = 0
        self.image = animations[int(self.frameIndex)]

        image = animations[int(self.frameIndex)]
        if self.facingRight:
            self.image = image
        else:
            flippedImage = pygame.transform.flip(image,True,False)
            self.image = flippedImage

        if self.invincible:
            alpha = self.waveValue()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)
        #set the rect
        if self.onGround and self.onRight:
            self.rect = self.image.get_rect(bottomright = self.rect.bottomright)
        elif self.onGround and self.onLeft:
            self.rect = self.image.get_rect(bottomleft = self.rect.bottomleft)
        elif self.onGround:
            self.rect = self.image.get_rect(midbottom = self.rect.midbottom)
        elif self.onCeiling and self.onRight:
            self.rect = self.image.get_rect(topright = self.rect.topright)
        elif self.onCeiling and self.onLeft:
            self.rect = self.image.get_rect(topleft = self.rect.topleft)
        elif self.onCeiling:
            self.rect = self.image.get_rect(midtop = self.rect.midtop)
        else:
            self.rect = self.image.get_rect(center = self.rect.center)


    def getInput(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:
            self.direction.x = 0.3
            self.facingRight = True
        elif keys[pygame.K_LEFT]:
            self.direction.x = -0.3
            self.facingRight = False
        else:
            self.direction.x = 0

        if keys[pygame.K_SPACE] and self.onGround:
            self.jump()

    def getStatus(self):
        if self.direction.y < 0:
            self.status = 'jump'
        elif self.direction.y > 1:
            self.status = 'slide'
        else:
            if self.direction.x != 0:
                self.status = 'run'
            else:
                self.status = 'idle'

    def applyGravity(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y

    def jump(self):
        self.jumpSound.play()
        self.jumpSound.set_volume(0.2)
        self.direction.y = self.jumpSpeed

    def getDamage(self):
        if not self.invincible:
            self.hitSound.play()
            self.changeHealth(-10)
            self.invincible = True
            self.hurtTime = pygame.time.get_ticks()

    def invincibilityTimer(self):
        if self.invincible:
            currentTime = pygame.time.get_ticks()
            if currentTime - self.hurtTime >= self.invincibilityDuration:
                self.invincible = False

    def waveValue(self):
        value = sin(pygame.time.get_ticks())
        if value >= 0: return 255
        else: return 0


    def update(self):
        self.getInput()
        self.getStatus()
        self.animate()
        self.invincibilityTimer()
        self.waveValue()



