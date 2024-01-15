import pygame
import random
import math
from pygame import mixer

# Intialising the pygame 
pygame.init()

# Creating the screen

screen = pygame.display.set_mode((800,600))

# Title, Icon and Background

pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("icon.png")
pygame.display.set_icon(icon)
background = pygame.image.load("background.png")

# Collision

score = 0

def collison(bulletX, enemyX, bulletY, enemyY):
    distance = math.sqrt((math.pow(bulletX - enemyX, 2)) + math.pow(bulletY - enemyY, 2))

    if distance < 20:
        return True
    else:
        return False

# Bullet

bulletImg = pygame.image.load("bullet.png")
bulletX = 0
bulletY = 480
bulletX_delta = 0
bulletY_delta = 10
bullet_state = "ready"

def bullet(x,y):
    global bullet_state
    screen.blit(bulletImg, (x + 16, y + 10)) 

# Player

playerImg = pygame.image.load('player.png')
playerX = 370
playerY = 480
playerXdelta = 0
playerYdelta = 0

def player(x,y):
    screen.blit(playerImg, (x, y))

# Enemy 
enemyImg = []
enemyX = []
enemyY = []
enemyX_delta = []
enemyY_delta = []
enemyXi = 0

number_of_enemies = 4

for i in range(number_of_enemies):
    enemyImg.append(pygame.image.load("enemy.png"))
    enemyX.append(random.randint(0, 800))
    enemyY.append(random.randint(50,150))
    enemyX_delta.append(2)
    enemyY_delta.append(64)
    enemyXi += 184

def enemy(x,y,i):
    screen.blit(enemyImg[i], (x,y))

# Score

score_value = 0
font = pygame.font.Font("pixel_font.ttf", 32)

textX = 10
textY = 10

def show_score(x,y):
    score = font.render("Score: " + str(score_value), True, (255,255,255))
    screen.blit(score, (x,y))

# Game Over
    
over_font = pygame.font.Font("pixel_font.ttf", 256) 

def game_over_text(x,y):
    over = font.render("GAME OVER",True,(0,0,0))
    screen.blit(over, (x,y))

# Game Loop

if "__main__" == __name__:

    running = True

    while running:
        screen.fill((255,0,0))
        screen.blit(background, (0,0))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
            # Keystroke is left or right
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    playerXdelta = -1.5
                if event.key == pygame.K_RIGHT:
                    playerXdelta = 1.5
                if event.key == pygame.K_SPACE:
                    bullet_state = "fire"
                    bullet_sound = mixer.Sound("bullet_sound.wav")
                    bullet_sound.play()
            if event.type == pygame.KEYUP:
                if event.type == pygame.K_RIGHT or pygame.K_LEFT:
                    playerXdelta = 0
        
        if bulletY <= 0:
            bulletY = 480
            bullet_state = "ready"

        if bullet_state is "fire":
            bulletX = playerX
            bullet(bulletX, bulletY)
            bulletY -= bulletY_delta

        for i in range(number_of_enemies):

            # Game Over
            if enemyY[i] > 440:
                for j in range(number_of_enemies):
                    enemyY[j] = 2000
                game_over_text(200,300)
                break

            enemyX[i] += enemyX_delta[i]
            if enemyX[i] <= 0:
                enemyX_delta[i] = 2
                enemyY[i] += enemyY_delta[i]
            elif enemyX[i] >= 736:
                enemyX_delta[i] = -2
                enemyY[i] += enemyY_delta[i]
            
            if collison(bulletX, enemyX[i], bulletY, enemyY[i]) is True:
                bulletY = 480
                bullet_state = "ready"
                score_value += 1
                die_sound = mixer.Sound("death.wav")
                die_sound.play()
                enemyX[i] = random.randint(0, 736)
                enemyY[i] = random.randint(50, 150)
            
            enemy(enemyX[i],enemyY[i],i)

        playerX += playerXdelta
        playerY += playerYdelta

        if playerX <= 0:
            playerX = 0
        elif playerX >= 736:
            playerX = 736

        player(playerX ,playerY)
        show_score(textX,textY)
         

        pygame.display.update()
