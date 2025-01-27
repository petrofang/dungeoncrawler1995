from contextlib import contextmanager
from dotenv import load_dotenv
import os
from passlib.hash import pbkdf2_sha256
import pymssql
from sqlalchemy import create_engine, ForeignKey, JSON 
from sqlalchemy.orm import DeclarativeBase, sessionmaker, mapped_column, relationship, Mapped, scoped_session
from typing import List
from typing_extensions import Annotated

from engine.exceptions import *

# Load and validate database configuration
load_dotenv()
SERVER = os.getenv('DB_SERVER')
USER = os.getenv('DB_USER')
PASSWORD = os.getenv('DB_PASSWORD')
DATABASE = os.getenv('DB_DATABASE')

if not all([SERVER, USER, PASSWORD, DATABASE]):
    raise ValueError("Missing required database environment variables. Check your .env file.")

STARTING_ROOM = 0

# Database connection setup
connection = f"mssql+pymssql://{USER}:{PASSWORD}@{SERVER}/{DATABASE}"
sql_engine = create_engine(connection)
SQL = scoped_session(sessionmaker(bind=sql_engine))

# Type annotations
pk_id = Annotated[int, mapped_column(primary_key=True, autoincrement=True)]
fk_id = Annotated[int, mapped_column(ForeignKey('game_objects.id'), primary_key=True, autoincrement=True)]
fk_from_room = Annotated[int, mapped_column(ForeignKey('rooms.id', name='fk_from_room'))]
fk_to_room = Annotated[int, mapped_column(ForeignKey('rooms.id', name='fk_to_room'))]
fk_room = Annotated[int, mapped_column(ForeignKey('rooms.id', name='fk_room'))]
json = Annotated[str, mapped_column(JSON)]
null_1 = Annotated[int, mapped_column(nullable=False, default=1)]
creature_id = Annotated[int, mapped_column(ForeignKey('creatures.id'), primary_key=True, autoincrement=True)]

# Base class
class Base(DeclarativeBase):
    """Base class for all SQLAlchemy models in the application."""
    pass

# Models
class GameObject(Base):
    """
    Initialize with:
        name (str): Name of object (default: 'unnamed')
        description (str): Object description (default: None)
        owner_id (int): ID of containing object (default: 0)
        article (bool): Use 'a/an' prefix (default: True)
        **kwargs: Additional attributes to set on the object
    """
    __tablename__ = 'game_objects'
    __mapper_args__ = {'polymorphic_identity': 'game_object',
                       'polymorphic_on': 'object_type'}
    id: Mapped[pk_id]
    name: Mapped[str]
    noun: Mapped[str] # Noun form of the name
    adjectives: Mapped[json] # Adjectives describing the object
    description: Mapped[str]
    article: Mapped[bool] # True if the name should be preceded with an article such as 'a' or 'an'
    owner_id: Mapped[int | None] = mapped_column(ForeignKey('game_objects.id'), nullable=True)
    object_type: Mapped[str]
    owner: Mapped["GameObject"] = relationship('GameObject', 
                                            foreign_keys='GameObject.owner_id',
                                            remote_side='GameObject.id',
                                            back_populates='inventory')
    inventory: Mapped[List["GameObject"]] = relationship('GameObject',
                                                         back_populates='owner', 
                                                         foreign_keys='GameObject.owner_id')    

    def __init__(self, 
                 name: str = 'unnamed',
                 noun: str = 'thing',
                 adjectives: List[str] = None,
                 description: str|None = None,  
                 owner_id: int = 0,
                 article: bool = True,
                 *args, **kwargs):
        self.name = name
        
        self.description = description
        self.owner_id = owner_id
        self.article = article
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __repr__(self):
        return f'<{self.__class__.__name__}(id:{self.id})[{self.name}]>'
    
    def __str__(self):
        return f"{self.a}{self.name}"

    @property
    def a(self) -> str:
        return 'an ' if self.name[0].lower() in 'aeioh' else 'a '

    @property
    def room(self):
        try:
            if self.owner.object_type == 'room':
                return self.owner
            else: 
                raise RoomError(f'{self.name} is not in a room.') 
        except RoomError as e:
            print(e)
            return None
        
    @room.setter
    def room(self, room) -> None:
        try:
            if room.object_type != 'room':
                raise RoomError(f'{room} is not room.')
        except RoomError as e:
            print(f"Error:{self} trying to set room to not-a-room: {room}")
            return False
        self.owner = room
        return True


