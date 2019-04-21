from dataclasses import dataclass, field
from collections import UserDict

@dataclass
class Coordinates:
    x: int = 0
    y: int = 0
    
@dataclass
class Player:
    username: str
    coord: Coordinates = field(default_factory=Coordinates)
        
class PlayerRegistery(UserDict):
    def join(self, username):
        self.data[username] = Player(username)
    
    def quit(self, username):
        del self.data[username]
