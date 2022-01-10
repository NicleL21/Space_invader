import pygame
import os
import time
import random

pygame.font.init() # Need to initialize font for pygame to run

WHITE = (255, 255, 255)

WIDTH, HEIGHT = 750, 750
WIN = pygame.display.set_mode((WIDTH, HEIGHT)) # use pygame to disply a window
pygame.display.set_caption("Space Shooter Tutorial")

# Load images
RED_SPACE_SHIP = pygame.image.load(os.path.join("assets","pixel_ship_red_small.png"))
BLUE_SPACE_SHIP = pygame.image.load(os.path.join("assets","pixel_ship_blue_small.png"))
GREEN_SPACE_SHIP = pygame.image.load(os.path.join("assets","pixel_ship_green_small.png"))
#From pygame module use imgae.load method load image in the os.path at (folder, name file)
# could use pygame.image.load(assets/pixel_ship_red_small.png))

# Player ship
YELLOW_SPACE_SHIP = pygame.image.load(os.path.join("assets","pixel_ship_yellow.png"))

# Lasers
RED_LASER = pygame.image.load(os.path.join("assets","pixel_laser_red.png"))
BLUE_LASER = pygame.image.load(os.path.join("assets","pixel_laser_blue.png"))
GREEN_LASER = pygame.image.load(os.path.join("assets","pixel_laser_green.png"))
YELLOW_LASER = pygame.image.load(os.path.join("assets","pixel_laser_yellow.png"))

# Background
BG = pygame.image.load(os.path.join("assets", "background-black.png"))
BG2 = pygame.transform.scale(BG, (WIDTH, HEIGHT)) # scale img to dimension

class Ship:
  def __init__(self, x, y, health=100):
    self.x = x
    self.y = y
    self.health = health
    self.ship_img = None
    self.laser_img = None
    self.laseres = []
    self.cool_down_counter = 0 # stop laser from spaming

  #Draw obj
  def draw(self, window):
    window.blit(self.ship_img, (self.x, self.y))
    # pygame.draw.rect(window, (255, 0, 0), (self.x, self.y, 50, 50)) # not be fill-in can put another para as 2 px

  # getter methods
  def get_width(self):
    return self.ship_img.get_width()

  def get_height(self):
    return self.ship_img.get_height()


class Player(Ship): #inherit ship class
  def __init__(self, x, y, health=100):
    super().__init__(x, y, health) # call the instructor of parent class
    self.ship_img = YELLOW_SPACE_SHIP
    self.laser_img = YELLOW_LASER
    self.mask = pygame.mask.from_surface(self.ship_img) # pixel perfect collision
    # make a mask from a surface for checking collision of pixels not hippox( box around an img)
    self.max_health = health # to draw hp bar

class Enemy(Ship):
  # map to get correct img
  COLOR_MAP = {
    "red": (RED_SPACE_SHIP, RED_LASER),
    "blue": (BLUE_SPACE_SHIP, BLUE_LASER),
    "green": (GREEN_SPACE_SHIP, GREEN_LASER)
  }

  def __init__(self, x, y, color, health=100):
    super().__init__(x, y, health)
    self.ship_img, self.laser_img = self.COLOR_MAP[color]
    self.mask = pygame.mask.from_surface(self.ship_img)

  # to move the enemy ship down the screen
  def move(self, vel):
    self.y += vel

def main():
  run = True
  lost = False
  lost_count = 0
  FPS = 60 # fast/slow the game run: 60 frames/sec -> too low: check collision, frame every sec
  main_font = pygame.font.SysFont("comicsans", 50) # name and size of font
  lost_font = pygame.font.SysFont("comicsans", 60)
  clock = pygame.time.Clock()

  #var set for player
  level = 0
  lives = 5
  player_vel = 5
  player = Player(300, 650)

  #var set for enemies
  enemies = []
  wave_length = 5
  enemies_vel = 1

  #func inside func, only call when it in outter func and get variables inside
    #the outter func

  # Handle all the drawing inside the game
  def redraw_window():
    # draw background
    WIN.blit(BG2, (0, 0)) # on the WIN surface blit img (transfer to surface) and set at (0,0)

    # draw text
    lives_label = main_font.render(f"Lives: {lives}", 1, WHITE) #f-string embed variabel into braclet
    level_label = main_font.render(f"Level: {level}", 1, WHITE)
    WIN.blit(lives_label, (10, 10))
    WIN.blit(level_label, (WIDTH - level_label.get_width() - 10, 10))

    # draw enemy
    for enemy in enemies:
      enemy.draw(WIN)

    # draw ship
    player.draw(WIN)

    if lost:
      lost_label = lost_font.render("You lost!", 1, WHITE)
      WIN.blit(lost_label, (WIDTH / 2 - lost_label.get_width() / 2, 350))

    pygame.display.update() # refresh display to have updated version

  '''
  in pygame, there exist surfaces which can then be blit (place imgae ontop)
  everytime rerun can redraw everythhing the image and update
  '''

  while run:
    clock.tick(FPS) # tick the clock base on FPS -> keep the game run at constant speed for any device
    redraw_window()

    if lives <= 0 or player.health <= 0:
      lost = True
      lost_count += 1

    if lost:
      if lost_count > FPS * 3: # show the message for 3 sec
        run = False
      else:
        continue

    if len(enemies) == 0:
      level += 1
      wave_length += 5
      for i in range(wave_length):
        enemy = Enemy(random.randrange(50, WIDTH - 100), random.randrange(-1500, -100), random.choice(["red", "blue", "green"])) #choose random 1 ele
        enemies.append(enemy)

    #Check for event in the game
    for event in pygame.event.get():
      if event.type == pygame.QUIT: #Press the quit button to stop game
        quit()

    # track keys is pressed with dictionary that key is press or not
    keys = pygame.key.get_pressed()
    #K short for key, K_<keyname>
    if keys[pygame.K_LEFT] and player.x - player_vel > 0: #left
      player.x -= player_vel # the ship move velc px to the left, and depend on the FPS
    if keys[pygame.K_RIGHT] and player.x + player_vel + player.get_width() < WIDTH: #right
      player.x += player_vel
    if keys[pygame.K_UP] and player.y - player_vel > 0: #up
      player.y -= player_vel
    if keys[pygame.K_DOWN] and player.y + player_vel + player.get_height() < HEIGHT: #down
      player.y += player_vel

    for enemy in enemies:
      enemy.move(enemies_vel)
      if enemy.y + enemy.get_height() > HEIGHT:
        lives -= 1
        enemies.remove(enemy)

main()