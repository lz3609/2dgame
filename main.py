import pygame
import sys

from scripts.helper import load_image, load_tiles
from scripts.sprite import Sprite
from scripts.tilemap import Tilemap


screen_width = 1600
screen_height = 900
WHITE = (255, 255, 255)

class Game:
    def __init__(self):
        pygame.init()

        pygame.display.set_caption("stickman game")
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        self.display = pygame.Surface((800, 450))

        self.clock = pygame.time.Clock()

        self.movement = [0, 0] 
        self.speed = 1.8

        self.assets = {
            'platform' : load_tiles('plat'),
            'platform1' : load_tiles('plat1'),
            'character' : load_image('stick.png')
        }

        print(self.assets)

        # position and size
        self.character = Sprite(self, 'character', (60, 100), (15,15))   
        self.tilemap = Tilemap(self, tile_size=16)


    def event_handle(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            # key for moving left and right, jump
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    self.movement[0] = self.speed
                if event.key == pygame.K_d:
                    self.movement[1] = self.speed
                if event.key == pygame.K_SPACE:
                    self.character.velocity[1] = -3
            # Stopping the movement
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    self.movement[0] = 0
                if event.key == pygame.K_d:
                    self.movement[1] = 0    
                    
    def run(self):
        while True:
            # Game Updates
            self.display.fill((WHITE))
            self.tilemap.render(self.display)
            self.character.update(self.tilemap, (self.movement[1] - self.movement[0], 0))
            self.character.render(self.display)

            #event handle
            self.event_handle()

            # Render to screen
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            pygame.display.update()
            self.clock.tick(144)

Game().run()


