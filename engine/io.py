from abc import ABC, abstractmethod
from orm import Player, SQL
from ini import STARTING_ROOM



class IOHandler(ABC):
    def __init__(self, parser: 'Parser'):
        self.parser = parser

    def authenticate(self) -> Player|None:
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
    
    def _login(self) -> Player|None:
        username = self.input("Username: ")
        password = self.input("Password: ")
        
        if player := SQL.query(Player).filter_by(username=username).first():
            if player.check_password(password):
                return player
        self.output("Invalid username or password")
        return None

    def _create_player(self) -> Player:
        while True:
            username = self.input("Choose username: ")
            if not SQL.query(Player).filter_by(username=username).first():
                break
            self.output("Username taken")
        
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
              
    def listen(self, player) -> None:
        """Start listening for commands and pass them to parser"""

        while True:
            command = self.input()
            if not self.parser.parse(self, player, command):
                break
  
    @abstractmethod
    def output(self, message: str) -> None:
        pass

    @abstractmethod
    def input(self, prompt: str|None = None) -> str:
        pass

class ConsoleIO(IOHandler):
    def output(self, message: str) -> None:
        print(message)

    def input(self, prompt: str|None = None) -> str:
        return input(prompt or " > ").strip().lower()
    

# TODO: Implement other IOHandlers as needed (for example, a telnet handler)


class Parser:
    def parse(self, io: IOHandler, player: Player, command: str) -> bool:
        """Parse and handle a command. Return False to quit."""
        if not command:
            return True
            
        verb, *args = command.split()
        
        match verb:
            case "quit" | "q":
                io.output("Goodbye!")
                return False
            case "look" | "l":
                io.output(player.owner.look(player))
            case _:
                io.output("I don't understand that.")
        return True

# Usage would be like:
# parser = Parser()
# io = ConsoleIO(parser)
# io.listen()
