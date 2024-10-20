# this allows us to use code from
# the open-source pygame library
# throughout this file
import pygame
from constants import *
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot
from explosion import Explosion
score = 0

def main():
    score = 0
    pygame.init()
    pygame.font.init()
    pygame.mixer.init()
    boom = pygame.mixer.Sound("explosion.wav")
    print("Starting asteroids!")
    print("Screen width:", SCREEN_WIDTH)
    print("Screen height:", SCREEN_HEIGHT)
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    my_font = pygame.font.Font(pygame.font.get_default_font(), 30)
    clock = pygame.time.Clock()
    dt = 0
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    explosions = pygame.sprite.Group()
    
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable)
    Player.containers = (updatable, drawable)
    Shot.containers = (shots, updatable, drawable)
    Explosion.containers = (explosions, updatable, drawable)
    
    player = Player(x=SCREEN_WIDTH/2, y=SCREEN_HEIGHT/2)
    asteroid_field = AsteroidField()
    
    while True:
        text_surface = my_font.render(f"score: {score}", False, (255, 255, 255))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        
        for object in updatable:    
            object.update(dt)
        
        for object in asteroids:
            if object.check_collision(player):
                if player.lives == 0:  
                    print("Game over!")
                    print(f"Your score is: {score}")
                    return
                for object in asteroids:
                    object.kill()
                player.respawn()
                
        
        for object in asteroids:
            for bullet in shots:
                if object.check_collision(bullet):
                    boom.play()
                    object.explosion()
                    object.split()
                    bullet.kill()
                    score += 1
        
        for object in explosions:
            object.del_particle()
            
        background = pygame.image.load("space.jpg").convert()
        background = pygame.transform.scale(background,(1280, 720))
        
        screen.blit(background, (0, 0))
        screen.blit(text_surface, (0, 0))
        for object in drawable:
            object.draw(screen)
        pygame.display.flip()
        
        # limit the framerate to 60 FPS
        dt = clock.tick(60)/1000


if __name__ == "__main__":
    main()