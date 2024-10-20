from circleshape import CircleShape
import pygame
from constants import *
import random
from explosion import Explosion

class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
    
    def draw(self, screen):
        pygame.draw.circle(screen, "white", self.position, self.radius, width = 2)
    
    def update(self, dt):
        self.position += self.velocity * dt
        if self.position.x < -self.radius and self.velocity.x < 0:
            self.position.x = SCREEN_WIDTH + self.radius
        if self.position.x > SCREEN_WIDTH + self.radius and self.velocity.x > 0 :
            self.position.x = -self.radius
        if self.position.y < -self.radius and self.velocity.y < 0:
            self.position.y = SCREEN_HEIGHT + self.radius
        if self.position.y > SCREEN_HEIGHT + self.radius and self.velocity.y < 0:
            self.position.y = -self.radius

        
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

    def explosion(self):
        angle = 72
        new_radius = 3
        x, y = self.position
        particle_1 = Explosion(x, y, new_radius)
        particle_2 = Explosion(x, y, new_radius)
        particle_3 = Explosion(x, y, new_radius)
        particle_4 = Explosion(x, y, new_radius)
        particle_5 = Explosion(x, y, new_radius)
        particle_1.velocity = self.velocity.rotate(angle) * 3
        particle_2.velocity = self.velocity.rotate(2*angle) * 3
        particle_3.velocity = self.velocity.rotate(3*angle) * 3
        particle_4.velocity = self.velocity.rotate(4*angle) * 3
        particle_5.velocity = self.velocity.rotate(5*angle) * 3