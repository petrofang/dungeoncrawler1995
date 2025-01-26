from abc import ABC, abstractmethod
from orm import Player, SQL
from ini import STARTING_ROOM
from .parser import Parser
from .exceptions import Quit

class IOHandler(ABC):
    """Base class for handling input/output operations in the game."""
    
    def __init__(self, parser: Parser):
        """Initialize with a command parser."""
        self.parser = parser

    def start_session(self) -> None:
        """Start a game session - authenticate and begin command loop."""
        if player := self.authenticate():
            # attach the io handler to the player object:
            player.io = self
            self.listen(player)

    def authenticate(self) -> Player|None:
        """Authenticate player and return Player object or None."""
        while True:
            choice = self.input("[L]ogin or [C]reate character? ")
            
            match choice.lower():
                case "l":
                    if player := self._login():
                        return player
                case "c":
                    return self._create_player()
                case "q":
                    return None
    
    def listen(self, player: Player) -> None:
        """Main command loop - get input and pass to parser."""
        try:
            while True:
                command = self.input()
                self.parser.parse(player, command)
        except Quit:
            self.print("Goodbye!")
            # Here we could do cleanup if needed
            return

    @abstractmethod
    def print(self, message: str) -> None:
        """Display output to the user."""
        pass

    @abstractmethod
    def input(self, prompt: str|None = None) -> str:
        """Get input from the user."""
        pass

    def _login(self) -> Player|None:
        """Handle login flow."""
        username = self.input("Username: ").lower()
        password = self.input("Password: ")
        
        if player := SQL.query(Player).filter_by(username=username).first():
            if player.check_password(password):
                return player
        self.print("Invalid username or password")
        return None

    def _create_player(self) -> Player:
        """Handle new player creation flow."""
        while True:
            username = self.input("Choose username: ").lower()
            if not SQL.query(Player).filter_by(username=username).first():
                break
            self.print("Username taken")
        
        name = username.capitalize()
        password = self.input("Choose password: ")
        
        player = Player(
            username=username,
            name=name,
            description=f"A brave adventurer known as {name}",
            article=False,
            owner_id=STARTING_ROOM,
        )
        player.set_password(password)
        SQL.add(player)
        SQL.commit()
        return player

class ConsoleIO(IOHandler):
    """Implementation of IOHandler for console-based interaction."""
    
    def print(self, message: str = '', **kwargs) -> None:
        print(message, **kwargs)

    def input(self, prompt: str|None = None) -> str:
        return input(prompt or " > ").strip().lower()

class RemoteIO(IOHandler):
    """Stub implementation of IOHandler for remote connections."""
    
    def print(self, message: str) -> None:
        raise NotImplementedError

    def input(self, prompt: str|None = None) -> str:
        raise NotImplementedError

if __name__ == "__main__":
    print("This module is not meant to be run directly. use main.py instead.")