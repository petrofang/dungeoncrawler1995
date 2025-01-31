from typing import List

from engine.commands import AliasList, CommandList
from orm import Player, GameObject, Room, Item, Creature, Exit

class Parser:
    """Handles parsing and executing game commands."""
    
    def parse(self, player: Player, command_str: str) -> None:
        """Parse and execute a game command."""
        if not command_str:
            player.io.print('Huh?\n')   
            return

        if command_str[0] == "'":
            command_str = 'say ' + command_str[1:]

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

        target = find_target(player, valid_target_types, arg, mine)

        
        if command: 
            command(player=player, arg=arg, target=target)                
        elif alias:
            alias(player=player, arg=arg, target=target)
        else:                 
            player.io.print(f'Unknown command "{command}".')
            player.io.print('Type "help" for a list of commands.\n')


def find_target(player:Player, target_types:List[type], arg:str, mine:bool=False) -> GameObject:
    """Parse a target from the player's current room or inventory.
    
    Args:
        player: The player looking for the target
        target_types: List of valid target classes (Item, Creature, etc)
        arg: Name of target to find
        mine: Whether to search inventory instead of room
    """
    if not arg:
        return None
    
    if arg in ['me', 'myself']:
        return player
    
    if mine:
        for item in player.inventory:
            if item.name == arg and any(isinstance(item, t) for t in target_types):
                return item
        else:
            player.io.print(f'I cannot find your "{arg}".')
            return None
        
    for object in player.room.inventory:
        if object.name == arg and any(isinstance(object, t) for t in target_types):
            return object
        
    for object in player.inventory:
        if object.name == arg and any(isinstance(object, t) for t in target_types):
            return object

    return None
