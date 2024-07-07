from random import choice
from typing import Any
from pygame import *

init()
font.init()
font1 = font.SysFont("impact", 150, )
game_over_text = font1.render("GAME_OVER", True, (150, 0, 0))
#mixer.init()
#mixer.music.load('')
#mixer.music.play()
#mixer.music.set_volume(0.2)
MAP_WIDTH, MAP_HEIGHT =25, 20
TILESIZE = 35

WIDTH, HEIGHT = MAP_WIDTH*TILESIZE, MAP_HEIGHT*TILESIZE

window  = display.set_mode((WIDTH,HEIGHT))
FPS = 60
clock = time.Clock()

#bg = image.load('parallax-mountain-animX1.gif')
#bg = transform.scale(bg, (WIDTH,HEIGHT))

player_img = image.load("image/human_male.png")
wall_img = image.load("image/catacombs_8.png")
all_sprites = sprite.Group()
coin_img = image.load("image/gold_pile_1.png")
orc_img = image.load("image/orc_new.png")
orc2_img = image.load("image/orc_warrior_new.png")
ladder_img = image.load("image/pixil-frame-0.png")
floor_img = image.load("image/brick_brown-vines_1.png")
magma_img = image.load("image/lava_3.png")
banner_img = image.load("image/banner_1.png")
ret2_img = image.load("image/return_zot_old.png")
class Sprite(sprite.Sprite):
    def __init__(self, sprite_img, width, height, x , y ):
        super().__init__()
        self.image = transform.scale(sprite_img, (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.leftimage = self.image
        self.rightimage = transform.flip(self.image,True,False)
        self.mask = mask.from_surface(self.image)
        all_sprites.add(self)

class Player(Sprite):
    def __init__(self, sprite_img, width, height, x, y):
        super().__init__(sprite_img, width, height, x, y)
        self.hp = 100
        self.speed = 4

    def update(self):
        old_pos = self.rect.x, self.rect.y
        key_pressed = key.get_pressed()
        if key_pressed[K_w] and self.rect.y > 0:
            self.rect.y -= self.speed 
        if key_pressed[K_s] and self.rect.bottom < HEIGHT:
            self.rect.y += self.speed
        if key_pressed[K_a] and self.rect.x > 0:
            self.image = self.rightimage
            self.rect.x -= self.speed
        if key_pressed[K_d] and self.rect.right < WIDTH:
            self.image = self.leftimage
            self.rect.x += self.speed

            
        enemy_collide = sprite.spritecollide(self, enemys, False, sprite.collide_mask)
        if len(enemy_collide) > 0:
            self.hp -= 100



class Enemy(Sprite):
    def __init__(self, sprite_img, width, height, x, y):
        super().__init__(sprite_img, width, height, x, y)
        self.damage = 100
        self.speed = 2
        self.leftimage = self.image
        self.rightimage = transform.flip(self.image,True,False)
        self.dir_list = ('right', 'left',)
        self.dir = choice(self.dir_list)

    def update(self):
        old_pos = self.rect.x, self.rect.y
        if self.dir == "right":
            self.rect.x +=self.speed
            self.image = self.leftimage
        if self.dir == "left":
            self.rect.x -=self.speed
            self.image = self.rightimage

        #collide_list = sprite.spritecollide(self, walls, False, sprite.collide_mask)
        #if len(collide_list) > 0:
          #  self.rect.x, self.rect.y = old_pos
          #  self.dir = choice(self.dir_list)


player = Player(player_img,30, 30, 300, 300)
walls = sprite.Group()
enemys = sprite.Group()


with open("map1.txt", "r") as f:
    map = f.readlines()
    x = 0
    y = 0
    for line in map:
        for symbol in line:
            if symbol == "w":
                walls.add(Sprite(wall_img, TILESIZE, TILESIZE, x, y))
            if symbol == "p":
                player.rect.x = x
                player.rect.y = y
            if symbol == "c":
                treasure = Sprite(coin_img, 30 ,30, x, y)
            if symbol == "e":
                enemys.add(Enemy(orc_img, TILESIZE-5, TILESIZE-5, x, y))
            if symbol == "l":
                Sprite(ladder_img, TILESIZE, TILESIZE, x, y)
            if symbol == "f":
                Sprite(floor_img, TILESIZE, TILESIZE, x, y)
            if symbol == "m":
                Sprite(magma_img, TILESIZE, TILESIZE, x, y)
            if symbol == "b":
                Sprite(banner_img, TILESIZE, TILESIZE, x, y)
            if symbol == "r":
                Sprite(ret2_img, TILESIZE, TILESIZE, x, y)
            x +=TILESIZE
        y +=TILESIZE
        x = 0        





run = True
finish = False


while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
  #  window.blit(bg,(0,0))
    window.fill(((0,0,0)))
    if player.hp <= 0:
        finish = True
    all_sprites.draw(window)
    if not finish:
        all_sprites.update()
    if finish:
        window.blit(game_over_text, (75, 250))
    display.update()
    clock.tick(FPS)