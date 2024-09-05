from random import choice
from typing import Any
from pygame import *
import pygame_menu

init()
font.init()
font1 = font.SysFont("impact", 151, )
font2 = font.SysFont("impact", 30, )
game_over_text = font1.render("GAME_OVER", True, (150, 0, 0))
score_text = font2.render("Score 0", False, (255,255,255))
hp_text = font2.render("HP 200", False, (255,0,0))
win_text = font1.render("YOU WIN", False, (0,255,0))
mixer.init()
mixer.music.load('Тема королевства.mp3')
mixer.music.play()
mixer.music.set_volume(0.2)
MAP_WIDTH, MAP_HEIGHT =25, 20
TILESIZE = 35

WIDTH, HEIGHT = MAP_WIDTH*TILESIZE, MAP_HEIGHT*TILESIZE

window  = display.set_mode((WIDTH,HEIGHT))
FPS = 60
clock = time.Clock()

#bg = image.load('parallax-mountain-animX1.gif')
#bg = transform.scale(bg, (WIDTH,HEIGHT))
axe2_img = image.load("image/broad_axe.png")
player_img = image.load("image/human_male.png")
wall_img = image.load("image/catacombs_8.png")
coin_img = image.load("image/gold_pile_1.png")
orc_img = image.load("image/orc_new.png")
orc2_img = image.load("image/orc_warrior_new.png")
ladder_img = image.load("image/pixil-frame-0.png")
floor_img = image.load("image/brick_brown-vines_1.png")
magma_img = image.load("image/lava_3.png")
banner_img = image.load("image/banner_1.png")
ret2_img = image.load("image/return_zot_old.png")
orc5_img = image.load("image/orc_1.png")
torch_img = image.load("image/torch_1.png")
barrier_img = image.load("image/permarock_clear_red_0.png")
sand_img = image.load("image/limestone_0.png")
axe_img = image.load("image/axe.png")
all_sprites = sprite.Group()

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
        self.axe = False
        self.hp = 200
        self.speed = 3
        self.ground = False
        self.jump_speed = 35
        self.gravity = 0.5
        self.y_speed = 0
        self.score = 0
        self.hit_timer = 0
        self.left_axe = axe2_img
        self.right_axe = transform.flip(axe2_img, True,False)
        self.axe_img = self.right_axe
    def update(self):
        
        
        self.old_pos = self.rect.x, self.rect.y
        key_pressed = key.get_pressed()
        if key_pressed[K_a] and self.rect.x > 0:
            self.image = self.leftimage 
            self.axe_img = self.left_axe
            self.rect.x -= self.speed
        if key_pressed[K_d] and self.rect.right < WIDTH:
            self.image = self.rightimage
            self.axe_img = self.right_axe
            self.rect.x += self.speed
        if key_pressed[K_SPACE] and self.ground:
            self.ground = False
            self.y_speed = 0
            self.rect.y -=self.jump_speed
        self.check_collision()
        if self.axe:
            window.blit(self.axe_img,(self.rect.x, self.rect.y))
    def attack(self):
        player_collide = sprite.spritecollide(self, enemys, False, sprite.collide_mask)
        for e in player_collide:
            if e.attack_timer == 0:
                e.attack_timer = time.get_ticks()
                e.hp-=25
                if e.hp <= 0:
                    e.kill()
            else:
                if time.get_ticks() - e.attack_timer> 1000:
                    e.attack_timer = 0

    def check_collision(self):   
        global hp_text,score_text

        key_pressed = key.get_pressed()
        
        enemy_collide = sprite.spritecollide(self, enemys, False, sprite.collide_mask)
        for e in enemy_collide:
            if e.attack_timer == 0:
                if self.hit_timer == 0:
                    self.hp -=20
                    self.hit_timer = time.get_ticks()
                    hp_text = font2.render(f"HP {player.hp}", False, (255,0,0))
                else:
                    if time.get_ticks() - self.hit_timer> 3000:
                        self.hit_timer = 0

        if len(enemys) ==0:
            for barrier in barriers:
                barrier.kill()

        wall_collide = sprite.spritecollide(self, walls, False) 
        if len(wall_collide) > 0:
            self.rect.x , self.rect.y = self.old_pos
        wall_collide = sprite.spritecollide(self, ground, False)
        if len(wall_collide) == 0:
            self.ground = False
        for wall in wall_collide:
            if wall.rect.y > self.rect.y:
                self.ground = True
                self.y_speed = 0
                self.rect.bottom = wall.rect.y 
                break
            else:
                self.ground = False 
                self.rect.x, self.rect.y = self.old_pos

        
 
        ladder_collide = sprite.spritecollide(self, ladder, False)
        if len(ladder_collide) > 0:
            if key_pressed [K_w]:
                self.rect.y -= self.speed

        if not self.ground and not len(ladder_collide) > 0:
            self.y_speed += self.gravity
            self.rect.y += self.y_speed

    
        coin_collide = sprite.spritecollide(self, coins,True, sprite.collide_mask)
        if len(coin_collide) > 0:
            self.score +=1
            score_text = font2.render(f"Score {self.score}", False, (255,255,255))

        axe_collide = sprite.spritecollide(self, axe,True, sprite.collide_mask)
        if len(axe_collide) > 0:
            self.axe = True

        magma_collide = sprite.spritecollide(self, fake,False, sprite.collide_mask)
        if len(magma_collide) > 0:
            if self.hit_timer == 0:
                self.hp -=10
                self.hit_timer = time.get_ticks()
                hp_text = font2.render(f"HP {player.hp}", False, (255,0,0))
            else:
                if time.get_ticks() - self.hit_timer> 3000:
                    self.hit_timer = 0   
 
