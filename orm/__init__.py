"""
DungeonCrawler1995 ORM Package
-----------------------------
Database models and SQLAlchemy setup for the dungeon crawler game.
"""

from .models import SQL, Base, GameObject, Room, Exit, Item, Creature, Player

# Explicitly declare public API
__all__ = [
    'SQL',          # Session instance for database access
    'Base',         # SQLAlchemy declarative base
    'GameObject',   # Base game object class
    'Room',         # Room model for dungeon locations
    'Exit',         # Exit model for connections between rooms
    'Creature',     # Creature model for monsters and NPCs
    'Item',         # Item model for objects that can be collected
    'Player',       # Player model for the user-controlled character
]