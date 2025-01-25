"""
DungeonCrawler1985 Game Engine Package
--------------------------------------
Game engine for the dungeon crawler game.
"""

from ini import __author__, __version__

from .io import IOHandler, ConsoleIO
from .parser import Parser

# Explicitly declare public API
__all__ = [
    'IOHandler',        # Base IO handler class
    'ConsoleIO',        # Console IO handler class
    'Parser'            # Command parser class
]
