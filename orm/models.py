import pymssql
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy.orm import DeclarativeBase, sessionmaker, mapped_column, relationship, Mapped
from typing import List
from typing_extensions import Annotated

from shadow import SERVER, USER, PASSWORD, DATABASE

# Database connection setup
connection = f"mssql+pymssql://{USER}:{PASSWORD}@{SERVER}/{DATABASE}"
engine = create_engine(connection)
Session = sessionmaker(bind=engine)
SQL = Session()

# Base class
class Base(DeclarativeBase):
    pass

# Type annotations
pk_id = Annotated[int, mapped_column(primary_key=True, autoincrement=True)]
fk_from_room = Annotated[int, mapped_column(ForeignKey('rooms.id', name='fk_from_room'))]
fk_to_room = Annotated[int, mapped_column(ForeignKey('rooms.id', name='fk_to_room'))]

# Models
class Room(Base):
    __tablename__ = 'rooms'
    id: Mapped[pk_id]
    title: Mapped[str]
    description: Mapped[str]

    exits: Mapped[List["Exit"]] = relationship(back_populates="from_room", foreign_keys='Exit.from_room_id')
    entries: Mapped[List["Exit"]] = relationship(back_populates="to_room", foreign_keys='Exit.to_room_id')

    def __repr__(self):
        return f'<{self.__class__.__name__}(id:{self.id})[{self.title}]>'

class Exit(Base):
    __tablename__ = 'exits'
    id: Mapped[pk_id]
    direction: Mapped[str] 
    from_room_id: Mapped[fk_from_room]
    to_room_id: Mapped[fk_to_room]

    from_room: Mapped[Room] = relationship(back_populates='exits', foreign_keys='Exit.from_room_id')
    to_room: Mapped[Room] = relationship(back_populates='entries', foreign_keys='Exit.to_room_id')

    def __repr__(self):
        return f'<{self.__class__.__name__}(id:{self.id})[{self.from_room_id}]->{self.direction}->[{self.to_room_id}]>'

if __name__ == "__main__":
    print(SQL.query(Room).all())
    print(SQL.query(Exit).all())
