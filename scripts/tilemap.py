import pygame

NEIGHBOR_OFFSETS = [(-1, -0),(-1, -1),(0, -1),(1, -1),(1, 0),(0,0),(-1, 1),(0, 1),(1, 1)]
PHYSICS_TILES = {'platform', 'platform1'}

class Tilemap:
    def __init__(self, game, tile_size=16):
        self.game = game
        self.tile_size = tile_size
        self.tilemap = {}
        self.offgrid_tiles = []

        for i in range(20):
            self.tilemap[f'{3 + i};10'] = {
                'type': 'platform',
                'variant': 0,
                'pos': (3 + i, 10) 
            }
            self.tilemap[f'22;{5 + i}'] = {
                'type': 'platform1',
                'variant': 0,
                'pos': (22, 5 + i)
            }

    def tiles_around(self, pos):
        tiles = []
        tile_x = int(pos[0] // self.tile_size)
        tile_y = int(pos[1] // self.tile_size)
        
        for offset in NEIGHBOR_OFFSETS:
            check_x = tile_x + offset[0]
            check_y = tile_y + offset[1]
            check_location = f'{check_x};{check_y}'
            if check_location in self.tilemap:
                tiles.append(self.tilemap[check_location])
        return tiles

    def physics_rect(self, pos):
        rects = []
        for tile in self.tiles_around(pos):
            if tile['type'] in PHYSICS_TILES:
                rect_x = tile['pos'][0] * self.tile_size
                rect_y = tile['pos'][1] * self.tile_size
                rects.append(pygame.Rect(rect_x, rect_y, self.tile_size, self.tile_size))
        return rects
    
    def render(self, surf):
        for tile in self.offgrid_tiles:
            surf.blit(self.game.assets[tile['type']][tile['variant']], tile['pos'])
        
        for location in self.tilemap:
            tile = self.tilemap[location]
            pos_x = tile['pos'][0] * self.tile_size
            pos_y = tile['pos'][1] * self.tile_size
            surf.blit(self.game.assets[tile['type']][tile['variant']], (pos_x, pos_y))

