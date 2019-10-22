import pygame
from pygame.locals import *
import random
from settings import *



class Node(pygame.sprite.Sprite):
    def __init__(self, pos=None):
        super().__init__()
        self.pos = pos
        
        self.image = pygame.Surface([1*SCALE_FACTOR, 1*SCALE_FACTOR])
        self.rect = self.image.get_rect()
        self.image.fill((255,255,255))

        self.cost_scale = 1

        self.rect.x = self.pos[0]*SCALE_FACTOR
        self.rect.y = self.pos[1]*SCALE_FACTOR
        self.diggable = False
        self.health = 0
        self.dug = True

    def dig(self,damage):
        return False


class VoidSpace(Node):
    def __init__(self, pos=None):
        super().__init__(pos)
        self.image.fill((255,255,255))
        self.diggable = False


class Stone(Node):
    def __init__(self, pos=None):
        super().__init__(pos)
        temp = random.randint(76,96)
        self.image.fill((temp,temp,temp))
        self.diggable = True

        self.cost_scale = 1000
        self.health = 1000
        self.dug = False

    def dig(self,damage):
        if self.health > 10:
            self.health -= damage
            self.cost_scale -= damage
        if self.health <= 10:
            if self.dug == False:
                self.health = 10
                temp = random.randint(191,204)
                self.image.fill((temp,temp,temp))
                self.dug = True
                return True
        return False

class Ground(Node):
    def __init__(self, pos=None):
        super().__init__(pos)
        self.image.fill((random.randint(76,96),random.randint(57,64),random.randint(29,32)))
        self.diggable = True

        self.cost_scale = 100
        self.health = 100
        self.dug = False

    def dig(self,damage):
        if self.health > 10:
            self.health -= damage
            self.cost_scale -= damage
        if self.health <= 10:
            if self.dug == False:
                self.health = 10
                self.image.fill((random.randint(172,198),random.randint(115,140),random.randint(57,83)))
                self.dug = True
                return True
        return False


class Sky(Node):
    def __init__(self, pos=None):
        super().__init__(pos)
        self.image.fill((64,128,random.randint(172,198)))
        self.diggable = False
        self.cost_scale = 10
        self.health = 0

class Crust(Sky):
    def __init__(self, pos=None):
        super().__init__(pos)
        self.diggable = True
        self.cost_scale = 50