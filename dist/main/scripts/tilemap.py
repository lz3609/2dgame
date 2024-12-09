import json
import pygame

# Offsets to check neighboring tiles (8 directions around a tile)
NEIGHBOR_OFFSETS = [
    (-1, 0),   # Left
    (-1, -1),  # Top-left
    (0, -1),   # Top
    (1, -1),   # Top-right
    (1, 0),    # Right
    (0, 0),    # Center
    (-1, 1),   # Bottom-left
    (0, 1),    # Bottom
    (1, 1)     # Bottom-right
]

# Set of tiles that are considered as physical. Decoration are not physical tiles
TILES = {'dirt', 'grass'}


class Tilemap:
    def __init__(self, game, tile_size=32):
        """
        Initializes the Tilemap object 
        """
        self.game = game
        self.tile_size = tile_size
        self.tilemap = {}  # A dictionary to store tiles by their location
        self.offgrid_tiles = []  # A list for tiles that are off the grid

    def extract(self, id_pairs, keep=False):
        """
        Extracts tiles from the tilemap and offgrid tiles based on the given type and variant pairs.
        """
        matches = []

        # Check off-grid tiles
        for tile in self.offgrid_tiles.copy():
            if (tile['type'], tile['variant']) in id_pairs:
                matches.append(tile.copy())
                if not keep:
                    self.offgrid_tiles.remove(tile)

        # Check grid tiles
        for loc in self.tilemap:
            tile = self.tilemap[loc]
            if (tile['type'], tile['variant']) in id_pairs:
                matches.append(tile.copy())
                matches[-1]['position'] = matches[-1]['position'].copy()  # Copy the position for consistency
                matches[-1]['position'][0] *= self.tile_size  # Scale position by tile size
                matches[-1]['position'][1] *= self.tile_size
                if not keep:
                    del self.tilemap[loc]

        return matches

    def tiles_around(self, position):
        """
        Returns the tiles surrounding a given position.
        """
        tiles = []
        tile_location = (int(position[0] // self.tile_size), int(position[1] // self.tile_size))  # Convert position to grid coordinates

        # Check the surrounding 8 tiles
        for offset in NEIGHBOR_OFFSETS:
            check_location = str(tile_location[0] + offset[0]) + ';' + str(tile_location[1] + offset[1])
            if check_location in self.tilemap:
                tiles.append(self.tilemap[check_location])
        return tiles

    def save_map(self, path):
        """
        Saves the current tilemap to a JSON file.
        """
        f = open(path, 'w')
        json.dump({
            'tilemap': self.tilemap,
            'tile_size': self.tile_size,
            'offgrid': self.offgrid_tiles
        }, f)
        f.close()

    def load_map(self, path):
        """
        Loads a tilemap from a JSON file.
        """
        f = open(path, 'r')
        map_data = json.load(f)
        f.close()

        self.tilemap = map_data['tilemap']
        self.tile_size = map_data['tile_size']
        self.offgrid_tiles = map_data['offgrid']

    def check_tiles(self, position):
        """
        Checks if a given position collides with any physical tiles.
        """
        tile_location = str(int(position[0] // self.tile_size)) + ';' + str(int(position[1] // self.tile_size))
        if tile_location in self.tilemap:
            if self.tilemap[tile_location]['type'] in TILES:
                return self.tilemap[tile_location]

    def get_physics_collisions_around(self, position):
        """
        Returns a list of rectangles representing the physical tiles around a position.
        """
        rects = []
        for tile in self.tiles_around(position):
            if tile['type'] in TILES:
                rects.append(pygame.Rect(
                    tile['position'][0] * self.tile_size, 
                    tile['position'][1] * self.tile_size, 
                    self.tile_size, 
                    self.tile_size
                ))
        return rects

    def render(self, surf, offset=(0, 0)):
        """
        Renders the tilemap and off-grid tiles to the given surface.
        """
        # Render off-grid tiles
        for tile in self.offgrid_tiles:
            surf.blit(self.game.assets[tile['type']][tile['variant']], 
                      (tile['position'][0] - offset[0], 
                       tile['position'][1] - offset[1]))

        # Render grid tiles
        for x in range(offset[0] // self.tile_size, 
                       (offset[0] + surf.get_width()) // self.tile_size + 1):
            for y in range(offset[1] // self.tile_size, 
                           (offset[1] + surf.get_height()) // self.tile_size + 1):
                location = str(x) + ';' + str(y)
                if location in self.tilemap:
                    tile = self.tilemap[location]
                    surf.blit(self.game.assets[tile['type']][tile['variant']], 
                              (tile['position'][0] * self.tile_size - offset[0], 
                               tile['position'][1] * self.tile_size - offset[1]))
