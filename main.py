from orm import Room, Item, Creature, Exit, SQL


if __name__ == "__main__":
    room = SQL.query(Room).first()
    print(room.look())