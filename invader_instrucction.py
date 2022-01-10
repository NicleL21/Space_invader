import pygame
import os
import random

from pygame import image

pygame.font.init() # Need to initialize font for pygame to run

WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

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

class Laser:
  def __init__(self, x, y, img):
    self.x = x
    self.y = y
    self.img = img
    self.mask = pygame.mask.from_surface(self.img)

  def draw(self):
    WIN.blit(self.img, (self.x, self.y))

  # to move the lazer down the screen
  def move(self, vel):
    self.y += vel

  def off_screen(self, height):
    return not(self.y <= height and self.y >= 0)

  # to check if the laser collide with obj
  def collision(self, obj):
    return collide(self, obj)

class Ship:
  COOLDOWN = 30

  def __init__(self, x, y, health=100):
    self.x = x
    self.y = y
    self.health = health
    self.ship_img = None
    self.laser_img = None
    self.lasers = [] #list of lazer obj
    self.cool_down_counter = 0 # stop laser from spaming

  # increase cooldown counter
  def cooldown(self):
    if self.cool_down_counter >= self.COOLDOWN:
      self.cool_down_counter = 0
    elif self.cool_down_counter > 0:
      self.cool_down_counter += 1

  # Shooting laserS
  def shoot(self):
    if self.cool_down_counter == 0:
      laser = Laser(self.x, self.y, self.laser_img)
      self.lasers.append(laser)
      self.cool_down_counter = 1

  #mover the laser
  def move_lasers(self, vel, obj):
    self.cooldown()
    for laser in self.lasers:
      laser.move(vel)
      if laser.off_screen(HEIGHT):
        self.lasers.remove(laser)
      elif laser.collision(obj):
        obj.health -= 10
        self.lasers.remove(laser)


  #Draw obj
  def draw(self, window):
    window.blit(self.ship_img, (self.x, self.y))
    # pygame.draw.rect(window, (255, 0, 0), (self.x, self.y, 50, 50)) # not be fill-in can put another para as 2 px
    for laser in self.lasers:
      laser.draw()

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

  # override for player
  def move_lasers(self, vel, objs):
    self.cooldown()
    for laser in self.lasers:
      laser.move(vel)
      if laser.off_screen(HEIGHT):
        self.lasers.remove(laser)
      else:
        for obj in objs:
          if laser.collision(obj):
            objs.remove(obj)
            if laser in self.lasers:
              self.lasers.remove(laser)

  def draw(self, window):
    super().draw(window)
    self.healthbar()

  # display player health bar
  def healthbar(self):
    y_coordinate = self.y + self.ship_img.get_height() + 10
    red_width_bar = self.ship_img.get_width()
    green_width_bar = self.ship_img.get_width() * (self.health/ self.max_health)
    pygame.draw.rect(WIN, RED, (self.x, y_coordinate, red_width_bar, 10))
    pygame.draw.rect(WIN, GREEN, (self.x, y_coordinate, green_width_bar, 10))

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

  # Shooting laserS
  def shoot(self):
    if self.cool_down_counter == 0:
      laser = Laser(self.x - 15, self.y, self.laser_img)
      self.lasers.append(laser)
      self.cool_down_counter = 1

# Check the overlap of the pixels
def collide(obj1, obj2):
  offset_x = obj2.x - obj1.x #(x,y) of top left corner
  offset_y = obj2.y - obj1.y
  # overlap the pixels when use mask
  return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None

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
  laser_vel = 5
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

    # check for losing game
    if lives <= 0 or player.health <= 0:
      lost = True
      lost_count += 1

    # display mess and stop game
    if lost:
      if lost_count > FPS * 3: # show the message for 3 sec
        run = False
      else:
        continue

    # Level up behavior
    if len(enemies) == 0:
      level += 1
      wave_length += 5
      laser_vel += 1
      for i in range(wave_length):
        color = random.choice(["red", "blue", "green"])
        x = random.randrange(50, WIDTH - 100)
        y = random.randrange(-1500, -100)
        enemy = Enemy(x, y, color) #choose random 1 ele
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
    if keys[pygame.K_DOWN] and player.y + player_vel + player.get_height() + 15 < HEIGHT: #down
      player.y += player_vel
    if keys[pygame.K_SPACE]:
      player.shoot()

    for enemy in enemies:
      enemy.move(enemies_vel)
      enemy.move_lasers(laser_vel, player)

      # check for ship collision
      if collide(enemy, player):
        player.health -= 10
        enemies.remove(enemy)

      if random.randrange(0, 2 * 60) == 1: # probability 50% of shoot in sec -> 60 frame
        enemy.shoot()

      # if the enemy reach the end of window
      if enemy.y + enemy.get_height() > HEIGHT:
        lives -= 1
        enemies.remove(enemy)

    player.move_lasers(-laser_vel, enemies)

def main_menu():
  title_font = pygame.font.SysFont("comicsans", 50)
  run = True
  while run:
    WIN.blit(BG2, (0, 0))
    title_label = title_font.render("Press the mouse to begin...", 1, WHITE)
    WIN.blit(title_label, (WIDTH / 2 - title_label.get_width()/ 2, 350))
    pygame.display.update()

    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        run = False
      if event.type == pygame.MOUSEBUTTONDOWN:
        main()

  pygame.quit()

main_menu()