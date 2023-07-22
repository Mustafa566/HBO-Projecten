from ast import And
from os import times
import random
from tkinter import CENTER, TRUE, X, Y, Button, Tk
from tkinter.font import ROMAN
from turtle import heading, position
import pygame

#Initialises the game
pygame.init()

# Canvas
width = 900
height = 700
backgroundMenu = pygame.image.load('./images/backgroundMenu.png')

# Background
background = pygame.image.load('./images/background.png')
gameOver = pygame.image.load('./images/gameOver.png')
shipImg = pygame.image.load('./images/player.png')

# Shooting and Movement variables
bulletImage = pygame.image.load('./images/bullet.png')
playerLoc = 0
playerX = 30
playerY = 350
playerSpeed = 2
bulletX = 30
bulletY = 350
bulletSpeed = 5
bulletState = "ready"
highscore = 0

# Powerup
powerUp = pygame.image.load('./images/powerUp.png')
powerUpLocX = 900
powerUpLocY = random.randint(50, 650)
powerUpTimer = 0
powerUpEnabled = False

# Enemy related
enemyAmount = 2
enemyTimer = 0
enemyXPos = []
enemyYPos = []
enemyXMovement = []
enemyImages = []
speed = -.6
canShoot = False
bullets=[]
enimies=[]

score = 0
timer = 0

# Player health related
heartOne = pygame.image.load('./images/heart.png')
heartTwo = pygame.image.load('./images/heart.png')
heartThree = pygame.image.load('./images/heart.png')
numHeart = 3

# Add for every enemy x, y position / X movement / images
for enemies in range(enemyAmount):
    enemyXPos.append(random.randint(900, 1200))
    enemyYPos.append(random.randint(80, 660))
    enemyXMovement.append(1)
    enemyImages.append(pygame.image.load('./images/spaceShip.png'))

# Create enemy
def createEnemy(xLoc, yLoc, enemies):
    screen.blit(enemyImages[enemies], (xLoc, yLoc))

#Images
icon = pygame.image.load('images/spaceShip.png')

# Creates the screen
screen = pygame.display.set_mode((width, height))

# Name & icon
pygame.display.set_caption("The amazing spaceshooter")
pygame.display.set_icon(icon)

