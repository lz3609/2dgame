import os
import pygame

BASE_IMG_PATH = 'data/'

def load_image(path):
    """
    Loads a single image from the given path
    """
    img = pygame.image.load(BASE_IMG_PATH + path).convert_alpha()  # Load the image 
    img.set_colorkey((0, 0, 0))  
    return img

def load_images(path):
    """
    Loads all images from the folder, sorted by file name.
    """
    images = []
    for img_name in sorted(os.listdir(BASE_IMG_PATH + path)):
        images.append(load_image(path + '/' + img_name))  # Load each image in the folder
    return images

class Animation:
    """
    Manages an animation cycle through a list of images. 
    """
    def __init__(self, images, img_duration=5, loop=True):
        """
        Initializes the animation with the provided images and duration.
        """
        self.images = images
        self.loop = loop
        self.img_duration = img_duration  
        self.done = False  
        self.frame = 0  
    def copy(self):
        """
        Creates a copy of the animation object.
        """
        return Animation(self.images, self.img_duration, self.loop)
    
    def update(self):
        """
        Updates the current frame of the animation.
        Loops the animation if the loop flag is set to True.
        """
        if self.loop:
            # Loop the animation frames
            self.frame = (self.frame + 1) % (self.img_duration * len(self.images))
        else:
            # Play once and stop after the last frame
            self.frame = min(self.frame + 1, self.img_duration * len(self.images) - 1)
            if self.frame >= self.img_duration * len(self.images) - 1:
                self.done = True  

    def img(self):
        """
        Returns the image corresponding to the current frame.
        """
        return self.images[int(self.frame / self.img_duration)]
