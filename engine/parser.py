from typing import TYPE_CHECKING

from commands import AliasList, CommandList

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
        # TODO: really? I think we can do better than this. Let's try and parse targets before command
        # however, it depends on the command. Some commands may not require a target, or
        # some commands may require a particular target type. Note that all targets are ultimately
        # inherited from GameObject, so we can always check the type of the target, or maybe even
        # have some intentionally unexpected behavior if the target is not of the expected type.
        # either way it would be ideal to move target parsing into the parser module.

        command_action = getattr(CommandList, verb, None)
        alias_action = getattr(AliasList, verb, None)

        if command_action: 
            command_action(player=player, arg=arg, target=target)                
        elif alias_action:
            alias_action(player=player, arg=arg, target=target)
        else:                 
            player.io.print(f'Unknown command "{command}".')