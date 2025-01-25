import pymssql
from sqlalchemy import create_engine, ForeignKey, JSON 
from sqlalchemy.orm import DeclarativeBase, sessionmaker, mapped_column, relationship, Mapped
from typing import List
from typing_extensions import Annotated
from passlib.hash import pbkdf2_sha256

from orm.shadow import SERVER, USER, PASSWORD, DATABASE

STARTING_ROOM = 0

# Database connection setup
connection = f"mssql+pymssql://{USER}:{PASSWORD}@{SERVER}/{DATABASE}"
engine = create_engine(connection)
Session = sessionmaker(bind=engine)
SQL = Session()

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
    pass
# Models

class GameObject(Base):
    __tablename__ = 'game_objects'
    __mapper_args__ = {'polymorphic_identity': 'game_object',
                       'polymorphic_on': 'object_type'}
    id: Mapped[pk_id]
    name: Mapped[str]
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

    @property
    def a(self) -> str:
        return 'an' if self.name[0].lower() in 'aeioh' else 'a'

    def __init__(self, name: str, description: str, *args, **kwargs):
        self.name = name
        self.description = description
        super().__init__(*args, **kwargs)

    def __repr__(self):
        return f'<{self.__class__.__name__}(id:{self.id})[{self.name}]>'

class Room(GameObject):
    __tablename__ = 'rooms'
    __mapper_args__ = {'polymorphic_identity': 'room'}

    id: Mapped[fk_id]
    exits: Mapped[List["Exit"]] = relationship(back_populates="from_room", foreign_keys='Exit.from_room_id')
    entries: Mapped[List["Exit"]] = relationship(back_populates="to_room", foreign_keys='Exit.to_room_id')
  
    def view(self, looker) -> str:
        items = [obj for obj in self.inventory if isinstance(obj, Item)]
        creatures = [mob for mob in self.inventory if isinstance(mob, Creature) and mob != looker]
        items_text = "Items: " + ", ".join(i.name for i in items) if items else ""
        creatures_text = "Creatures: " + ", ".join(c.name for c in creatures) if creatures else ""
        return f'[{self.name}]\n    {self.description} {items_text}. {creatures_text}. \nExits: {", ".join(e.direction for e in self.exits)}'

class Creature(GameObject):
    __tablename__ = 'creatures'
    __mapper_args__ = {'polymorphic_identity': 'creature'}

    id: Mapped[fk_id]
    Str: Mapped[null_1] # Strength
    Dex: Mapped[null_1] # Dexterity
    Int: Mapped[null_1] # Intelligence
    hp: Mapped[null_1] # Hit points
    hp_max: Mapped[null_1] # Maximum hit points

    @property
    def room(self) -> Room:
        if self.owner.object_type == 'room':
            return self.owner
        


class Player(Creature):
    __tablename__ = 'players'
    __mapper_args__ = {'polymorphic_identity': 'player'}
    
    id: Mapped[creature_id]
    username: Mapped[str] = mapped_column(unique=True)
    password_hash: Mapped[str]
    
    def set_password(self, password: str) -> None:
        self.password_hash = pbkdf2_sha256.hash(password)
        
    def check_password(self, password: str) -> bool:
        return pbkdf2_sha256.verify(password, self.password_hash)
        
class Item(GameObject):
    __tablename__ = 'items'
    __mapper_args__ = {'polymorphic_identity': 'item'}

    id: Mapped[fk_id]
    stats: Mapped[json] # JSON string with item stats


class Exit(Base):
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