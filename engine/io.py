from abc import ABC, abstractmethod
import socket

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

class TelnetIO(IOHandler):
    """Implementation of IOHandler for telnet connections."""
    
    # Telnet protocol bytes
    IAC  = bytes([255]) # Interpret As Command
    DONT = bytes([254])
    DO   = bytes([253])
    WONT = bytes([252])
    WILL = bytes([251])
    
    def __init__(self, parser: Parser, connection: socket.socket):
        super().__init__(parser)
        self.connection = connection
        self.buffer = bytearray()
        
    def print(self, message: str = '', **kwargs) -> None:
        """Send output to telnet client with preserved formatting."""
        try:
            # Split message into lines to preserve exact formatting
            lines = message.splitlines() or ['']  # Handle empty strings
            
            # Handle end= parameter for prompts
            if kwargs.get('end', '\n') == '':
                # Single line without newline (prompt)
                self.connection.send(message.encode())
            else:
                # Full message with preserved line breaks
                output = []
                for line in lines:
                    output.append(line)
                    output.append('\r\n')  # Explicit newline after each line
                self.connection.send(''.join(output).encode())
                
        except Exception as e:
            print(f"Error sending to client: {e}")
        
    def input(self, prompt: str|None = None) -> str:
        """Get input from telnet client."""
        try:
            if prompt:
                self.print(prompt, end='')
            else:
                self.print(" >> ", end='')  # Added default prompt
            
            line = ''
            self.buffer.clear()
            
            while True:
                byte = self.connection.recv(1)
                if not byte:
                    raise ConnectionError("Client disconnected")
                
                # Handle telnet protocol commands
                if byte == self.IAC:
                    cmd = self.connection.recv(1)
                    opt = self.connection.recv(1)
                    continue
                
                # Handle normal input
                if byte == b'\r':
                    continue
                if byte == b'\n':
                    self.connection.send(b'\r\n')  # Move to next line
                    return line.strip().lower()
                
                # Handle backspace
                if byte == b'\x7f' or byte == b'\x08':
                    if line:
                        line = line[:-1]
                        # Erase character from screen
                        self.connection.send(b'\x08 \x08')
                    continue
                
                # Add printable characters to line
                if byte.isascii() and not byte[0] > 127:
                    char = byte.decode()
                    line += char
                    # Echo character back
                    self.connection.send(byte)
                    
        except Exception as e:
            print(f"Error receiving from client: {e}")
            raise

if __name__ == "__main__":
    print("This module is not meant to be run directly. use main.py instead.")