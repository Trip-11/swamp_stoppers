# Sprite classes for platform game
from operator import truediv
import pygame as pg
from settings import *
vec = pg.math.Vector2
import random


class Player(pg.sprite.Sprite):
    def __init__(self, game):
        self._layer = PLAYER_LAYER
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.width = 60
        self.height = 30
        self.idle_img = []
        self.run_img_r = []
        self.run_img_l = []
        self.jump_img_r = []
        self.jump_img_l=[]
        self.load_images()
        self.image = self.idle_img[0]

        self.running = False
        # self.image = pg.Surface((30, 40))
        # self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.center = (100, HEIGHT / 2)
        self.pos = vec(100, HEIGHT / 2)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.last_update = 0
        self.current_frame = 0
        self.jumping=False

    def animate(self):
        now=pg.time.get_ticks()
        if int(self.vel.x) != 0:
            self.running = True
        else:
            self.running = False
            self.jumping = False
        if not self.running and not self.jumping:
            if now-self.last_update>350:
                self.last_update=now
                self.current_frame = (self.current_frame+1)%len(self.idle_img)
                self.image = self.idle_img[self.current_frame]
                self.rect = self.image.get_rect()
        if self.running and not self.jumping:

            if now - self.last_update > 150:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.run_img_r)
                if self.vel.x>0:
                    self.vel.y -= 6
                    self.image = self.run_img_r[self.current_frame]
                else:
                    self.vel.y -= 6
                    self.image = self.run_img_l[self.current_frame]



    def load_images(self):
        for i in range(1,4):
            filename = "frog{}.png".format(i)
            img=pg.image.load(filename)
            #img = pg.transform.scale(img,(self.width,self.height))
            self.idle_img.append(img)
        for i in range(1, 5):
            filename = "frogjump{}.png".format(i)
            img = pg.image.load(filename)
            # img = pg.transform.scale(img,(self.width,self.height))
            self.run_img_r.append(img)
        for frame in self.run_img_r:
            self.run_img_l.append(pg.transform.flip(frame,True,False))
        for i in range(1, 5):
            filename = "frogjump{}.png".format(i)
            img = pg.image.load(filename)
            # img = pg.transform.scale(img,(self.width,self.height))
            self.jump_img_r.append(img)
        for frame in self.run_img_r:
            self.jump_img_l.append(pg.transform.flip(frame,True,False))
    def jump(self):
        # jump only if standing on a platform
        self.rect.x += 1
        hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.x -= 1
        if hits:
            self.vel.y = -20
            now = pg.time.get_ticks()
            if now - self.last_update > 50:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.run_img_r)
                if self.vel.x > 0:
                    self.vel.y -= 6
                    self.image = self.jump_img_r[self.current_frame]
                else:
                    self.vel.y -= 6
                    self.image = self.jump_img_l[self.current_frame]
        # self.jumpimg = False
    def update(self):
        self.animate()
        self.acc = vec(0, PLAYER_GRAV)
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.acc.x = -PLAYER_ACC
        if keys[pg.K_RIGHT]:
            self.acc.x = PLAYER_ACC

        # apply friction
        self.acc.x += self.vel.x * PLAYER_FRICTION
        # equations of motion
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        # wrap around the sides of the screen
        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH

        self.rect.midbottom = self.pos

class Platform(pg.sprite.Sprite):
    def __init__(self, game,x, y, w, h):
        self._layer = PLATFORM_LAYER
        self.groups = game.all_sprites,game.platforms
        self.game=game
        self.groups = game.all_sprites, game.platforms
        pg.sprite.Sprite.__init__(self, self.groups)
        # pg.sprite.Sprite.__init__(self)
        # self.image = pg.Surface((w, h))
        # self.image.fill(GREEN)
        # self.rect = self.image.get_rect()

        self.plat_img = []
        self.side = random.randint(1, 2)
        #print(self.side)
        if self.side == 1:
            x = random.randrange(0, WIDTH // 4)

        else:
            x = random.randrange(3 * WIDTH // 4, WIDTH)
            print('2')
        self.load_images()
        print(self.side)

        self.image = random.choice(self.plat_img)
        self.rect = self.image.get_rect()


        self.rect.centerx = x
        self.rect.y = y
        # self.width = 25
        # self.height = 10
        if random.randrange(100)<POW_SPAWN_PCT:
            Pow(self.game,self)
    def load_images(self):

        if self.side == 1:
            for i in range(1, 4):
                filename = "platform{}.png".format(i)
                img = pg.image.load(filename)
                if i ==2 or i == 3:
                    img = pg.transform.flip(img, True, False)


                img = pg.transform.scale(img,(150,50))
                self.plat_img.append(img)
        else:
            for i in range(1, 4):
                filename = "platform{}.png".format(i)
                img = pg.image.load(filename)
                if i == 1 or i == 4:
                    img = pg.transform.flip(img, True, False)

                img = pg.transform.scale(img, (150, 50))
                self.plat_img.append(img)




class Cloud(pg.sprite.Sprite):
    def __init__(self, game):
        self._layer = CLOUD_LAYER
        self.groups = game.all_sprites, game.clouds
        pg.sprite.Sprite.__init__(self,self.groups)
        self.game=game
        self.image = random.choice(self.game.cloud_images)
        self.image.set_colorkey(BLACK)
        # self.image = pg.Surface((w, h))
        # self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        scale = random.randrange(50,101) / 100
        self.image= pg.transform.scale(self.image,(int(self.rect.width*scale),int(self.rect.height*scale)))
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-500,-50)
    def update(self):
      if self.rect.top> HEIGHT*2:
        self.kill()


class Pow(pg.sprite.Sprite):
    def __init__(self, game, plat):
        self.groups = game.all_sprites, game.powerups
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.plat = plat
        self.type = random.choice(['boost'])
        self.image = pg.image.load("power.PNG")
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = self.plat.rect.centerx
        self.rect.bottom = self.plat.rect.top - 5

    def update(self):
        self.rect.bottom = self.plat.rect.top - 5
        if not self.game.platforms.has(self.plat):
            self.kill()


