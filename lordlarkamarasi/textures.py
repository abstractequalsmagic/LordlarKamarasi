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
class Texture:
    id: int
    texture: pygame.Surface
    must_connect: Optional[id] = None

class Blocks(Enum):
    GRASS = Texture(0, relative_load("textures/land/grass.png"))
    STONE = Texture(1, relative_load("textures/land/stone.png"))
    WATER = Texture(2, relative_load("textures/land/water.png"))
    SAND = Texture(3, relative_load("textures/land/sand.png"))

    @classmethod
    def get_by_id(cls, id):
        block, = filter(lambda member: member.value.id == id, cls.__members__.values())
        return cls(block)

ALL_BLOCKS = set(Blocks.__members__.values())
AVAILABLE_BLOCKS = set(filter(lambda block: not block.value.must_connect, ALL_BLOCKS))
MUST_CONNECT_BLOCKS = ALL_BLOCKS - AVAILABLE_BLOCKS
TILE_SIZE = 25
