from typing import TYPE_CHECKING

from commands import CommandList

if TYPE_CHECKING:
    from .io import IOHandler
    from orm import Player

class Parser:
    """Handles parsing and executing game commands."""
    
    def parse(self, player: 'Player', command: str) -> bool:
        """
        This is the command parser, the first link in the chain of command
        where player input is parsed and converted into game action. Here,
        user input is split into a command and an argument. Then, the command
        is checked against the CommandList and (if a command is found) the
        argument is sent for further parsing, sanitizing, and execution.

        Args:
            player: Player issuing the command
            command: Command string to parse
            
        Returns:
            bool: False if game should quit, True to continue
        """
        if not command:
            player.io.print('Huh?\n')   
            return True
        verb, *args = command.split()
        arg = " ".join(args) if args else None
        target = arg # target acquisition is handled by each command handler
        command_action = getattr(CommandList, command, None)
        if command_action: 
            command_action(player=player, arg=arg, target=target)                
        else:                 
            player.io.print(f'Unknown command "{command}".')
  
        return True