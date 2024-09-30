import pygame
import sys

screen_width = 1600
screen_height = 900

class Game:
    def __init__(self):
        pygame.init()

        pygame.display.set_caption("game")
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        self.clock = pygame.time.Clock()
        self.background = pygame.image.load('images/background.png')
        self.background = pygame.transform.scale(self.background, (screen_width, screen_height))
    
    def run(self):
        while True:
            self.screen.blit(self.background, (0,0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
        
            pygame.display.update()
            self.clock.tick(60)

Game().run()