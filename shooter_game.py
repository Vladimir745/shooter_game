#Создай собственный Шутер!
from pygame import *
from random import *                                        
from time import time as timer
font.init()
font1 = font.SysFont('Arial', 36)
font2 = font.SysFont('Arial', 36)
font = font.SysFont('Arial', 70)
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
lost_ship = mixer.Sound('kick.ogg')
fire = mixer.Sound('fire.ogg')
lose = font.render('YOU LOSE!', True, (255, 0, 0))
win = font.render('YOU WIN!', True,(0, 255, 0))
reload = font.render('wait, reload...', 1 ,(255, 0, 0))
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
class Player(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys_pressed[K_RIGHT] and self.rect.x < width - 80:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 10, 20, -15)
        bullets.add(bullet)


class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > height:
            lost_ship
            self.rect.y = 0
            self.rect.x = randint(80, width - 80)
            lost += 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()
        

lost = 0
score = 0
window = display.set_mode((700, 500))
display.set_caption('pygame window')
galaxy = transform.scale(image.load('galaxy.jpg'), (700, 500))
width = 700
height = 500

rocket = Player('rocket.png', 5, height - 100, 80, 100, 10)
bullets = sprite.Group()
asteroids = sprite.Group()
for i in range(1, 3):
    asteroid = Enemy('asteroid.png', randint(80, width - 80), -40, 80, 50, randint(1, 7))
    asteroids.add(asteroid)
monsters = sprite.Group()
for i in range(5):
    monster = Enemy('ufo.png', randint(80, width - 80), -40, 80, 50, randint(1, 5))
    monsters.add(monster)

finish = False
run = True

num_fire = 0
reload_time = False

while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 5 and reload_time == False:
                    num_fire += 1
                    rocket.fire()
                    fire.play()
                if num_fire >= 5 and reload_time == False:
                    last_time = timer()
                    reload_time = True
    if not finish:
        window.blit(galaxy, (0, 0))
        text_lose = font1.render('Пропущено: ' + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 40))
        text_win = font2.render('Счет: ' + str(score), 1, (255, 255, 255))
        window.blit(text_win, (10, 10))
        rocket.update()
        monsters.update()
        asteroids.update()
        bullets.update()
        rocket.reset()
        monsters.draw(window)
        asteroids.draw(window)
        bullets.draw(window)
        if reload_time == True:
            now_time = timer()
            if now_time - last_time < 3:
                window.blit(reload, (200, 450))
            else:
                num_fire = 0
                reload_time = False
        collide = sprite.groupcollide(bullets, monsters, True, True)
        for i in collide:
            score += 1
            monster = Enemy('ufo.png', randint(80, width - 80), -40, 80, 50, randint(1, 5))
            monsters.add(monster)
        if sprite.spritecollide(rocket, monsters, False) or lost >= 3:
            finish = True
            window.blit(lose, (200, 200))
        if sprite.spritecollide(rocket, asteroids, False):
            finish = True
            window.blit(lose, (200, 200))
        if score == 15:
            finish = True
            window.blit(win, (200, 200))
        display.update()
    time.delay(50)