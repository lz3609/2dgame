import os
import pygame

IMG_PATH  = 'data/'

# Load the images
def load_image(path):
    img = pygame.image.load(IMG_PATH  + path).convert()
    img.set_colorkey((255, 255, 255))
    return img

# Load the tiles
def load_tiles(path):
    images = []
    for img_name in sorted(os.listdir(IMG_PATH + path)):
        images.append(load_image(path + '/' + img_name))
    return images