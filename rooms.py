from sqlalchemy.orm import relationship, Mapped
from typing import List

from base import Base 
from base import (pk_id, 
                  fk_from_room, 
                  fk_to_room,
                  )

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

    def  __repr__(self):
        return f'<{self.__class__.__name__}(id:{self.id})[{self.from_room_id}]->{self.direction}->[{self.to_room_id}]>'
