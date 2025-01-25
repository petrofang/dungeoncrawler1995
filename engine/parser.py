from typing import TYPE_CHECKING

from commands import CommandList

if TYPE_CHECKING:
    from .io import IOHandler
    from orm import Player

class Parser:
    """Handles parsing and executing game commands."""
    
    def parse(self, player: 'Player', command: str) -> None:
        """Parse and execute a game command."""
        if not command:
            player.io.print('Huh?\n')   
            return
            
        verb, *args = command.split()
        arg = " ".join(args) if args else None
        target = arg # target acquisition is handled by each command handler
        
        command_action = getattr(CommandList, verb, None)
        if command_action: 
            command_action(player=player, arg=arg, target=target)                
        else:                 
            player.io.print(f'Unknown command "{command}".')