from circleshape import *
from constants import *
import pygame
from shot import Shot

class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.shot_timer = 0
        self.lives = LIVES
        self.init_acceleration = 0.1
        self.acceleration = self.init_acceleration
        self.shielded = False

            
    # in the player class
    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]
    
    def draw(self, screen):
        pygame.draw.polygon(screen, "white", self.triangle(), 2)
        if self.shielded:
            pygame.draw.circle(screen, "white",self.position,self.radius*2, 2)
        
    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt
    
    def update(self, dt):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.rotate(-dt)
        if keys[pygame.K_d]:
            self.rotate(dt)
        if keys[pygame.K_w]:
            self.move(dt)
        if keys[pygame.K_s]:
            self.move(-dt)
        if keys[pygame.K_SPACE]:
            self.shoot()
        if self.shot_timer > 0:
            self.shot_timer -= dt
        
        if True not in keys:
            if self.acceleration > 0.1 :
                self.acceleration = self.init_acceleration
    
    def move(self, dt):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        self.position += forward * PLAYER_SPEED * self.acceleration * dt
        if self.acceleration < 2:
            self.acceleration += 0.01
            clock = pygame.time.Clock()
            clock.tick(60)
    
    def shoot(self):
        if self.shot_timer <= 0:
            x, y = self.position
            pellet_1 = Shot(x, y)
            pellet_2 = Shot(x, y)
            pellet_3 = Shot(x, y)
            pellet_1.velocity = pygame.Vector2(0,1).rotate(self.rotation+30) * PLAYER_SHOT_SPEED
            pellet_2.velocity = pygame.Vector2(0,1).rotate(self.rotation) * PLAYER_SHOT_SPEED
            pellet_3.velocity = pygame.Vector2(0,1).rotate(self.rotation-30) * PLAYER_SHOT_SPEED
            self.shot_timer = PLAYER_SHOOT_COOLDOWN
    
    def respawn(self):
        self.position = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
        self.lives -= 1
    
        