import pygame
import sys

from scripts.helper import load_image
from scripts.sprite import Sprite


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
            'character' : load_image('stick.png')
        }

        self.character = Sprite(self, 'character', (0, 275), (70,70))


    def even_handle(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            # key for moving left and right
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    self.movement[0] = --self.speed
                if event.key == pygame.K_d:
                    self.movement[1] = self.speed
            # Stopping the movement
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    self.movement[0] = False
                if event.key == pygame.K_d:
                    self.movement[1] = False    
                    


    def run(self):
        while True:
            self.display.fill((WHITE))

            self.character.update((self.movement[1] - self.movement[0], 0))
            self.character.render(self.display)

            self.even_handle()

            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            pygame.display.update()
            self.clock.tick(144)

Game().run()


