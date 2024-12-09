#Level Editor, you can create your own level
import sys
import pygame

from scripts.helper import load_images
from scripts.tilemap import Tilemap

class Game:
    def __init__(self):
        pygame.init()

        # Window and display setup
        pygame.display.set_caption('level')
        self.screen = pygame.display.set_mode((1280, 960))
        self.display = pygame.Surface((640, 480))

        self.clock = pygame.time.Clock()

        # Load assets
        self.assets = {
            'decoration': load_images('decoration'),
            'dirt': load_images('dirt'),
            'grass': load_images('grass'),
            'spawner' : load_images('spawner')
        }

        # Game state variables
        self.movement = [False, False, False, False]  # Left, Right, Up, Down
        self.tilemap = Tilemap(self, tile_size=32)

        try:
            self.tilemap.load_map('map.json')
        except FileNotFoundError:
            pass

        self.scroll = [0, 0]

        # Tile selection
        self.tile_list = list(self.assets)
        self.tile_group = 0
        self.tile_variant = 0

        # Input state
        self.clicking = False
        self.right_clicking = False
        self.shift = False
        self.ongrid = True

    def run(self):
        while True:
            # Clear the display
            self.display.fill((0, 0, 0))

            # WASD to move camera around
            self.scroll[0] += (self.movement[1] - self.movement[0]) * 2 
            self.scroll[1] += (self.movement[3] - self.movement[2]) * 2

            # Render the tilemap with scroll offset
            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))
            self.tilemap.render(self.display, offset=render_scroll)

            # Prepare the current tile for rendering
            current_tile = self.assets[self.tile_list[self.tile_group]][self.tile_variant].copy()
            current_tile.set_alpha(100)

            # Determine mouse and tile positions
            mouse_pos = pygame.mouse.get_pos()
            mouse_pos = (mouse_pos[0] / 2.0, mouse_pos[1] / 2.0)
            tile_pos = (
                int((mouse_pos[0] + self.scroll[0]) // self.tilemap.tile_size),
                int((mouse_pos[1] + self.scroll[1]) // self.tilemap.tile_size)
            )
            

            # See where you are placing stuff
            if self.ongrid:
                tile_x = tile_pos[0] * self.tilemap.tile_size - self.scroll[0]
                tile_y = tile_pos[1] * self.tilemap.tile_size - self.scroll[1]
                self.display.blit(current_tile, (tile_x, tile_y))
            else:
                self.display.blit(current_tile, mouse_pos)

            # Handle tile placement and removal
            if self.clicking and self.ongrid:
                self.tilemap.tilemap[str(tile_pos[0]) + ';' + str(tile_pos[1])] = {
                    'type': self.tile_list[self.tile_group],
                    'variant': self.tile_variant,
                    'position': tile_pos
                }
            if self.right_clicking:
                tile_location = str(tile_pos[0]) + ';' + str(tile_pos[1])
                if tile_location in self.tilemap.tilemap:
                    del self.tilemap.tilemap[tile_location]
                for tile in self.tilemap.offgrid_tiles.copy():
                    tile_img = self.assets[tile['type']][tile['variant']]
                    tile_r = pygame.Rect(tile['position'][0] - self.scroll[0], tile['position'][1] - self.scroll[1], tile_img.get_width(), tile_img.get_height())
                    if tile_r.collidepoint(mouse_pos):
                        self.tilemap.offgrid_tiles.remove(tile)

            # Display the current tile as a preview
            self.display.blit(current_tile, (5, 5))

            # Scale the display to fit the screen
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            pygame.display.update()
            self.clock.tick(60)

            for event in pygame.event.get():
                # Quit event
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # Draw on the display, also off grid
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.clicking = True
                        if not self.ongrid:
                            self.tilemap.offgrid_tiles.append({
                                'type' : self.tile_list[self.tile_group], 
                                'variant' : self.tile_variant, 
                                'position': (mouse_pos[0] + self.scroll[0], mouse_pos[1] + self.scroll[1])})
                            
                    if event.button == 3:
                        self.right_clicking = True
                    if self.shift:
                        if event.button == 4:
                            self.tile_variant = (self.tile_variant - 1) % len(self.assets[self.tile_list[self.tile_group]])
                        if event.button == 5:
                            self.tile_variant = (self.tile_variant + 1) % len(self.assets[self.tile_list[self.tile_group]])
                    else:
                        if event.button == 4:
                            self.tile_group = (self.tile_group - 1) % len(self.tile_list)
                            self.tile_variant = 0
                        if event.button == 5:
                            self.tile_group = (self.tile_group + 1) % len(self.tile_list)
                            self.tile_variant = 0

                # Mouse input
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1: # Left click
                        self.clicking = False
                    if event.button == 3: # Right click
                        self.right_clicking = False

                # Keyboard input
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        self.movement[0] = True
                    if event.key == pygame.K_d:
                        self.movement[1] = True
                    if event.key == pygame.K_w:
                        self.movement[2] = True
                    if event.key == pygame.K_s:
                        self.movement[3] = True
                    if event.key == pygame.K_g:
                        self.ongrid = not self.ongrid
                    if event.key == pygame.K_o:
                        self.tilemap.save_map('map.json')
                    if event.key == pygame.K_LSHIFT:
                        self.shift = True
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_a:
                        self.movement[0] = False
                    if event.key == pygame.K_d:
                        self.movement[1] = False
                    if event.key == pygame.K_w:
                        self.movement[2] = False
                    if event.key == pygame.K_s:
                        self.movement[3] = False
                    if event.key == pygame.K_LSHIFT:
                        self.shift = False

# Run the game
Game().run()
