"""
DungeonCrawler1995 ORM Package
-----------------------------
Database models and SQLAlchemy setup for the dungeon crawler game.
"""

from .models import GameObject, Room, Exit, Item, Creature, Player
from .db import do, SQL, process_actions
# Explicitly declare public API
__all__ = [
    'SQL',              # SQLAlchemy scoped session object
    'Base',             # SQLAlchemy declarative base
    'GameObject',       # Base game object class
    'Room',             # Room model for dungeon locations
    'Exit',             # Exit model for connections between rooms
    'Creature',         # Creature model for monsters and NPCs
    'Item',             # Item model for objects that can be collected
    'Player',           # Player model for the user-controlled character
    'do',               # action queue interface
    'process_actions',  # process action queue

]