from circleshape import CircleShape
import pygame
from constants import *
from random import uniform

class Powerup(CircleShape):
    def __init__(self,powerup):
        super().__init__(uniform(0,SCREEN_WIDTH),uniform(0,SCREEN_HEIGHT),radius = 30)
        self.taken = False
        self.rotation = 0
        self.powerup = powerup
    
    def draw(self,screen):
        pygame.draw.circle(screen,"red",self.position,self.radius+2, width=2)
        if self.powerup == "shield":
            pygame.draw.polygon(screen,"white",self.shield(), width=2)
        if self.powerup == "speedup":
            pygame.draw.polygon(screen,"white",self.speedup(), width=2)
    
    
    def shield(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius /1.5
        a = self.position + forward/1.2 * self.radius
        b = self.position + forward/2 * self.radius - right
        c = self.position - forward/2 * self.radius - right
        d = self.position - forward/2 * self.radius + right
        e = self.position + forward/2 * self.radius + right
        return [a,b,c,d,e]
    
    
    def speedup(self):
        forward = pygame.Vector2(0, -1).rotate(self.rotation)
        right = pygame.Vector2(0, -1).rotate(self.rotation + 90) * self.radius /1.5
        a = self.position + forward/1.2 * self.radius
        b = self.position + forward/2 * self.radius - right
        c = self.position + forward/2 * self.radius - right/2
        d = self.position - forward/2 * self.radius - right/2
        e = self.position - forward/2 * self.radius + right/2
        f = self.position + forward/2 * self.radius + right/2
        g = self.position + forward/2 * self.radius + right
        return [a,b,c,d,e,f,g]