from dataclasses import dataclass, field
from collections import UserDict

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
        
class PlayerRegistery(UserDict):
    def join(self, username):
        self.data[username] = Player(username)
        return self.data[username]
        
    def quit(self, username):
        del self.data[username]
