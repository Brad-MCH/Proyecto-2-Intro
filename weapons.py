from pygame import *
import math
from constants import *

def mouse_tile_index():
    pos = mouse.get_pos()
    x = pos[0] // TILE_SIZE
    y = pos[1] // TILE_SIZE
    return x + (y * WORLD_COLS)

# Esta clase maneja los ataques del mago rojo.
class RedMage:
    def __init__(self, weapons, obstacles):
        self.fireball_image = weapons[0]
        self.firebomb_image = weapons[1]
        self.angle = 0
        self.fired = False
        self.last_shot = time.get_ticks()
        self.obstacles = obstacles

    def update(self, player):
        object_fired = None

        pos = mouse.get_pos()
        x_dist = pos[0] - player.rect.centerx
        y_dist = -(pos[1] - player.rect.centery)
        self.angle = math.degrees(math.atan2(y_dist, x_dist))

        if mouse.get_pressed()[2] and not self.fired and (time.get_ticks() - self.last_shot) >= TROWN_COOLDOWN and player.mana >= ESP_ATACK_MANA:
            player.mana -= ESP_ATACK_MANA
            object_fired = RedFireball(self.fireball_image, player.rect.centerx, player.rect.centery, self.angle, self.obstacles)
            self.fired = True
            self.last_shot = time.get_ticks()
        
        if not mouse.get_pressed()[2]:
            self.fired = False

        if mouse.get_pressed()[0] and not self.fired and (time.get_ticks() - self.last_shot) >= TROWN_COOLDOWN and player.mana >= BOMB_MANA:
            player.mana -= BOMB_MANA
            object_fired = FireBomb(self.firebomb_image, player.rect.centerx, player.rect.centery, self.angle, self.obstacles)
            self.fired = True
            self.last_shot = time.get_ticks()
        
        if not mouse.get_pressed()[0]:
            self.fired = False
        
        return object_fired

class Archer:
    def __init__(self, weapons, obstacles):
        self.arrow_image = weapons[0]
        self.firebomb_image = weapons[1]
        self.angle = 0
        self.fired = False
        self.last_shot = time.get_ticks()
        self.obstacles = obstacles

    def update(self, player):
        object_fired = None

        pos = mouse.get_pos()
        x_dist = pos[0] - player.rect.centerx
        y_dist = -(pos[1] - player.rect.centery)
        self.angle = math.degrees(math.atan2(y_dist, x_dist))

        if mouse.get_pressed()[2] and not self.fired and (time.get_ticks() - self.last_shot) >= TROWN_COOLDOWN:
            object_fired = Arrow(self.arrow_image, player.rect.centerx, player.rect.centery, self.angle, self.obstacles)
            self.fired = True
            self.last_shot = time.get_ticks()
        
        if not mouse.get_pressed()[2]:
            self.fired = False

        if mouse.get_pressed()[0] and not self.fired and (time.get_ticks() - self.last_shot) >= TROWN_COOLDOWN:
            object_fired = FireBomb(self.firebomb_image, player.rect.centerx, player.rect.centery, self.angle, self.obstacles)
            self.fired = True
            self.last_shot = time.get_ticks()
        
        if not mouse.get_pressed()[0]:
            self.fired = False
        
        return object_fired

class Warrior:
    def __init__(self, weapons, obstacles):
        self.dagger_image = weapons[0]
        self.firebomb_image = weapons[1]
        self.angle = 0
        self.fired = False
        self.last_shot = time.get_ticks()
        self.obstacles = obstacles

    def update(self, player):
        object_fired = None

        pos = mouse.get_pos()
        x_dist = pos[0] - player.rect.centerx
        y_dist = -(pos[1] - player.rect.centery)
        self.angle = math.degrees(math.atan2(y_dist, x_dist))

        if mouse.get_pressed()[2] and not self.fired and (time.get_ticks() - self.last_shot) >= TROWN_COOLDOWN:
            object_fired = Dagger(self.dagger_image, player.rect.centerx, player.rect.centery, self.angle, self.obstacles)
            self.fired = True
            self.last_shot = time.get_ticks()
        
        if not mouse.get_pressed()[2]:
            self.fired = False

        if mouse.get_pressed()[0] and not self.fired and (time.get_ticks() - self.last_shot) >= TROWN_COOLDOWN:
            object_fired = FireBomb(self.firebomb_image, player.rect.centerx, player.rect.centery, self.angle, self.obstacles)
            self.fired = True
            self.last_shot = time.get_ticks()
        
        if not mouse.get_pressed()[0]:
            self.fired = False
        
        return object_fired


# Esta clase maneja el ataque de bola de fuego del mago rojo.       
class RedFireball(sprite.Sprite):

    def __init__(self, image, x, y, angle, obstacles):
        sprite.Sprite.__init__(self)
        self.original_image = image
        self.angle = angle
        self.image = transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.obstacles = obstacles
        self.collide_rect = Rect(0, 0, 30, 30)
        self.collide_rect.center = self.rect.center
        self.spawn_time = time.get_ticks()
        

        self.dx = math.cos(math.radians(self.angle)) * TROWN_SPEED
        self.dy = -(math.sin(math.radians(self.angle)) * TROWN_SPEED)
        
    def update(self, screen_scroll):
        range = 1000
        self.rect.x += self.dx + screen_scroll[0]
        self.rect.y += self.dy + screen_scroll[1]
        self.collide_rect.center = self.rect.center


        if time.get_ticks() - self.spawn_time > range:
            self.kill()

        for obstacle in self.obstacles:
            if self.collide_rect.colliderect(obstacle[1]):
                self.kill()

    def draw(self, surface):
        surface.blit(self.image, ((self.rect.centerx - int(self.image.get_width()/2)), self.rect.centery - int(self.image.get_height()/2)))
        # Para Brandon: Puede descomentar esto para ver los rectángulos de colisión 
        #draw.rect(surface, (255, 0, 0), self.rect, 1)  #Este rectángulo es el de la imagen
        #draw.rect(surface, (0, 255, 0), self.collide_rect, 1) #Este rectángulo es el de colisión

