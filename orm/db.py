from dotenv import load_dotenv
import os
import pymssql
import queue
from sqlalchemy import create_engine 
from sqlalchemy.orm import Session, scoped_session

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
        SQL.expire_all()
        target.owner = arg
        SQL.add(target)
        SQL.commit()
        return True

def do(subject, action, target, arg, **kwargs):
    action_queue.put((subject, action, target, arg, kwargs))

def process_actions():
    while True:
        subject, action, target, arg, kwargs = action_queue.get()
        if action in Action.__dict__:
            Action.__dict__[action](subject, target, arg, **kwargs)
            SQL.commit()
        else:
            print(f"Unknown action: {action}")
        action_queue.task_done()