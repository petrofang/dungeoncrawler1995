from dotenv import load_dotenv
import os
import pymssql
import queue
from sqlalchemy import create_engine 
from sqlalchemy.orm import Session, scoped_session

from orm import Player

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
SQL = Session(sql_engine)

# Action queue setup
action_queue = queue.Queue()

class Action():
    # class because each function will be an database action

    @staticmethod
    def chown(subject, target, arg, **kwargs):
        ''' Change the owner of an object. '''
        print(f"Changing owner of {target} to {arg}")
        target.owner = arg
        SQL.add(target)
        return True
    
    @staticmethod
    def echo(subject, target, arg, **kwargs):
        ''' Print to all in the player's room. '''
        room = subject.owner
        for everyone in room.inventory:
            if isinstance(everyone, Player):
                try:
                    everyone.io.print(arg)
                except Exception as e:
                    print(f"Error echoing to {everyone}: {e}")

    @staticmethod
    def echo_at(subject, target, arg, **kwargs):
        ''' Print to a specific player. '''
        try:
            target.io.print(arg)
        except Exception as e:
            print(f"Error echoing to {target}: {e}")

    @staticmethod
    def echo_around(subject, target, arg, **kwargs):
        ''' Print to all in the player's room except the player. '''
        room = subject.owner
        for everyone in room.inventory:
            if isinstance(everyone, Player) and everyone != subject:
                try:
                    everyone.io.print(arg)
                except Exception as e:
                    print(f"Error echoing to {everyone}: {e}")

def do(subject, action, target, arg, **kwargs):
    action_queue.put((subject, action, target, arg, kwargs))

def process_actions():
    while True:
        try:
            subject, action, target, arg, kwargs = action_queue.get()
            if action in Action.__dict__:
                Action.__dict__[action](subject, target, arg, **kwargs)
                SQL.commit()
            else:
                print(f"Unknown action: {action}")
            action_queue.task_done()
        except Exception as e:
            print(f"Error processing action:\n   {e}")