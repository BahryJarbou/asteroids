from circleshape import CircleShape
import pygame
from constants import *
import random

class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
    
    def draw(self, screen):
        pygame.draw.circle(screen, "white", self.position, self.radius, width = 2)
    
    def update(self, dt):
        self.position += self.velocity * dt
        
    def split(self):
        self.kill()
        if self.radius <= ASTEROID_MIN_RADIUS:
            return
        angle = random.uniform(20,50)
        random_angle = self.velocity.rotate(angle)
        random_angle_negative = self.velocity.rotate(-angle)
        new_radius = self.radius - ASTEROID_MIN_RADIUS
        x, y = self.position
        asteroid_1 = Asteroid(x, y, new_radius)
        asteroid_2 = Asteroid(x, y, new_radius)
        asteroid_1.velocity = random_angle * 1.2
        asteroid_2.velocity = random_angle_negative * 1.2