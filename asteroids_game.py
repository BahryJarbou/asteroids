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
from powerups import Powerup
from timer import Timer
from random import randint

def main():
    powerup_types = ["shield","speedup"]
    time = Timer()
    score = 0
    active_powerup = 0
    muted = False
    raise_difficulty = True
    pygame.init()
    pygame.font.init()
    pygame.mixer.init()
    boom = pygame.mixer.Sound("explosion.wav")
    shielded = pygame.mixer.Sound("shield.wav")
    # print("Starting asteroids!")
    # print("Screen width:", SCREEN_WIDTH)
    # print("Screen height:", SCREEN_HEIGHT)
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    my_font = pygame.font.Font(pygame.font.get_default_font(), 30)
    clock = pygame.time.Clock()
    dt = 0
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    explosions = pygame.sprite.Group()
    powerups = pygame.sprite.Group()
    
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable)
    Player.containers = (updatable, drawable)
    Shot.containers = (shots, updatable, drawable)
    Explosion.containers = (explosions, updatable, drawable)
    Powerup.containers = (powerups, drawable)
    
    
    player = Player(x=SCREEN_WIDTH/2, y=SCREEN_HEIGHT/2)
    asteroid_field = AsteroidField()
    
    button_surface = pygame.Surface((150, 50))
    text = my_font.render("Mute", False, (0, 0, 0))
    text_rect = text.get_rect(center=(button_surface.get_width()/2, button_surface.get_height()/2))


    # Create a pygame.Rect object that represents the button's boundaries
    button_rect = pygame.Rect(SCREEN_WIDTH-160, 10, 150, 50)
    
    while True:
        

               
        if time.get_time() % 10 != 0:
            raise_difficulty  = True
        
        if time.get_time() % 5 == 0 and time.get_time() !=0 and active_powerup == 0:
            shield = Powerup(powerup_types[randint(0,1)])
            active_powerup +=1
            raise_difficulty = True
        
        if time.get_time() % 10 == 0 and time.get_time() !=0 and raise_difficulty == True:
            asteroid_field.difficulty += 0.05
            raise_difficulty = False
            
            

        text_surface = my_font.render(f"score: {score}, Time: {time.get_time()}, speed: {player.init_acceleration}", False, (255, 255, 255))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            
            # Check for the mouse button down event
            match muted:
                case False:
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # Call the on_mouse_button_down() function
                        if button_rect.collidepoint(event.pos):
                            # print("Now muted")
                            text = my_font.render("Unmute", False, (0, 0, 0))
                            text_rect = text.get_rect(center=(button_surface.get_width()/2, button_surface.get_height()/2))
                            pygame.mixer.pause()
                            muted = True
                case True:
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # Call the on_mouse_button_down() function
                        if button_rect.collidepoint(event.pos):
                            # print("Now umnuted")
                            text = my_font.render("Mute", False, (0, 0, 0))
                            text_rect = text.get_rect(center=(button_surface.get_width()/2, button_surface.get_height()/2))
                            pygame.mixer.unpause()
                            muted = False
            
        if button_rect.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(button_surface, (127, 255, 212), (1, 1, 148, 48))
        else:
            pygame.draw.rect(button_surface, (0, 0, 0), (0, 0, 150, 50))
            pygame.draw.rect(button_surface, (255, 255, 255), (1, 1, 148, 48))
            pygame.draw.rect(button_surface, (0, 0, 0), (1, 1, 148, 1), 2)
            pygame.draw.rect(button_surface, (0, 100, 0), (1, 48, 148, 10), 2)

        
        for object in updatable:    
            object.update(dt)
        
        for object in asteroids:
            if object.check_collision(player):
                if player.shielded == False:
                    if player.lives == 0:  
                        print("Game over!")
                        print(f"Your score is: {score}")
                        return
                    for object in asteroids:
                        object.kill()
                    player.respawn()
                player.shielded = False
                object.kill()
                
        
        for object in asteroids:
            for bullet in shots:
                if object.check_collision(bullet):
                    if not muted:
                        boom.play()
                    object.explosion()
                    object.split()
                    bullet.kill()
                    score += 1
        
        for object in powerups:
            if object.check_collision(player):
                if not muted:
                    shielded.play()
                active_powerup = 0
                if object.powerup == "shield":
                    player.shielded = True
                if object.powerup == "speedup":
                    if player.init_acceleration < 1:
                       player.init_acceleration += 0.1
                
                object.kill()
        
        for object in explosions:
            object.del_particle()
        
        background = pygame.image.load("space.jpg").convert()
        background = pygame.transform.scale(background,(1280, 720))
        
        screen.blit(background, (0, 0))
        screen.blit(text_surface, (0, 0))

        # Show the button text
        button_surface.blit(text, text_rect)

        # Draw the button on the screen
        screen.blit(button_surface, (button_rect.x, button_rect.y))

        for object in drawable:
            object.draw(screen)
        pygame.display.flip()
        
        # limit the framerate to 60 FPS
        dt = clock.tick(60)/1000


if __name__ == "__main__":
    main()