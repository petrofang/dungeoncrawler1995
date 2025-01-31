import threading

from engine import ConsoleIO, Parser
import ini

def main():
    from orm import process_actions

    # Start the action processing thread
    action_thread = threading.Thread(target=process_actions, daemon=True)
    action_thread.start()

    # Start the player connection thread:
    connection = ConsoleIO(Parser())
    connection.print(ini.splash_art)
    connection.start_session()

if __name__ == "__main__":
    main()  
