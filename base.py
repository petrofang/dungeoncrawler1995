import pymssql # explicitly imported
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy.orm import DeclarativeBase, sessionmaker, mapped_column
from typing_extensions import Annotated


# remember to create a shadow.py as needed with the following:
from shadow import SERVER, USER, PASSWORD, DATABASE

# connection will need to be tailored to your particular SQL and driver:
connection = f"mssql+pymssql://{USER}:{PASSWORD}@{SERVER}/{DATABASE}"
engine = create_engine(connection)
Session = sessionmaker(bind=engine)
SQL = Session()

class Base(DeclarativeBase):
    pass

# Annotations: extended types for mapped database columns:
pk_id = Annotated[int, mapped_column(primary_key=True, autoincrement=True)]
fk_from_room = Annotated[int, mapped_column(ForeignKey('rooms.id', name='fk_from_room'))]
fk_to_room = Annotated[int, mapped_column(ForeignKey('rooms.id', name='fk_to_room'))]

if __name__ == "__main__":
    from rooms import Room, Exit
    print(SQL.query(Room).all())
    print(SQL.query(Exit).all())