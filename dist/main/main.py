import sys
import pygame
import os

from scripts.helper import load_image, load_images, Animation
from scripts.sprite import Sprite, Player, Monster
from scripts.tilemap import Tilemap

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('game')
        self.screen = pygame.display.set_mode((1280, 960))
        self.display = pygame.Surface((640, 480), pygame.SRCALPHA)
        self.display2 = pygame.Surface((640, 480))

        self.clock = pygame.time.Clock()
        self.movement = [False, False]

        # Load the assets
        self.assets = {
            'decoration': load_images('decoration'),
            'dirt': load_images('dirt'),
            'grass': load_images('grass'),
            'player': load_image('sprite.png'),
            'background': load_image('Background.png'),
            'player/idle': Animation(load_images('player/idle'), img_duration=14),
            'player/run': Animation(load_images('player/run'), img_duration=4),
            'player/jump': Animation(load_images('player/jump')),
            'player/invincible' : Animation(load_images('player/invincible'), img_duration=20),
            'player/attack' : Animation(load_images('player/attack'), img_duration = 9),
            'player/dead' : Animation(load_images('player/dead'), img_duration = 20),
            'enemy/idle' : Animation(load_images("enemy/eidle"), img_duration=12),
            'enemy/run' : Animation(load_images("enemy/ewalk"), img_duration=4),
            'projectile' : load_image('projectile.png')
        }
        
        self.player = Player(self, (200, 300), (20, 30))
        self.tilemap = Tilemap(self, tile_size=32)
        self.scroll = [0, 0]

        self.level = 0
        self.load_level(self.level)


    def load_level(self, level):
        self.tilemap.load_map('data/maps/' + str(level) + '.json')

        self.monsters = []
        for spawner in self.tilemap.extract([('spawner', 0), ('spawner', 1)]):
            if spawner['variant'] == 0:
                self.player.position = spawner['position'] 
                self.player.air_time = 0
            else:
                self.monsters.append(Monster(self, spawner['position'], (20, 30)))
        
        self.projectile = []
        self.scroll = [0, 0]
        self.dead = 0
        self.transition = -30
        
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    self.movement[0] = True
                if event.key == pygame.K_d:
                    self.movement[1] = True
                if event.key == pygame.K_SPACE:
                    self.player.jump()
                if event.key == pygame.K_LSHIFT:
                    self.player.blink()
         
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    self.movement[0] = False
                if event.key == pygame.K_d:
                    self.movement[1] = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: # Left click
                    self.player.attack()
                if event.button == 3: # Right click
                    self.player.activate_invincibility()
                

    def run(self):
        while True:
            self.handle_events() 
            self.display.fill((0, 0, 0, 0))
            self.display2.blit(self.assets['background'], (0, 0))

            if not len(self.monsters):
                self.transition += 1
                if self.transition > 30:
                    self.level = min(self.level + 1, len(os.listdir('data/maps')) - 1)
                    self.load_level(self.level)
            if self.transition < 0:
                self.transition += 1
       
            self.scroll[0] += (self.player.rect().centerx - self.display.get_width() / 2 - self.scroll[0]) / 30
            self.scroll[1] += (self.player.rect().centery - self.display.get_height() / 2 - self.scroll[1]) / 30
            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))
            
            # Rendering the game world
            self.tilemap.render(self.display, offset=render_scroll)

            #Kill and remove monster
            for monster in self.monsters.copy():
                kill = monster.update(self.tilemap, (0, 0))
                monster.render(self.display, offset =render_scroll)
                if kill:
                    self.monsters.remove(monster)

            # Update and render player
            if not self.dead:
                self.player.update(self.tilemap, (self.movement[1] - self.movement[0], 0))
                self.player.render(self.display, offset=render_scroll)
            
            # Handle player death and level transitions
            if self.dead and not self.player.rect().colliderect(monster.rect()):
                self.dead += 1
                if self.dead >= 10:
                    self.transition =min(30, self.transition + 1)
                    self.load_level(self.level)
            elif self.player.rect().colliderect(monster.rect()) and not self.dead:  
                self.player.die()
                  
            # Update and render projectiles
            for projectile in self.projectile.copy():
                projectile[0][0] += projectile[1]
                projectile[2] += 1
                img = self.assets['projectile']
                self.display.blit(img, (projectile[0][0] -- img.get_width() / 2 - render_scroll[0], projectile[0][1] - img.get_height() / 2 - render_scroll[1]))
                if self.tilemap.check_tiles(projectile[0]):
                    self.projectile.remove(projectile)
                elif projectile[2] > 360:
                    self.projectile.remove(projectile)
                elif abs(self.player.blinking < 50):
                    if self.player.rect().collidepoint(projectile[0]):
                       self.projectile.remove(projectile)
                       self.dead += 1

            # Apply a shadow for display effects
            display_shadow = pygame.mask.from_surface(self.display)
            display_shade = display_shadow.to_surface(setcolor=(0, 0, 0, 180), unsetcolor=(0, 0, 0, 0))
            self.display2.blit(display_shade, (0, 0))

            # Handle transition effect
            if self.transition:
                transition_surface = pygame.Surface(self.display.get_size())
                pygame.draw.circle(transition_surface, (255, 255, 255), (self.display.get_width() // 2, self.display.get_height() // 2), (30 - abs(self.transition)) * 8)
                transition_surface.set_colorkey((255, 255, 255))
                self.display.blit(transition_surface, (0, 0))

            # Render the display with slight offset
            self.display2.blit(self.display, (2,2)) 

            # Draw the display to the screen
            self.screen.blit(pygame.transform.scale(self.display2, self.screen.get_size()), (0, 0))
            pygame.display.update()
            self.clock.tick(60)

# Run the game
Game().run()
