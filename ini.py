# Description: This file contains the configuration for the game.
STARTING_ROOM = 0

__version__ = '0.1.0'
__author__ = 'Giles Cooper'
__license__ = 'MIT'
__status__ = 'Development'  # can be 'Development', 'Production', 'Beta', etc.
__url__ = 'https://github.com/petrofang/dungeoncrawler1995'
__description__ = 'A text-based multi-user dungeon (MUD) game'
__requires__ = [
    'sqlalchemy>=2.0.0',  # Using newer SQLAlchemy features
    'pymssql>=2.2.0',     # For MS SQL Server connection
    'passlib>=1.7.4',     # For password hashing
    'typing_extensions>=4.0.0',  # For type hints
    'python-dotenv>=1.0.0'  # Suggested for handling .env files with DB credentials
]

splash_art = f'''

        ██████╗ ██╗   ██╗███╗   ██╗ ██████╗ ███████╗ ██████╗ ███╗   ██╗
        ██╔══██╗██║   ██║████╗  ██║██╔════╝ ██╔════╝██╔═══██╗████╗  ██║
        ██║  ██║██║   ██║██╔██╗ ██║██║  ███╗█████╗  ██║   ██║██╔██╗ ██║
        ██║  ██║██║   ██║██║╚██╗██║██║   ██║██╔══╝  ██║   ██║██║╚██╗██║
        ██████╔╝╚██████╔╝██║ ╚████║╚██████╔╝███████╗╚██████╔╝██║ ╚████║
        ╚═════╝  ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝ ╚══════╝ ╚═════╝ ╚═╝  ╚═══╝
 ██████╗██████╗  █████╗ ██╗    ██╗██╗     ███████╗██████╗   ╖╓─╖╓─╖╓─╴
██╔════╝██╔══██╗██╔══██╗██║    ██║██║     ██╔════╝██╔══██╗  ║╙─╢╙─╢╙─╮
██║     ██████╔╝███████║██║ █╗ ██║██║     █████╗  ██████╔╝  ╨  ╜  ╜╰─╯        
██║     ██╔══██╗██╔══██║██║███╗██║██║     ██╔══╝  ██╔══██╗ a multi-user     
╚██████╗██║  ██║██║  ██║╚███╔███╔╝███████╗███████╗██║  ██║ dungeon game 
 ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚══╝╚══╝ ╚══════╝╚══════╝╚═╝  ╚═╝ 
'''



'''
Reference: ASCII Box Drawing Characters
═   ║   ╬   ╔   ╗   ╚   ╝   ╠   ╣   ╦   ╩
        ╪   ╒   ╕   ╘   ╛   ╞   ╡   ╤   ╧
        ╫   ╓   ╖   ╙   ╜   ╟   ╢   ╥   ╨
─   │   ┼   ┌   ┐   └   ┘   ├   ┤   ┬   ┴
╌   ╎   			        ╶   ╴   ╷   ╵
┄   ┆
┈   ┊
╭   ╮
╰   ╯
╱   ╲   ╳	
►   ◄   ▲   ▼
'''
