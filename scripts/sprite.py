import pygame

class Sprite:
    def __init__(self, game, sprite_type, position, size):
        self.game = game
        self.type = sprite_type
        self.position = list(position)
        self.size = size
        self.velocity = [0, 0]
        

        self.image = pygame.transform.scale(self.game.assets[sprite_type], size)

    def update(self, movement=(0, 0)):
        frame_movement = (
            movement[0] + self.velocity[0],
            movement[1] + self.velocity[1]
        )
        # Update x pos
        self.position[0] += frame_movement[0]
        # Update y pos
        self.position[1] += frame_movement[1] 

    def render(self, surface):
        surface.blit(self.image, self.position)


        