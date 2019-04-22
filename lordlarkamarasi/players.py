from dataclasses import dataclass, field
from collections import UserDict
from lordlarkamarasi.sprites import Player

@dataclass
class Coordinates:
    x: int = 0
    y: int = 0
    
    def __repr__(self):
        return f"{self.y}:{self.x}"
@dataclass
class Player:
    username: str
    coord: Coordinates = field(default_factory=Coordinates, repr=False)
    player: Player = field(default_factory=Player, repr=False)
    
class PlayerRegistery(UserDict):
    def __init__(self, sprite_hook, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.sprite_hook = sprite_hook
    def join(self, username):
        self.data[username] = Player(username)
        self.sprite_hook.add(self.data[username].player)
        return self.data[username]
        
    def quit(self, username):
        self.sprite_hook.remove(self.data[username].player)
        del self.data[username]
