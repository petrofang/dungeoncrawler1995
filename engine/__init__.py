"""
DungeonCrawler1985 Game Engine Package
--------------------------------------
Game engine for the dungeon crawler game.
"""

__version__ = '0.1.0'
__author__ = 'Giles Cooper'

from .io import IOHandler, ConsoleIO, Parser

# Explicitly declare public API
__all__ = [
    'IOHandler',        # Base IO handler class
    'ConsoleIO',        # Console IO handler class
    'Parser'            # Command parser class
]
