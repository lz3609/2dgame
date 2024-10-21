import pygame

IMG_PATH  = 'data/'

# Load the images
def load_image(path):
    img = pygame.image.load(IMG_PATH  + path).convert()
    img.set_colorkey((255, 255, 255))
    return img