import pygame
import random
import math
from pygame import mixer


# game variables that can be modified 
player_speed = 5
spawning_no_of_enemy = 1
spiritSize = 32

# Game Url Constant
playerUrl = 'img/player.png'
gameIconUrl = 'img/icon.png'
bgUrl = 'img/background.png'
enemyUrl = 'img/enemy.png'
bulletUrl = 'img/bullet.png'
bgmusicUrl = 'sound/bgmusic.ogg'
explosion_sound_url = 'sound/explosion.wav'
laser_sound_url = 'sound/laser.wav'

# initializing the game
pygame.init()

# Game Variables 
level = 1
bullet_speed = player_speed * 2.25
enemy_min_speed = (player_speed * 4/10)
enemy_max_speed = (player_speed * 7/10)
no_of_bullet_can_fired = 1
def bulletconfig():
  global no_of_bullet_can_fired
  ''' sets the amount of bullet can fired '''
  no_of_bullet_can_fired = (spawning_no_of_enemy // 3)
  #ensuring that no of bullet isn't less than 1
  if no_of_bullet_can_fired == 0:
    no_of_bullet_can_fired = 1
bulletconfig()

# screen size
screen_width = 400
screen_height = (screen_width*(3/4))

# Loading and playing music
mixer.music.load(bgmusicUrl)
mixer.music.play()

# Loading gamw sounds
explosion_sound = mixer.Sound(explosion_sound_url)
# laser or bullet is same stuff
bullet_sound = mixer.Sound(laser_sound_url)

# screen of the game
screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption('Star Shooter By Aman Gamarz')
icon = pygame.image.load(gameIconUrl)
pygame.display.set_icon(icon)

# Loading Background Image
bgImg = pygame.image.load(bgUrl)

# Loading Score text in game
score = 0
font = pygame.font.Font('font-family/myfont.ttf',16)
def scoreRender():
  text = font.render('Score : '+str(score),True,(255,255,255))
  screen.blit(text,(0,0))

# Loading Levl text in game
score = 0
font = pygame.font.Font('font-family/myfont.ttf',16)
def levelRender():
  text = font.render('Level : '+str(level),True,(255,255,255))
  screen.blit(text,(70,0))

# Loading gameovertext
gameover_font = pygame.font.Font('font-family/myfont.ttf',64)
gameoverText = gameover_font.render('Game Over',True,(255,255,255))
gameoverRect = gameoverText.get_rect()
gameoverRect.center = (screen_width//2,screen_height//2)

# resizing bg according to screen 
pygame.transform.scale(bgImg,(screen_width,screen_height))

# Player
playerImg = pygame.image.load(playerUrl)
pygame.transform.scale(playerImg,(spiritSize,spiritSize))
playerX = (screen_width / 2)-16
playerY = ((screen_height / 2)+(screen_height/4))-16

# Player Speed
pdx = 0 # player ∆x (speed in x)
pdy = 0 # player ∆y (speed in y)

# Player Loading Function
def player():
  global playerX
  global playerY
  global pdx
  global pdy
  # incremnting the player values
  playerX += pdx
  playerY += pdy
  
  # blocking player from going upwards
  if playerX <=  0:
    playerX = 0
    
  # blocking player from going downwards
  if playerX >=  screen_width-32:
    playerX = screen_width-32
    
  # blocking player from going leftways
  if playerY <=  0:
    playerY = 0
    
  # blocking player from going rightways
  if playerY >=  screen_height-32:
    playerY = screen_height-32
  screen.blit(playerImg,(playerX,playerY))



# Enemy class To Create Objects
class Enemy:
  def __init__(self):
    self.enemyImg = pygame.image.load(enemyUrl)
    pygame.transform.scale(self.enemyImg,(spiritSize,spiritSize))
    self.enemyX = random.randint(0,(screen_width-32))
    self.enemyY = random.randint(0,(screen_height / 4))
    self.xv = random.uniform(enemy_min_speed,enemy_max_speed) # enemy ∆x (speed in x)
    self.edx = self.xv
    self.edy = 0 # enemy ∆y (speed in y)
    
  def enemyLoad(self):
    self.enemyX += self.edx
    self.enemyY += self.edy
    
    if self.enemyX <=  0:
      self.enemyX = 0
      self.enemyY += 32
      self.edx = self.xv
      
    if self.enemyX >=  screen_width-32:
      self.enemyX = screen_width-32
      self.enemyY += 32
      self.edx = -self.xv
    
      
    
    screen.blit(self.enemyImg,(self.enemyX,self.enemyY))

# Creating Instances Of Enemey Class
enemyArr = []
for _ in range(spawning_no_of_enemy):
  enemyArr.append(Enemy())

# Enemy class To Create Objects
bulletImg = pygame.image.load(bulletUrl)
pygame.transform.scale(bulletImg,(spiritSize / 2,spiritSize /2))
class Bullet:
  def __init__(self):
    self.bulletX = playerX + spiritSize / 4
    self.bulletY = playerY
    # bullet ∆y (speed in y)
    self.edy = -(bullet_speed) 
    
  def bulletLoad(self):
    self.bulletY += self.edy
    
    screen.blit(bulletImg,(self.bulletX,self.bulletY))
    
# Creating Instances Of Enemey Class
bulletArr = []

# Is Collide With Bullet - Functions 
def isbulletcolide():
  global score
  global level
  global spawning_no_of_enemy
  '''
  Distance Between Two Points Is :
        √(a-x)²+(b-y)²
  Where Two Points Are (a,b) And (x,y)
  '''
  for b_index,bullet in enumerate(bulletArr):
    x1 = bullet.bulletX
    y1 = bullet.bulletY
    for e_index,enemy in enumerate(enemyArr):
      x2 = enemy.enemyX
      y2 = enemy.enemyY
      # s = distance
      s = math.sqrt(math.pow((x1-x2),2)+math.pow((y1-y2),2))
      if s <= 22.6 :
        enemyArr.pop(e_index)
        explosion_sound.play()
        enemyArr.append(Enemy())
        bulletArr.pop(b_index)
        score += 1
        if score // 5 > level:
          level = score // 5
          spawning_no_of_enemy += 1
          bulletconfig()
        break
    
# Is Collide With Player - Functions 
def isplayercolide():
  global score
  '''
  Distance Between Two Points Is :
        √(a-x)²+(b-y)²
  Where Two Points Are (a,b) And (x,y)
  '''
  x1 = playerX
  y1 = playerY
  for e_index,enemy in enumerate(enemyArr):
    x2 = enemy.enemyX
    y2 = enemy.enemyY
    # s = distance
    s = math.sqrt(math.pow((x1-x2),2)+math.pow((y1-y2),2))
    if s <= 30 :
      return True
      break
  return False

# Game mainoop
running = True
gameover = False

while running:
  # coloring the screen and loading the image
  screen.fill((0,0,0))
  screen.blit(bgImg,(0,0))
  # loading game over screen 
  if gameover:
    # below code is to insure that player is at screen when game over
    screen.blit(playerImg,(playerX,playerY))
    # below code is to insure that enemy is at screen when game over
    for enemy in enemyArr:
      screen.blit(enemy.enemyImg,(enemy.enemyX,enemy.enemyY))
    # bliting game over text
    screen.blit(gameoverText,gameoverRect)
    pygame.display.update()
    continue # to avoid running of below code
    
  # checking events and handeling  them
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False
    # checking whether arrow key is pressed
    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_SPACE:
        if not (len(bulletArr) >= no_of_bullet_can_fired):
          bulletArr.append(Bullet())
          bullet_sound.play()
      if event.key == pygame.K_LEFT:
        pdy = 0
        pdx = -player_speed
      if event.key == pygame.K_RIGHT:
        pdy = 0
        pdx = player_speed
      if event.key == pygame.K_UP:
        pdx = 0
        pdy = -player_speed
      if event.key == pygame.K_DOWN:
        pdx = 0
        pdy = player_speed
      ''' only for mobile purpose '''
      if event.key == pygame.K_o:
        pdx = 0
        pdy = 0
      
    ''' only for computer purpose '''
    # if event.type == pygame.KEYUP:
      # if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
      #   pdx = 0
      # if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
      #   pdy = 0
  # loading the player
  player()
  # moving the enemy using enemy array
  for enemy in enemyArr:
    enemy.enemyLoad()
    if len(enemyArr) < spawning_no_of_enemy:
      enemyArr.append(Enemy())
    if enemy.enemyY >= screen_height:
      enemyArr.pop(0)
      gameover = True
      
  # moving the bullet using bullet array
  for bullet in bulletArr:
    bullet.bulletLoad()
    if bullet.bulletY <=  -16:
      bulletArr.pop(0)
  # checking bullet collison
  isbulletcolide()
  # checking player collison
  gameover = isplayercolide()
  # rendering the score
  scoreRender()
  # rendering the level
  levelRender()
  # updating the display to show changes
  pygame.display.update()

pygame.quit()
quit()