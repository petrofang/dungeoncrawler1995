from orm import Player, Creature, Item

class CommandList():
    ''' 
    This is the master list of all player commands outside of combat,
    as well as being the command handler for each command.
    
    The command handlers further parse and sanitize command arguments,
    then determine the target with find_target() before sending 
    PAAT (Player, Action, Arguments, Target) to be performed by the
    actions module (actions.py) with:
        actions.do(P,A,A,T)

    Generally speaking, commands which do not change anything or cause
    any interaction with other game objects, mobiles or players can
    be parsed directly by the command and are not sent to do(PAAT).
        eg., checking inventory or looking.
    
    format:
    
    def command(player:Mobile=None, arg:str=None, target=None):
        """ 
        docstring - displayed by help <command>
        """
        action="action"
        # command logic
        actions.do(player, action, arg, target)     
    '''

    def __no_dunders(arg:str, **kwargs): 
        ''' A filter to show only public commands on the help list.'''
        return not arg.startswith('_')

    def help(player:Player = None, arg:str = None, target=None, **kwargs):
        ''' 
        help           - get a list of commands.
        help <command> - show help for a command.
        '''
        list_of_commands = sorted(filter(CommandList.__no_dunders, 
                                         vars(CommandList)))
        if arg == None:
            player.io.print(CommandList.help.__doc__)
            player.io.print(' --- Command List ---')
            for each in list_of_commands:
                player.io.print(f'    {each}',end=' ')
            player.io.print()
        elif arg in list_of_commands:
            help_command = getattr(CommandList, arg)
            player.io.print(help_command.__doc__)       
        else: player.io.print(f'Unknown command "{arg}".')

    def look(player:Player = None, arg:str = None, **kwargs):
        """
        look - look at your surroundings
        look <target> - look at target
        look in <container> - look inside a container 
        """
        if arg==None: 
            pass
        player.io.print(player.room.view(player))
        # TODO: look at target
        '''
        elif arg.startswith("in "):
            arg=arg[3:]
            target=find_target(player, arg, Item, in_room=True, in_inventory=True)
            if target and target.type == "container":
                target.look_in(player)
            else:
                player.print("You cannot see inside that.")
        elif player.room.signs and arg in player.room.signs.keys():
            player.print(player.room.signs[arg])
        else:
            target=find_target(player, arg, in_room=True, 
                               in_inventory=True, in_equipment=True)
            if target is not None:
                target.look(player)
            elif player.room.exit(arg): 
                player.room.exit(arg).look(player)
            else:
                player.print(f"You see no '{arg}'.")
        '''
    l=look


def find_target(player:Player, arg:str, type=None, in_room=False, in_inventory=False,
                in_equipment=False, in_exits=False, in_containers=False, **kwargs):
    """
    This function searches for a target item, mobile, or exit by keyword 
    and returns the game object if found, or None. 
        arguments:
            player - the player with whom the search is associated
            arg - the keyword or name of the item being searched
            type - Object, Mobile, or None, where None means either/both
            in_room - search in the player's room. If type=Mobile, the
                room will be searched even if in_room=False
            in_inventory - search in the player's inventory.
            in_equipment - search in the player's equipment.
            in_containers - search in containers in myself's room and inventory.
            in_exits - search for exits in the player's room.
    """
    # TODO: fuzzywuzzy? .like()?
    target = None
    if type is Creature or type is None: # not an object
        for mobile in player.room.mobiles:
            if mobile.name.startswith(arg) and mobile is not player: 
                target = mobile
            else:
                names=mobile.name.split()
                for name in names:
                    if name.startswith(arg):
                        target = mobile
        if target: return target
    if type is Item or type is None: # and if it's not a mobile it must be an object or None
        if in_room:
            for item in player.room.inventory:
                if item.name.startswith(arg):    
                    target = item
                else:
                    names=item.name.split()
                    for name in names:
                        if name.startswith(arg):
                            target = item
            if target: return target            
        if in_inventory:
            for item in player.inventory:
                if item.name.startswith(arg): 
                    target = item
                else:
                    names=item.name.split()
                    for name in names:
                        if name.startswith(arg):
                            target = item
            if target: return target
        if in_equipment:
            for item in [item for item in player.equipment.values() if item is not None]:
                if item.name.startswith(arg): 
                    target = item
                else:
                    names=item.name.split()
                    for name in names:
                        if name.startswith(arg):
                            target = item
            if target: return target
        if in_containers:
            for item in player.room.inventory:
                if item.contents:
                    for thing in item.contents:
                        if thing.name.startswith(arg):
                            target=thing
            if target: return target
            for item in player.inventory:
                if item.contents:
                    for thing in item.contents:
                        if thing.name.startswith(arg):
                            target=thing
            if target: return 

    if type is None:                        
        if in_exits:
            for exit in player.room.exits:
                if exit.direction == arg:
                    target = exit
        return target
    return target