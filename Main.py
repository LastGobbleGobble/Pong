import pygame
import random

WIDTH = 1000
HEIGHT = 600
FPS = 60

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

running = True

class Player(pygame.sprite.Sprite):
    #sprite for the Player, also the player's paddle
    def __init__(self, playerNum):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((25,125))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.centery = HEIGHT / 2
        self.speedx = 0
        self.speedy = 0

        self.playerNum = playerNum
        buffer = 10
        if self.playerNum == 1: # player 1 (left paddle)
            self.rect.left = 0 + buffer
        else: # player 2 (right paddle)
            self.rect.right = WIDTH - buffer

    def update(self):
        self.speedx = 0 #makes the paddle only move when the key is pressed down
        self.speedy = 0 #fiddle around with things like this to get different motion effects
        keystate = pygame.key.get_pressed()

        if self.playerNum == 1:
            if keystate[pygame.K_w]:
                self.speedy = -5
            if keystate[pygame.K_s]:
                self.speedy = 5
        else:
            if keystate[pygame.K_UP]:
                self.speedy = -5
            if keystate[pygame.K_DOWN]:
                self.speedy = 5

        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT

class Ball(pygame.sprite.Sprite):
    # sprite for the Player, also the player's paddle
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((25, 25))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.speedx = 4
        self.speedy = -6

    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.top < 0:
            self.rect.top = 0
            self.speedy = -self.speedy
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
            self.speedy = -self.speedy
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
            self.speedx = -self.speedx
        if self.rect.left < 0 or self.rect.right > WIDTH:
            pygame.quit() #exits the game

    def bounce(self):
        self.speedx = -self.speedx

# initialize pygame and create window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()

all_sprites = pygame.sprite.Group()
ball = Ball()
all_sprites.add(ball)
player_sprites = pygame.sprite.Group()
player1 = Player(1)
all_sprites.add(player1)
player_sprites.add(player1)
player2 = Player(2)
all_sprites.add(player2)
player_sprites.add(player2)

# Game loop
running = True
while running:
    # keep loop running at the right speed
    clock.tick(FPS)
    # Process input (events)
    for event in pygame.event.get():
            # check for closing window
            if event.type == pygame.QUIT:
                    running = False
    # Update
    all_sprites.update()

    # check to see if a mob hit the player
    hits = pygame.sprite.spritecollide(ball, player_sprites, False) # checks paddle1 hit the ball and the bool dtermines if the hit object should be deleted, also stores a list of all the mobs that hit that object
    if hits:
        print("connection")
        ball.bounce()

    # Draw / render
    screen.fill(BLACK)
    all_sprites.draw(screen)
    # after drawing everything, flip the display
    pygame.display.flip()
pygame.quit()