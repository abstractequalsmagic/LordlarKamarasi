import os
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Optional

import pygame

BASE_PATH = Path(__file__).parent


def relative_load(path: str) -> pygame.Surface:
    return pygame.image.load(os.fspath(BASE_PATH / path))


@dataclass
class Block:
    id: int
    texture: pygame.Surface
    must_connect: Optional[id] = None


class Blocks(Enum):
    STONE = Block(0, relative_load("textures/land/stone.png"))
    GRASS = Block(1, relative_load("textures/land/grass.png"))
    WATER = Block(2, relative_load("textures/land/water.png"))
    SAND = Block(3, relative_load("textures/land/sand.png"))


AVAILABLE_BLOCKS = list(
    filter(lambda block: not block.value.must_connect, Blocks.__members__.values())
)
MUST_CONNECT_BLOCKS = list(
    filter(lambda block: block.value.must_connect, Blocks.__members__.values())
)  # use set substractions
TILE_SIZE = 25
