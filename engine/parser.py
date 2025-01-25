from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .io import IOHandler
    from orm import Player

class Parser:
    """Handles parsing and executing game commands."""
    
    def parse(self, io: 'IOHandler', player: 'Player', command: str) -> bool:
        """
        Parse and execute a game command.
        
        Args:
            io: IOHandler instance for input/output
            player: Current player
            command: Command string to parse
            
        Returns:
            bool: False if game should quit, True to continue
        """
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
