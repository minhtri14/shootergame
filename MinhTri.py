#Create your own shooter
from pygame import *
from random import randint
class GameSprite(sprite.Sprite):
    def __init__(self, filename, x, y, width, height, speed=0):
        super().__init__()
        self.image = image.load(filename)
        self.image = transform.scale(self.image, (width, height))
        self.rect = Rect(x, y, width, height)
        self.speed = speed
    def draw(self, surface):
        surface.blit(self.image, (self.rect.x, self.rect.y))
    def is_touching(self, other_sprite):
        return sprite.collide_rect(self, other_sprite)
class Player(GameSprite):
    def update(self):
        Key = key.get_pressed()
        if Key[K_a]:
            self.rect.x -= self.speed 
        if Key[K_d]:
            self.rect.x += self.speed
    def shoot(self):
        b = Bullet("cannon bullets 2.jpg", x=0, y=0, width=15, height=20, speed=6)
        b.rect.centerx = self.rect.centerx
        b.rect.bottom = self.rect.top
        bullets.add(b) 
class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed   
        if self.rect.top > _HEIGHT:
            self.rect.bottom = 0
            self.rect.x = randint(0, _WIDTH-self.rect.width)

class Asteroid(GameSprite):
    def update(self):
        self.rect.y += self.speed   
        if self.rect.top > _HEIGHT:
            self.rect.bottom = 0
            self.rect.x = randint(0, _WIDTH-self.rect.width)
class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.bottom < 0:
            self.kill()
_WIDTH = 800
_HEIGHT = 640

window = display.set_mode((_WIDTH, _HEIGHT))
clock = time.Clock()

background = GameSprite("sea background with sand.jpg", 0, 0, _WIDTH, _HEIGHT)
player = Player("cannon 2d have cut.jpg", _WIDTH/2, _HEIGHT-95, 60, 80, speed = 15)
game_over = GameSprite("game over again.jpg", 0, 0, _WIDTH, _HEIGHT)
win = GameSprite("victory background.jpg", 0, 0, _WIDTH, _HEIGHT)
bullets = sprite.Group()
enemies =  sprite.Group()
asteroids = sprite.Group()

def create_enemy():
    random_speed = randint(1, 4)
    enemy = Enemy("pirate ship.png", x=0, y=0, width=80, height=55, speed=random_speed)
    enemy.rect.x = randint(0, _WIDTH-enemy.rect.width)
    enemy.rect.bottom = 0
    enemies.add(enemy)
for i in range(8):
    create_enemy()

def create_asteroid():
    random_speed = randint(1, 4)
    asteroid = Asteroid("private ship part 2 have cut.jpg", x=0, y=0, width=80, height=55, speed=random_speed)
    asteroid.rect.x = randint(0, _WIDTH-asteroid.rect.width)
    asteroid.rect.bottom = 0
    asteroids.add(asteroid)
for i in range(8):
    create_asteroid()   
font.init()
f = font.SysFont('Arial', 70)
points = 0
death = False
done = False
destroyed = False
game_is_running = True    
while game_is_running:
    for e in event.get():
        if e.type == QUIT:
            game_is_running = False
        if e.type == KEYDOWN and e.key == K_SPACE:
            player.shoot()
    background.draw(window)
    second = time.get_ticks()//1000
    timer = f.render("Timer:"+ str(second), True, (255,255,255))
    window.blit(timer, (30, 30))
    point_text = f.render("Points:"+str(points), True, (255,255,255))
    window.blit(point_text, (30,80))
    
    if not done:
        player.update()
        player.draw(window)
        
        enemies.update()
        enemies.draw(window)

        bullets.update()
        bullets.draw(window)   

        asteroids.update()
        asteroids.draw(window)
    hits = sprite.groupcollide(bullets, enemies, True, True)
    for hit in hits:
        create_enemy()
        points += 1

    death = sprite.spritecollide(player, enemies, False)
    destroyed = sprite.spritecollide(player, asteroids, False)
    if death or destroyed:
        game_over. draw(window)
        done = True

    if second > 15 and points < 10:
        game_over.draw(window)
        done = True
        
        keys = key.get_pressed()
        if keys[K_r]:
            done = False
            game_is_running = True
    if points >= 10:
        win.draw(window)
        done = True
    display.update()
    clock.tick(60)