# Esta clase maneja un hechizo de bomba que puede ser utilizado por varios personajes.
class FireBomb(sprite.Sprite):
    def __init__(self, image, x, y, angle, obstacles):
        sprite.Sprite.__init__(self)
        self.original_image = image
        self.angle = angle
        self.image = transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.obstacles = obstacles
        self.collide_rect = Rect(0, 0, 30, 30)
        self.collide_rect.center = self.rect.center
        self.spawn_time = time.get_ticks()

        self.dx = math.cos(math.radians(self.angle)) * TROWN_SPEED
        self.dy = -(math.sin(math.radians(self.angle)) * TROWN_SPEED)

        self.bomb_mode = False
        self.wall_hitten = None

        

    def update(self, screen_scroll):
        
            
        range = 100
        self.rect.x += self.dx + screen_scroll[0]
        self.rect.y += self.dy + screen_scroll[1]
        self.collide_rect.center = self.rect.center

        if not self.bomb_mode:
            if time.get_ticks() - self.spawn_time > range:
                self.dx = self.dy = 0
                self.bomb_mode = True

            for obstacle in self.obstacles:
                if self.collide_rect.colliderect(obstacle[1]):
                    self.bomb_mode = True
                    self.wall_hitten = obstacle[1]
                    self.dx = self.dy = 0
        else:
            """
            Brandon, Aquí irá la lógica de la explosión de la bomba.
            Ahora mismo se queda quieta al tocar una pared. pensaba que sería bueno
            que se comportara como una sticky bomb, que se queda pegada a la pared
            y explota después de un tiempo.

            Antes de entrar a este else, se guardó la pared tocada en self.wall_hitten.
            pensaba que se podría partir de esa infomación para hacer obtener la ubicación
            de la explosión, pero no sé si es lo mejor.
            """
            

    def draw(self, surface):
        surface.blit(self.image, ((self.rect.centerx - int(self.image.get_width()/2)), self.rect.centery - int(self.image.get_height()/2)))

"""
Brandon, en este documento hay dos tipos de clases: 
Una clase que maneja los ataques de un personaje en especifico (mago rojo)
y una clase que maneja ataques que pueden ser utilizados por varios personajes.

las clases de ataques son RedFireball y FireBomb están asignadas al mago rojo,
pero pueden ser utilizadas por otros personajes.

Es decir, para agregar un nuevo personaje se debe de crear una nueva clase para ese personaje o 
si se quiere poner elegantemente, se puede crear una clase base de personaje que maneje los ataques
y que herede de ella el personaje en especifico.

Para los ataques, se podría hacer lo mismo, crear una clase base de ataque que maneje los ataques
y que herede de ella los ataques específicos de cada personaje. Si no, se pueden crear las clases de ataque directamente como lo hice aquí.
"""
class Arrow(sprite.Sprite):

    def __init__(self, image, x, y, angle, obstacles):
        sprite.Sprite.__init__(self)
        self.original_image = image
        self.angle = angle
        self.image = transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.obstacles = obstacles
        self.collide_rect = Rect(0, 0, 30, 30)
        self.collide_rect.center = self.rect.center
        self.spawn_time = time.get_ticks()
        

        self.dx = math.cos(math.radians(self.angle)) * TROWN_SPEED
        self.dy = -(math.sin(math.radians(self.angle)) * TROWN_SPEED)
        
    def update(self, screen_scroll):
        range = 1000
        self.rect.x += self.dx + screen_scroll[0]
        self.rect.y += self.dy + screen_scroll[1]
        self.collide_rect.center = self.rect.center


        if time.get_ticks() - self.spawn_time > range:
            self.kill()

        for obstacle in self.obstacles:
            if self.collide_rect.colliderect(obstacle[1]):
                self.kill()

    def draw(self, surface):
        surface.blit(self.image, ((self.rect.centerx - int(self.image.get_width()/2)), self.rect.centery - int(self.image.get_height()/2)))

class Dagger(sprite.Sprite):

    def __init__(self, image, x, y, angle, obstacles):
        sprite.Sprite.__init__(self)
        self.original_image = image
        self.angle = angle
        self.image = transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.obstacles = obstacles
        self.collide_rect = Rect(0, 0, 30, 30)
        self.collide_rect.center = self.rect.center
        self.spawn_time = time.get_ticks()
        

        self.dx = math.cos(math.radians(self.angle)) * TROWN_SPEED
        self.dy = -(math.sin(math.radians(self.angle)) * TROWN_SPEED)
        
    def update(self, screen_scroll):
        range = 1000
        self.rect.x += self.dx + screen_scroll[0]
        self.rect.y += self.dy + screen_scroll[1]
        self.collide_rect.center = self.rect.center


        if time.get_ticks() - self.spawn_time > range:
            self.kill()

        for obstacle in self.obstacles:
            if self.collide_rect.colliderect(obstacle[1]):
                self.kill()

    def draw(self, surface):
        surface.blit(self.image, ((self.rect.centerx - int(self.image.get_width()/2)), self.rect.centery - int(self.image.get_height()/2)))