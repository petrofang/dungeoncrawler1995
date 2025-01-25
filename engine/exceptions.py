"""Game engine exceptions."""

class GameException(Exception):
    """Base class for game exceptions"""
    pass

class Quit(GameException):
    """Raised when a player quits the game"""
    pass
