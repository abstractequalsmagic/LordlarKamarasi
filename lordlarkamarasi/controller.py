import itertools
import random
import time
import logging
from collections import UserList
from contextlib import suppress
from configparser import ConfigParser
from typing import Tuple

import pygame
from pygame.locals import *

from lordlarkamarasi.textures import AVAILABLE_BLOCKS, BASE_PATH, TILE_SIZE, Blocks, Entities
from lordlarkamarasi.players import PlayerRegistery

MOVE_KEYS = {K_RIGHT, K_LEFT, K_UP, K_DOWN}

class Map(UserList):
    def __init__(self, width, height, surface):
        self.width = width
        self.height = height
        self.data = surface

    @classmethod
    def from_file(cls, file):
        cfg = ConfigParser()
        cfg.read(BASE_PATH / file)
        
        meta = cfg['meta']
        width, height = meta.getint('width'), meta.getint('height')
        
        ground = cfg['ground']
        default = Blocks.get_by_id(ground.getint('default'))
        
        surface = [list(itertools.repeat(default, width)) for _ in range(height)]
        return cls(width, height, surface)
        
    def _shake_map(self):
        for _ in range((self.width * self.height) // 32):
            print(random.choice(AVAILABLE_BLOCKS))
            self._generate_group(random.choice(AVAILABLE_BLOCKS))

    def _generate_group(self, group):
        row_start = random.randint(0, self.height)
        width_start = random.randint(0, self.width)
        size = round((self.width * self.height) // 113)

        self.data[row_start - 1][width_start - 1] = group
        with suppress(IndexError):
            for row in range(row_start, row_start + size):
                for column in range(width_start, width_start + size):
                    if random.randint(0, 3):  # %75
                        self.data[row][column] = group


class Game:
    def __init__(self, window: Tuple[int, int] = (800, 800)):
        pygame.init()
        pygame.display.set_caption("Lordlar Kamarası")

        self.surface = pygame.display.set_mode(window)
        self.map = Map.from_file('maps/base_map.ini')
        
        self.playerreg = PlayerRegistery()
        self.player = self.playerreg.join("BTaskaya")
        
        self.logger = logging.getLogger('Game')
    def process_event(self, event: pygame.event.EventType):
        if event.type is MOUSEMOTION:
            x, y = event.rel
            if x > 0 and self.player.coord.x <= self.map.width:
                self.player.coord.x += 1
            elif x < 0 and self.player.coord.x > self.map.width:
                self.player.coord.x -= 1
            
            if y > 0 and self.player.coord.y <= self.map.height:
                self.player.coord.y += 1
            elif y < 0 and self.player.coord.y > self.map.height:
                self.player.coord.y -= 1
                
        self.draw_map()
        pygame.display.update()
        
    def event_handler(self):
        event = pygame.event.wait()
        while event.type is not QUIT:
            self.logger.info(f"Event handled: {event}")
            self.process_event(event)
            event = pygame.event.wait()
        else:
            pygame.quit()

    def start(self):
        self.event_handler()
    
    def draw_map(self):
        self.logger.info(f"Drawing surface to {self.map.width * self.map.height} tiles")
        
        for rpos, row in enumerate(self.map):
            for cpos, block in enumerate(row):
                self.surface.blit(
                    block.value.texture, (cpos * TILE_SIZE, rpos * TILE_SIZE)
                )
                
        self.logger.info(f"Drawing {len(self.playerreg)} players")
        for player in self.playerreg.values():
            self.surface.blit(Entities.PLAYER.value.texture, (player.coord.x * TILE_SIZE, player.coord.y * TILE_SIZE))
            
if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    game = Game()
    game.start()
