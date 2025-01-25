"""
DungeonCrawler1985 ORM Package
-----------------------------
Database models and SQLAlchemy setup for the dungeon crawler game.
"""

__version__ = '0.1.0'
__author__ = 'Giles Cooper'

from .models import Base, Room, Exit, SQL

# Explicitly declare public API
__all__ = [
    'SQL',     # Session instance for database access
    'Base',    # SQLAlchemy declarative base
    'Room',    # Room model for dungeon locations
    'Exit',    # Exit model for connections between rooms
]