import itertools
import random
import time
from collections import UserList
from contextlib import suppress
from typing import Tuple

import pygame
from pygame.locals import QUIT

from lordlarkamarasi.textures import AVAILABLE_BLOCKS, TILE_SIZE, Blocks


class Map(UserList):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.data = list(
            list(itertools.repeat(Blocks.GRASS, width)) for _ in range(height)
        )
        self._shake_map()

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
        self.map = Map(*(meter // 25 for meter in window))

    def process_event(self, event: pygame.event.EventType):
        self.draw_map()

    def event_handler(self, interval: int = 0.005):
        event = pygame.event.wait()
        while event.type is not QUIT:
            self.process_event(event)
            pygame.display.update()
            time.sleep(interval)
        else:
            pygame.quit()

    def start(self):
        self.event_handler()

    def draw_map(self):
        for rpos, row in enumerate(self.map):
            for cpos, block in enumerate(row):
                self.surface.blit(
                    block.value.texture, (cpos * TILE_SIZE, rpos * TILE_SIZE)
                )


if __name__ == "__main__":
    game = Game()
    game.start()