# Create button class
class Button():
    def __init__(self, X, Y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (X , Y)
        self.clicked = False
        
    def draw(self):
        action = False
        pos = pygame.mouse.get_pos()
        
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True
                
            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False
                
        screen.blit(self.image, (self.rect.x, self.rect.y))

        return action

class Enemy:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.destroyed = False
        self.respawn()

    # Update hearts
    def update(self):
        global numHeart
        self.x -= 1
        if self.x <= 0:
            if numHeart > 0:
                 numHeart -= 1
            self.respawn()

    # Create enemy
    def draw(self,screen):        
        screen.blit(enemyImages[0], (self.x,self.y))

    # Respawn enemy at random location
    def respawn(self):
        self.y = random.randint(50, 650)
        self.x = random.randint(900, 1000)

    # Checks if the bullet hits the enemy with collisions, 
    # if the bullet hits an enemy the bullet gets destroyed. 
    # If it hits nothing it just keeps going.
    def check_collision(self, bullets):
        for bullet in bullets:
            if bullet.rect().colliderect(self.rect()) and bullet.destroyed == False:
                bullet.destroy()
                self.destroy()
            
        # Check collision between enemy and player
        global numHeart
        if enemy.rect().colliderect(self.rectPlayer()):
            enemy.destroy()
            self.destroy()
            numHeart = numHeart - 1

    def rectPlayer(self):
        return pygame.Rect(playerX, playerY, shipImg.get_width(), shipImg.get_height())

    def rect(self):
        return pygame.Rect(self.x, self.y, enemyImages[0].get_width(), enemyImages[0].get_height())
    
    # Destroy enemy
    def destroy(self):
        global score
        score = score + 50
        self.respawn()

class Bullet:
    # Get / set variables
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.destroyed = False

    # Update bullet movement
    def update(self):
        self.x += 5
        if self.x > 950:
            self.destroy()
    
    # Set information
    def rect(self):
        return pygame.Rect(self.x, self.y, bulletImage.get_width(), bulletImage.get_height())
    
    # Create bullet
    def draw(self,screen):
        screen.blit(bulletImage, (self.x,self.y))
    
    # Destroy bullet
    def destroy(self):
        self.destroyed=True

# Game loop
menu = ''
running = True

# Add Sound
music = pygame.mixer.music.load('Sounds/music5.wav')
pygame.mixer.music.play(-1)

# Count bullets
bulletCounter = 0

# Spawn enemies forloop 
for i in range(enemyAmount):
    enimies.append(Enemy())

while running:
    # On quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            break
            
    # Menu background color
    screen.blit(backgroundMenu, (0, 0))

    # Add text to menu
    title_font = pygame.font.SysFont(ROMAN, 50)
    text = title_font.render("", TRUE, (255,255,255))
    textRect = text.get_rect(center=(width/2, 50))
    screen.blit(text, textRect)

    # Load menu buttons
    startImg = pygame.image.load('images/Start.png').convert_alpha()
    exitImg = pygame.image.load('images/Exit.png').convert_alpha()
    
    # Add menu buttons
    startButton = Button(350, 250, startImg) 
    exitButton = Button(350, 400, exitImg)
    
    # Draw button into the screen / onclick change menu variable
    if startButton.draw():
        menu = 'start'
    if exitButton.draw():
        if menu != 'start':
            pygame.quit()
            exit()
    
    # Game starts
    if menu == 'start':
        # Add background image
        screen.blit(background, (0, 0))

        # Create players health (adding hearts)
        screen.blit(heartOne, (0, 5))
        screen.blit(heartTwo, (70, 5))
        screen.blit(heartThree, (140, 5))

        # Add score
        text = title_font.render(str(score), TRUE, (255,255,255))
        textRect = text.get_rect(center=(width - 100, 30))
        screen.blit(text, textRect)

        # Highscore text in game
        textSize = pygame.font.Font(None, 25)
        textContent = textSize.render("Highscore: " + str(highscore), True, (255, 255, 255))
        textPos = textContent.get_rect(center = (width / 2, 30))
        screen.blit(textContent, textPos)

        # Bullet function sets the function
        def player(playerX, playerY):
            screen.blit(shipImg, (playerX, playerY))
        
        # Check bullet if is destroyed
        for bullet in bullets:
            if not bullet.destroyed:
                bullet.update()
                bullet.draw(screen)

        # Check if enemies is destroyed
        for enemy in enimies:
            if not enemy.destroyed:
                enemy.update()
                enemy.check_collision(bullets) # Checks if bullet hits the enemy
                enemy.draw(screen)
        
        # On quit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                break
         
        # Pressed a key
        pressed = pygame.key.get_pressed()
        
        # Shooting mechanic
        if pressed[pygame.K_SPACE] and bulletCounter > 20:
            spawn = False
            for b in bullets:
                # If bullet is destroyed 
                if b.destroyed == True:
                    b.x = bulletX
                    b.y = playerY + 20
                    b.destroyed = False
                    spawn = True
                    bulletCounter = 0
            # Spawn bullet on spacebar
            if spawn == False:
                bullets.append(Bullet(bulletX, playerY + 20))
                bulletCounter=0
        else:
            bulletCounter+=1

        if pressed[pygame.K_UP]: # Press Arrow Key up to move up
            playerY -= playerSpeed
        if pressed[pygame.K_DOWN]: # Press Arrow Key down to move down
            playerY += playerSpeed
        
        # Set player speed if hit power up
        if playerX == powerUpLocX:
            powerUpEnabled = True

        # If player hit power up
        if powerUpEnabled:
            playerSpeed = 4
            powerUpTimer = powerUpTimer + 1

            # If powerUpTimer is 3 seconds long then player gets his normal movement speed
            if powerUpTimer >= 3000:
                powerUpEnabled = False
                playerSpeed = 2

        # Add timer if the powerUp is not been picked up
        else:
            powerUpTimer = powerUpTimer + 1

        # Every 15 seconds spawns power up and if power up is not been picked up
        if powerUpTimer >= 5000 and powerUpEnabled == False:
            powerUpTimer = 0
            powerUpLocX = 900
        
        # Move powerUp from right to left
        else:
            powerUpLocX = powerUpLocX - 1

        # Draw image
        screen.blit(powerUp, (powerUpLocX, powerUpLocY))
         
        # Spawns the player
        player(playerX, playerY)

        # Get mouse location
        mouse = pygame.mouse.get_pos()

        # Player health
        match numHeart:
            # heart 3
            case 2:
                heartThree.fill((255, 255, 255, 0), None, pygame.BLEND_RGBA_MULT)
            # Heart 2
            case 1:
                heartTwo.fill((255, 255, 255, 0), None, pygame.BLEND_RGBA_MULT)
            # Heart 1
            case 0:
                heartOne.fill((255, 255, 255, 0), None, pygame.BLEND_RGBA_MULT)
                screen.blit(gameOver, (0, 0))
                
                # Game over screen
                textSize = pygame.font.Font(None, 150)
                textContent = textSize.render("Game over!", True, (255, 255, 255))
                textPos = textContent.get_rect(center = (width / 2, height / 2))
                screen.blit(textContent, textPos)

                # Restart button
                color_dark = (255, 255, 255)
                pygame.draw.rect(screen, color_dark, [350, 450, 200 , 50])
                textSize = pygame.font.Font(None, 50)
                textContent = textSize.render("Restart!", True, (0, 0, 0))
                textPos = textContent.get_rect(center = (width / 2, 475))
                screen.blit(textContent, textPos)

                # Set highscore
                if score > highscore:
                    highscore = score
                
                # Highscore text
                textSize = pygame.font.Font(None, 50)
                textContent = textSize.render("Highscore: " + str(highscore), True, (255, 255, 255))
                textPos = textContent.get_rect(center = (width / 2, height / 2 - 100))
                screen.blit(textContent, textPos)

                # Don't spawn enemies
                enemyAmount = 0

                # Reset score
                score = 0
        
    
    mouse = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False 
        # On button click restart game
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Get mouse location
            if mouse[0] > 350 and mouse[0] <= 550:
                numHeart = 3
                heartOne = pygame.image.load('./images/heart.png')
                heartTwo = pygame.image.load('./images/heart.png')
                heartThree = pygame.image.load('./images/heart.png')
                enemyAmount = 2

    # Score / timer
    timer = timer + 1
    if timer >= 300:
        score = score + 10
        timer = 0

    # Enemy timer
    enemyTimer = enemyTimer + 1
    if enemyTimer >= 1000:
        enemyAmount = enemyAmount + 1
        enemyTimer = 0

    pygame.display.update()