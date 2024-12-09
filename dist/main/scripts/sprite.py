import pygame
import time
import random


class Sprite:
    def __init__(self, game, sprite_type, position, size):
        self.game = game
        self.type = sprite_type
        self.position = list(position)
        self.size = size
        self.velocity = [0, 0]
        self.collisions = {'up': False, 'down': False, 'right': False, 'left': False}
        
        self.action = ''
        self.anim_offset = (-3, -3)
        self.flip = False
        self.set_action('idle')
    
    def rect(self):
        return pygame.Rect(self.position[0], self.position[1], self.size[0], self.size[1])
    
    def set_action(self, action):
        if action != self.action:
            self.action = action
            self.animation = self.game.assets[self.type + '/' + self.action].copy()
        
    def update(self, tilemap, movement=(0, 0)):
        self.collisions = {'up': False, 'down': False, 'right': False, 'left': False}
        
        # Calculate movement based on velocity and input movement
        frame_movement = (movement[0] + self.velocity[0], movement[1] + self.velocity[1])
        
        # Update x position and handle collisions with tiles
        self.position[0] += frame_movement[0]
        entity_rect = self.rect()
        for rect in tilemap.get_physics_collisions_around(self.position):
            if entity_rect.colliderect(rect):
                if frame_movement[0] > 0:
                    entity_rect.right = rect.left
                    self.collisions['right'] = True
                if frame_movement[0] < 0:
                    entity_rect.left = rect.right
                    self.collisions['left'] = True
                self.position[0] = entity_rect.x
        
        # Update y position and handle collisions with tiles
        self.position[1] += frame_movement[1]
        entity_rect = self.rect()
        for rect in tilemap.get_physics_collisions_around(self.position):
            if entity_rect.colliderect(rect):
                if frame_movement[1] > 0:
                    entity_rect.bottom = rect.top
                    self.collisions['down'] = True
                if frame_movement[1] < 0:
                    entity_rect.top = rect.bottom
                    self.collisions['up'] = True
                self.position[1] = entity_rect.y
                
        if movement[0] > 0:
            self.flip = False
        if movement[0] < 0:
            self.flip = True
        
        # Apply gravity and cap falling velocity
        self.velocity[1] = min(5, self.velocity[1] + 0.1)
        
        if self.collisions['down'] or self.collisions['up']:
            self.velocity[1] = 0
            
        self.animation.update()
        
    def render(self, surf, offset=(0, 0)):
        surf.blit(pygame.transform.flip(self.animation.img(), self.flip, False), 
                  (self.position[0] - offset[0] + self.anim_offset[0], 
                   self.position[1] - offset[1] + self.anim_offset[1]))

class Monster(Sprite):
    def __init__(self, game, position, size):
        super().__init__(game, 'enemy', position,  size)

        self.walking = 0

    def update(self, tilemap, movement=(0,0)):
        if self.walking:
            if tilemap.check_tiles((self.rect().centerx + (-16 if self.flip else 16), self.position[1] + 46)):
                # Check if enemy can walk (based on tilemap and collision)
                if (self.collisions['right'] or self.collisions['left']):
                    self.flip = not self.flip
                else:
                    movement = (movement[0] - 0.5 if self.flip else 0.5, movement[1])
            else:
                self.flip = not self.flip

            # Decrease walking time and potentially flip direction
            self.walking = max(0, self.walking - 1)
            if not self.walking:
                # If the enemy isn't walking, check distance to player, if it is too close, attack the player
                distance = (self.game.player.position[0] - self.position[0], self.game.player.position[1] - self.position[1])
                if (abs(distance[1]) < 32):
                    if(self.flip and distance[0] < 0):
                        self.game.projectile.append([[self.rect().centerx - 16, self.rect().centery], -1.5, 0])
                    if (not self.flip and distance[0] > 0):
                        self.game.projectile.append([[self.rect().centerx + 16, self.rect().centery], 1.5, 0])

        elif random.random() < 0.01:
            # Randomly decide when to start walking
            self.walking = random.randint(30, 120)

        super().update(tilemap, movement=movement)

        # Update enemy animation
        if movement[0] != 0:
            self.set_action('run')
        else:
            self.set_action('idle')

        if abs(self.game.player.blinking) >= 50:
            if self.rect().colliderect(self.game.player.rect()):
                return True


class Player(Sprite):
    def __init__(self, game, position, size):
        super().__init__(game, 'player', position, size)
        self.air_time = 0
        self.jumps = 2
        self.blinking = 0
        self.invincible = False
        self.invincible_timer = 0  
        self.attacking = False  
        self.dead = False  
        self.attack_duration = 20  
        self.attack_timer = 0  
        self.attack_range = 50  

    def update(self, tilemap, movement=(0, 0)):
        super().update(tilemap, movement=movement)

        # Handle attack logic
        if self.attacking:
            self.attack_timer += 1  
            self.animation.update()  
            if self.attack_timer >= self.attack_duration:  
                self.attacking = False  
                self.attack_timer = 0  
                self.set_action('idle')  
                self.check_attack_collision()  

        else:
            # Handle jumping and movement states
            self.air_time += 1
            # See if player is in the air too long
            if self.air_time > 180:
                self.game.dead +=1

            if self.collisions['down']:
                self.air_time = 0
                self.jumps = 2
            
            if self.invincible:
                self.set_action('invincible')  

            if not self.invincible:
                if self.air_time > 4:
                    self.set_action('jump')
                elif movement[0] != 0:
                    self.set_action('run')
                else:
                    self.set_action('idle') 

        if self.velocity[0] > 0:
            self.velocity[0] = max(self.velocity[0] - 0.1, 0)
        else:
            self.velocity[0] = min(self.velocity[0] + 0.1, 0)

        # Handle blinking state and invincibility speed boost
        if self.blinking > 0:
            self.blinking = max(0, self.blinking - 1)
        if self.blinking < 0:
            self.blinking = min(0, self.blinking + 1)
        if abs(self.blinking) > 50:
            self.velocity[0] = abs(self.blinking) / self.blinking * 8
            if abs(self.blinking) == 51:
                self.velocity[0] *= 0.1

        # Handle invincible time
        if self.invincible and time.time() - self.invincible_timer > 1:
            self.invincible = False
        
    # Jump mechanics, player has two jumps
    def jump(self):
        if self.jumps:
            self.velocity[1] = -3
            self.jumps -= 1
            self.air_time = 5

    # Blinking/dashing 
    def blink(self):
        if not self.blinking:
            if self.flip:
                self.activate_invincibility()
                self.blinking = -60
            else:
                self.activate_invincibility()
                self.blinking = 60

    # Toggle invincibility
    def activate_invincibility(self):
        self.invincible = True
        self.invincible_timer = time.time()  

    #Attack mechanics to kill enemy
    def attack(self):
        if not self.attacking and not self.dead:  
            self.attacking = True
            self.attack_timer = 0  
            self.set_action('attack')  

    # Define the hitbox for the attack based on the player's position and attack range
    def check_attack_collision(self):
        attack_hitbox = pygame.Rect(self.position[0] + (self.size[0] // 2) - (self.attack_range // 2), 
        self.position[1], 
        self.attack_range, 
        self.size[1])  
        
        for monster in self.game.monsters.copy(): 
            if attack_hitbox.colliderect(monster.rect()):  
                self.game.monsters.remove(monster) 

    def die(self):
        if not self.invincible and not self.dead:  
            self.dead = True  
            self.game.load_level(0)
        
    def render(self, surf, offset=(0, 0)):
        super().render(surf, offset=offset)