class Room(GameObject):
    """
    Initialize with:
        **kwargs: Arguments passed to GameObject parent class
    """
    __tablename__ = 'rooms'
    __mapper_args__ = {'polymorphic_identity': 'room'}

    id: Mapped[fk_id]
    exits: Mapped[List["Exit"]] = relationship(back_populates="from_room", foreign_keys='Exit.from_room_id')
    entries: Mapped[List["Exit"]] = relationship(back_populates="to_room", foreign_keys='Exit.to_room_id')
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def view(self, looker) -> str:
        items = [obj for obj in self.inventory if isinstance(obj, Item)]
        creatures = [mob for mob in self.inventory if isinstance(mob, Creature) and mob != looker]
        items_text = "Items: " + ", ".join(i.name for i in items) if items else ""
        creatures_text = "Creatures: " + ", ".join(c.name for c in creatures) if creatures else ""
        return f'[{self.name}]\n    {self.description} {items_text}. {creatures_text}. \nExits: {", ".join(e.direction for e in self.exits)}'


class Creature(GameObject):
    """
    Initialize with:
        Str (int): Strength stat (default: 1)
        Dex (int): Dexterity stat (default: 1)
        Int (int): Intelligence stat (default: 1)
        hp_max (int): Maximum hit points (default: 1)
                      (hit points will be set to this value)
        **kwargs: GameObject parameters (name, description, etc)
    """
    __tablename__ = 'creatures'
    __mapper_args__ = {'polymorphic_identity': 'creature'} 

    id: Mapped[fk_id]
    Str: Mapped[null_1] # Strength
    Dex: Mapped[null_1] # Dexterity
    Int: Mapped[null_1] # Intelligence
    hp: Mapped[null_1] # Hit points
    hp_max: Mapped[null_1] # Maximum hit points

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.hp = self.hp_max


class Player(Creature):
    """
    Initialize with:
        username (str): Player's login name
        password (str): Player's password (will be hashed)
        **kwargs: Creature and GameObject parameters
    """
    __tablename__ = 'players'
    __mapper_args__ = {'polymorphic_identity': 'player'}
    
    id: Mapped[creature_id]
    username: Mapped[str] = mapped_column(unique=True)
    password_hash: Mapped[str]
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.article = False

    def set_password(self, password: str) -> None:
        self.password_hash = pbkdf2_sha256.hash(password)
        
    def check_password(self, password: str) -> bool:
        return pbkdf2_sha256.verify(password, self.password_hash)


class Item(GameObject):
    """
    Initialize with:
        **kwargs: Arguments passed to GameObject parent class
    """
    __tablename__ = 'items'
    __mapper_args__ = {'polymorphic_identity': 'item'}

    id: Mapped[fk_id]
    stats: Mapped[json] # JSON string with item stats

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class Exit(Base):
    """
    Initialize with:
        direction (str): Cardinal direction of the exit
        from_room (Room): Room where this exit starts
        to_room (Room): Room where this exit leads
    """
    __tablename__ = 'exits'
    id: Mapped[pk_id]
    direction: Mapped[str] 
    from_room_id: Mapped[fk_from_room]
    to_room_id: Mapped[fk_to_room]
    from_room: Mapped[Room] = relationship(back_populates='exits',
                                           foreign_keys='Exit.from_room_id')
    to_room: Mapped[Room] = relationship(back_populates='entries', 
                                         foreign_keys='Exit.to_room_id')
    
    def __init__(self, direction: str, from_room: Room, to_room: Room):
        self.from_room = from_room
        self.to_room = to_room
        self.direction = direction

    def __repr__(self):
        return (f'<{self.__class__.__name__}',
                f'(id:{self.id})[{self.from_room_id}]->',
                f'{self.direction}->[{self.to_room_id}]>')


if __name__=="__main__":
    print("this module is not meant to be run directly")