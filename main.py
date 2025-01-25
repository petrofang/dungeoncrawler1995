from orm import Room, Item, Creature, Exit, SQL


if __name__ == "__main__":
    with SQL.begin():
        room = Room('The Void', 'A dark, empty space, devoid of light or sound. There is no gravity or sense of spacial orientation. It is nothing.')
        exit = Exit(from_room=room, to_room=room, direction='out')
        item = Item('nothing', 'There is nothing here.')
        item.owner = room
        creature = Creature('deep darkness', 'A certain wisp of darkness, immaterial and formless.')
        creature.owner = room
        print(room.look())