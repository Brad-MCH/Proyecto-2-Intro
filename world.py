from constants import *

class World:
    def __init__(self):
        self.map_tiles = []

    def load_map(self, map_data, tile_list):
        
        #? self.level_length = len(map_data)

        for y, row in enumerate(map_data):
            for x, tile in enumerate(row):
                img = tile_list[tile]
                img_rect = img.get_rect()   
                img_rect.x = x * TILE_SIZE
                img_rect.y = y * TILE_SIZE
                img_rect.center = (img_rect.x, img_rect.y)
                tile_data = [img, img_rect, img_rect.x, img_rect.y]

                # Add image data to the main tiles list
                if tile >= 0:
                    self.map_tiles.append(tile_data)

    def update(self, screen_scroll):
        for tile in self.map_tiles:
            tile[2] += screen_scroll[0]
            tile[3] += screen_scroll[1]
            tile[1].center = (tile[2], tile[3])

    def draw(self, screen):
        for tile in self.map_tiles:
            screen.blit(tile[0], tile[1])
            
        
