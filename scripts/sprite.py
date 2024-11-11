import pygame

class Sprite:
    def __init__(self, game, sprite_type, position, size):
        self.game = game
        self.type = sprite_type
        self.position = list(position)
        self.size = size
        self.velocity = [0, 0]
        self.collisions = {'up' : False, 'down' : False, "right" : False, 'left' : False}
        self.image = pygame.transform.scale(self.game.assets[sprite_type], size)

    def rect(self):
        return pygame.Rect(self.position[0], self.position[1], self.size[0], self.size[1])

    def update(self, tilemap, movement=(0, 0)):
        self.collisions = {'up' : False, 'down' : False, "right" : False, 'left' : False}

        frame_movement = (
            movement[0] + self.velocity[0], 
            movement[1] + self.velocity[1])

        self.position[0] += frame_movement[0]
        sprite_rect = self.rect()
        for rect in tilemap.physics_rect(self.position):
            if sprite_rect.colliderect(rect):
                if frame_movement[0] > 0: 
                    sprite_rect.right = rect.left
                    self.collisions['right'] = True
                if frame_movement[0] < 0: 
                    sprite_rect.left = rect.right
                    self.collisions['left'] = True
                self.position[0] = sprite_rect.x
     
        self.position[1] += frame_movement[1] 
        sprite_rect = self.rect()
        for rect in tilemap.physics_rect(self.position):
            if sprite_rect.colliderect(rect):
                if frame_movement[1] > 0:  
                    sprite_rect.bottom = rect.top 
                    self.collisions['down'] = True
                if frame_movement[1] < 0:  
                    sprite_rect.top = rect.bottom
                    self.collisions['up'] = True
                self.position[1] = sprite_rect.y

        self.velocity[1] = min(3, self.velocity[1] + 0.1)

        if self.collisions['down'] or self.collisions['up']:
            self.velocity[1] = 0

    def render(self, surface):
        surface.blit(self.image, self.position)


        