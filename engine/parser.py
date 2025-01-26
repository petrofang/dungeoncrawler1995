from typing import List

from commands import AliasList, CommandList
from orm import Player, GameObject, Room, Item, Creature, Exit

class Parser:
    """Handles parsing and executing game commands."""
    
    def parse(self, player: Player, command_str: str) -> None:
        """Parse and execute a game command."""
        if not command_str:
            player.io.print('Huh?\n')   
            return
            
        verb, *args = command_str.split()
     
        mine = False
        preposition = None
        article = None
        command = getattr(CommandList, verb, None)
        alias = getattr(AliasList, verb, None)

        if not command and not alias: 
            player.io.print(f"Command '{command_str}' not found")
            return
        else:
            valid_target_types = command.__target_types__ if command else alias.__target_types__

        if args:
            # check for prepositions
            if args[0] in ['at', 'to', 'with', 'in', 'on', 'under']:
                preposition = args[0] 
                args = args[1:]
            if args[0] in ['the', 'a', 'an']:
                article = True
                args = args[1:]
            elif args[0] in ['my']:
                mine = True
                args = args[1:]
            arg= ' '.join(args)
        else:
            arg = None
    
        if mine:
            if arg not in [inv.name for inv in player.inventory]:
                player.io.print(f'I cannot find your "{arg}".')
                return
    
        target = arg # target acquisition is handled by each command handler
        # TODO: really? I think we can do better than this. Let's try and parse targets before command
        # however, it depends on the command. Some commands may not require a target, or
        # some commands may require a particular target type. Note that all targets are ultimately
        # inherited from GameObject, so we can always check the type of the target, or maybe even
        # have some intentionally unexpected behavior if the target is not of the expected type.
        # either way it would be ideal to move target parsing into the parser module.


        if command: 
            command(player=player, arg=arg, target=target)                
        elif alias:
            alias(player=player, arg=arg, target=target)
        else:                 
            player.io.print(f'Unknown command "{command}".')
            player.io.print('Type "help" for a list of commands.\n')

def find_target(player:Player, target_types:List[object], arg:str, mine:bool=False) -> GameObject:
    """Parse a target from the player's current room."""
    if not arg:
        return None
    if arg in ['me', 'myself']:
        return player
    
    room = player.room
    target = None
    for target_type in target_types:
        match target_type:
            case [Room]:
                print('room')
            case [Item]:
                print('item')
            case [Creature]:
                print('creature')
            case [Exit]:
                print('exit')
            case _:
                print('unknown')
    return target
    