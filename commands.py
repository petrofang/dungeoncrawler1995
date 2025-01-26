from orm import GameObject, Creature, Player, Item, Room, Exit
from engine import Quit

def target_types(*target_types):
    ''' 
    This decorator is used to indicate the intended target types of a command.
    '''
    def decorator(func):
        func.__target_types__ = target_types
        return func
    return decorator

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
    
    def command(player:Creature, arg:str=None, target=None):
        """ 
        docstring - displayed by help <command>
        """
        action="action"
        # command logic
        actions.do(player, action, arg, target)     
    '''

    @staticmethod
    def __no_dunders(arg:str, **kwargs): 
        ''' A filter to show only public commands on the help list.'''
        return not arg.startswith('_')
    
    @target_types(None)
    def inventory(player:Player, **kwargs):
        ''' 
        inventory   - Check inventory and equipment. 
        inv         - Alias for inventory.
        '''
        # list equipped items:
        # CommandList.equip(subject)

        # list inventory items:
        s = '' if player.name[-1] == 's' else 's'
        title = (f'  {str(player.name).capitalize()}\'{s} Inventory  ')
        title = f'{title:^30}'
        player.io.print('─'*len(title))
        player.io.print(title)
        player.io.print('─'*len(title))
        if player.inventory: 
            for each_item in player.inventory:
                player.io.print(each_item)
        else: player.io.print('None')
        player.io.print()

    @target_types(None)
    def help(player: Player, arg: str=None, **kwargs):
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

    @target_types(GameObject, Exit, None)
    def look(player:Player, target:GameObject = None, **kwargs):
        """
        look - look at your surroundings
        look <target> - look at target
        look in <container> - look inside a container 
        """
        if target == None:
            player.io.print(player.room.view(player))
        # TODO: preposition handling, kwargs[preposition] == 'in', etc
        else:
            player.io.print(target.description)
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
        return True

    @target_types(None)
    def quit(player: Player, **kwargs):
        """
        quit    - disconnect from the game
        """
        raise Quit()
        
    @target_types(None)    
    def go(player:Player, arg: str=None, **kwargs): 
        """ 
        go <direction>  - move into the next room in <direction>
        for cardinal directions you can just type the direction, eg:
        <north|east|south|west|[etc.]> or <N|NE|E|SE|S|SW|W|NW>
        """
        action = "go"
        if not arg:
            player.io.print("Go where?")
            return
        go_exit = None
        dir = arg
        if dir=='n':dir='north'
        if dir=='ne':dir='northeast'
        if dir=='e':dir='east'
        if dir=='se': dir='southeast'
        if dir=='s':dir='south'
        if dir=='sw':dir='southwest'
        if dir=='w':dir='west'
        if dir=='nw':dir='northwest'
        for exit in player.room.exits:
            if exit.direction==dir: 
                way = exit
                break
        else: 
            player.io.print(f"Exit not found in direction '{dir}'")
            return
        if way:
            player.io.print(f"You go {way.direction}.")
            player.room = way.to_room
            player.io.print(player.room.view(player))
#        actions.do(subject, action, dir)


class AliasList():
    ''' 
    This is the master list of all player command aliases.
    '''
    l = CommandList.look    
    inv = CommandList.inventory
    
    @target_types(None)
    def north(player:Player, **kwargs):
        ''' alias for GO NORTH.'''
        CommandList.go(player, 'north')
    
    @target_types(None)    
    def northeast(player:Player, **kwargs):
        ''' alias for GO NORTHEAST.'''
        CommandList.go(player, 'northeast')
        
    @target_types(None)
    def east(player:Player, **kwargs):
        ''' alias for GO EAST.'''
        CommandList.go(player, 'east')
        
    @target_types(None)
    def southeast(player:Player, **kwargs):
        ''' alias for GO SOUTHEAST.'''
        CommandList.go(player, 'southeast')
        
    @target_types(None)
    def south(player:Player, **kwargs):
        ''' alias for GO SOUTH.'''
        CommandList.go(player, 'south')
        
    @target_types(None)
    def southwest(player:Player, **kwargs):
        ''' alias for GO SOUTHWEST.'''
        CommandList.go(player, 'southwest')
        
    @target_types(None)
    def west(player:Player, **kwargs):
        ''' alias for GO WEST.'''
        CommandList.go(player, 'west')
        
    @target_types(None)
    def northwest(player:Player, **kwargs):
        ''' alias for GO NORTHWEST'''
        CommandList.go(player, 'northwest')
        
    @target_types(None)
    def up(player:Player, **kwargs):
        ''' alias for GO UP.'''
        CommandList.go(player, 'up')
        
    @target_types(None)
    def down(player:Player, **kwargs):
        ''' alias for GO DOWN.'''
        CommandList.go(player, 'down')
        
    @target_types(None)
    def out(player:Player, **kwargs):
        ''' alias for GO OUT.'''
        CommandList.go(player, 'out')
    
    d=down
    u=up
    n=north
    ne=northeast
    e=east
    se=southeast
    s=south
    sw=southwest
    w=west
    nw=northwest