# DungeonCrawler1995

A text-based dungeon game engine built with modern Python and SQLAlchemy. The engine uses a classic MUD-style architecture but with contemporary programming practices and tooling.

## Features

- Command-line text adventure interface
- SQLAlchemy ORM with MS SQL Server persistence
- Rich game object system:
  - Rooms with exits and descriptions
  - Items with customizable stats
  - Creatures with basic RPG attributes (STR/DEX/INT)
  - Players with password protection
- Navigation system with cardinal directions
- Inventory management
- Command system with built-in help
- Decorator-based command argument parsing

## Setup

### Requirements
- Python 3.10+
- MS SQL Server instance
- Python packages (see requirements.txt)

### Project Structure
```
dungeoncrawler1995/
├── orm/            # Database interaction
│   ├── models.py   # Game object definitions
│   └── .env        # Database credentials (not in repo)
├── engine/         # Core game logic
├── commands.py     # Command parsing/handling
├── ini.py         # Configuration and metadata
└── main.py        # Game entry point
```

### Database Configuration
1. Create a new database in MS SQL Server
2. Copy `orm/.env.example` to `orm/.env`
3. Update database credentials in `orm/.env`:
   - DB_SERVER
   - DB_USER
   - DB_PASSWORD
   - DB_DATABASE

## Development Status

Currently in early development. The core engine and object system are functional, but many game features are still being implemented.

### Planned Features
- Combat system
- NPC interactions
- Item manipulation
- Equipment system
- Multi-user capabilities

## License

This project is licensed under the MIT License - see [LICENSE.md](LICENSE.md) for details.

## Author

Giles Cooper
- GitHub: [@petrofang](https://github.com/petrofang)
