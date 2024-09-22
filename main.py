import pygame
import sys

pygame.init()

screen_width = 1600
screen_height = 900

pygame.display.set_caption("game")
screen = pygame.display.set_mode((screen_width, screen_height))

clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        

        
    pygame.display.update()
    clock.tick(60)