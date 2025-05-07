import pygame as pg
import random
from settings import *
from sprites import *

class Game:
    def __init__(self):
        # initialize game window, etc
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True
        self.font_name = pg.font.match_font(FONT_NAME)

    def new(self):
        self.score=0
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.platforms = pg.sprite.Group()
        self.powerups = pg.sprite.Group()
        self.clouds = pg.sprite.Group()
        self.player = Player(self)
        self.all_sprites.add(self.player)
        for plat in PLATFORM_LIST:
            Platform(self,*plat)
        self.cloud_images = []
        for i in range(1, 4):
            filename = "cloud{}.png".format(i)
            img = pg.image.load(filename)
            self.cloud_images.append(img)
        for i  in range (8):
                c=Cloud(self)
                c.rect.y+=500
        self.run()
    def run(self):
        # Game Loop
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def update(self):
        # Game Loop - Update
        self.all_sprites.update()
        # check if player hits a platform - only if falling
        if self.player.vel.y > 0:
            hits = pg.sprite.spritecollide(self.player, self.platforms, False)
            if hits:
                self.player.pos.y = hits[0].rect.top
                self.player.vel.y = 0
        #if player reaches 1/4 of screen
        if self.player.rect.top<= HEIGHT/4:
            if random.randrange(100)<15:
                Cloud(self)
            self.player.pos.y += abs(self.player.vel.y)
            for cloud in self.clouds:
                    cloud.rect.y += abs(self.player.vel.y)
            for plat in self.platforms:
                plat.rect.y += abs(self.player.vel.y)
                if plat.rect.top >= HEIGHT:
                    plat.kill()
                    self.score += 10
        #spawn new platforms average of 5
        while len(self.platforms) < 6:
            width=random.randrange(50,101)
            x = random.randrange(0,WIDTH-width)
            y = random.randrange(-75, -30)
            p = Platform(self,x,y,width,20)
            self.platforms.add(p)
            self.all_sprites.add(p)
        #die
        if self.player.rect.top>HEIGHT:
            for sprite in self.all_sprites:
                sprite.rect.y -=max(self.player.vel.y,10)
                if sprite.rect.bottom <0:
                    sprite.kill()
        if len(self.platforms) == 0:
            self.playing = False
        pow_hits = pg.sprite.spritecollide(self.player,self.powerups, True)
        for pow in pow_hits:
            if pow.type == 'boost':
                self.player.vel.y = -BOOST_POWER
                self.player.jumping=False




    def events(self):
        # Game Loop - events
        for event in pg.event.get():
            # check for closing window
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:

                    self.jumping = True
                    self.player.jump()



    def draw(self):
        # Game Loop - draw
        self.screen.fill(GREEN)
        self.all_sprites.draw(self.screen)
        self.draw_text(self.screen, str(self.score),22, WIDTH/2,15,WHITE)
        # *after* drawing everything, flip the display
        pg.display.flip()

    def show_start_screen(self):
        # game splash/start screen
        # game splash/start screen
        self.screen.fill(BLUE)
        time = pg.time.get_ticks()
        # self.draw_text(self.screen, 'Platform Game', 64, WIDTH / 2, HEIGHT / 4, WHITE)
        self.draw_text(self.screen, 'Arrow Keys to Move', 22, WIDTH / 2, HEIGHT / 2, WHITE)
        self.draw_text(self.screen, 'Press A to Begin', 18, WIDTH / 2, HEIGHT * 3 / 4, RED)
        for i in range(WIDTH//2+100):
            self.screen.fill(BLUE)
            self.draw_text(self.screen, 'Swamp Stompers', 64, -100+i, HEIGHT / 4, WHITE)
            pg.display.flip()
        pg.display.flip()
        waiting = True
        while waiting:

            color = random.choice([RED, WHITE])
            self.draw_text(self.screen, 'Press A to Begin', 18, WIDTH / 2, HEIGHT * 3 / 4, color)

            pg.display.flip()
            self.clock.tick(FPS)
            for event in pg.event.get():
                keystate = pg.key.get_pressed()
                if event.type == pg.QUIT:
                    pg.quit()
                if event.type == pg.KEYDOWN:
                    if keystate[pg.K_a]:
                        waiting = False
    def show_go_screen(self):
        # game over/continue
        pass


    def draw_text(self, surf, text, size, x, y, Color):
        self.font_name = pg.font.match_font('arial')
        font = pg.font.Font(self.font_name, size)
        text_surface = font.render(text, True, Color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        surf.blit(text_surface, text_rect)
        
g = Game()
g.show_start_screen()
while g.running:
    g.new()
    g.show_go_screen()

pg.quit()



#trees on either side
#less branches
#jump power if held longer
#background
#diff powers
#score
#spawn on branch on side