from constants import *
from circleshape import CircleShape
import pygame

class Explosion(CircleShape):
    def __init__(self, x, y, radius = 2):
        super().__init__(x, y, radius)
        self.origin_pos = pygame.Vector2(x,y)
        
        
    def draw(self, screen):
        pygame.draw.circle(screen, "white", self.position, self.radius, width = 2)
    
    def update(self, dt):
        self.position += self.velocity * dt
        
    
    def del_particle(self):
        if self.position.distance_to(self.origin_pos) > 100 :
            self.kill()
            