class Enemy(Sprite):
    def __init__(self, sprite_img, width, height, x, y):
        super().__init__(sprite_img, width, height, x, y)
        self.damage = 20
        self.speed = 0
        self.hp = 50
        self.leftimage = self.image
        self.rightimage = transform.flip(self.image,True,False)
        self.dir_list = ('right', 'left',)
        self.dir = choice(self.dir_list)
        self.attack_timer = 0
    def update(self):
        old_pos = self.rect.x, self.rect.y
        if self.dir == "right":
            self.rect.x +=self.speed
            self.image = self.rightimage
        if self.dir == "left":
            self.rect.x -=self.speed
            self.image = self.leftimage

        collide_list = sprite.spritecollide(self, walls, False, sprite.collide_mask)
        if len(collide_list) > 0:
            self.rect.x, self.rect.y = old_pos
            self.dir = choice(self.dir_list)
        
        if player.rect.y > self.rect.y-20 and player.rect.y < self.rect.y + 20:
            self.speed = 2
            if player.rect.x < self.rect.x:
                self.dir = "left"
            else:
                self.dir = "right"


player = Player(player_img,30, 30, 300, 300)
walls = sprite.Group()
enemys = sprite.Group()
ladder = sprite.Group()
ground = sprite.Group()
fake = sprite.Group()
sand = sprite.Group()
axe = sprite.Group()
coins = sprite.Group()
barriers = sprite.Group()
superdoor = sprite.Group()

with open("map1.txt", "r",) as f:
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
                coins.add(Sprite(coin_img, 30 ,30, x, y))
            if symbol == "e":
                enemys.add(Enemy(orc_img, TILESIZE-5, TILESIZE-5, x, y))
            if symbol == "l":
                ladder.add(Sprite(ladder_img, TILESIZE, TILESIZE, x, y))
            if symbol == "f":
                ground.add(Sprite(floor_img, TILESIZE, TILESIZE, x, y))
            if symbol == "m":
                magma = Sprite(magma_img, TILESIZE, TILESIZE, x, y)
                fake.add(magma)
                ground.add(magma)
            if symbol == "b":
                Sprite(banner_img, TILESIZE, TILESIZE, x, y)
            if symbol == "r":
                superdoor.add(Sprite(ret2_img, 70, 70, x, y))
                # superdoor.add(ret2_img)
            if symbol == "g":
                ground.add(Sprite(orc5_img,TILESIZE, TILESIZE, x, y))
            if symbol == "t":
                Sprite(torch_img, TILESIZE, TILESIZE, x, y)
            if symbol == "v":
                barrier = Sprite(barrier_img, TILESIZE, TILESIZE, x, y)
                walls.add(barrier)
                barriers.add(barrier)
            if symbol == "s":
                sand.add(Sprite(sand_img, TILESIZE, TILESIZE, x, y))
            if symbol == "a":
                axe.add(Sprite(axe_img, TILESIZE, TILESIZE, x, y))                  
            x +=TILESIZE
        y +=TILESIZE
        x = 0        





run = True
finish = False



def set_difficulty(selected, value):
    """
    Set the difficulty of the game.
    """
    print(f'Set difficulty to {selected[0]} ({value})')

def start_the_game():
    # Do the job here !
    global run
    run = True
    menu.disable()

#завантажуємо картинку
# myimage = pygame_menu.baseimage.BaseImage(
    # image_path='infinite_starts.jpg',
    # drawing_mode=pygame_menu.baseimage.IMAGE_MODE_REPEAT_XY,
# )
#створюємо власну тему - копію стандартної
mytheme = pygame_menu.themes.THEME_DARK.copy()
# колір верхньої панелі (останній параметр - 0 робить її прозорою)
mytheme.title_background_color=(255, 255, 255, 0) 
#задаємо картинку для фону
# mytheme.background_color = myimage
menu = pygame_menu.Menu('dyno(1.1)', WIDTH, HEIGHT,
                       theme=mytheme)   

user_name = menu.add.text_input("Ім'я :", default='Анонім')
menu.add.button('Play', start_the_game)
menu.add.button('Quit', pygame_menu.events.EXIT)
menu.mainloop(window)


while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        if e.type == KEYDOWN:
            if e.key == K_f:
                player.attack()
  #  window.blit(bg,(0,0))
    window.fill(((0,0,0)))
    if player.hp <= 0:
        finish = True

    door_collide = sprite.spritecollide(player, superdoor,False, sprite.collide_mask)
    if len(door_collide) > 0:
        finish = True
        game_over_text = font1.render("YOU WIN", True, (150,0,0))

    all_sprites.draw(window)
    if not finish:
        all_sprites.update()
    if finish:
        window.blit(game_over_text, (75, 250))
    
    window.blit(score_text, (10, 5))
    window.blit(hp_text, (20, 35))
    # window.blit(win_text, (75, 250))
    display.update()
    clock.tick(FPS)




















































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































   




