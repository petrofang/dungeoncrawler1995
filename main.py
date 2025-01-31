import threading

from engine import GameServer
import ini

def main():
    from orm import process_actions

    # Start the action processing thread
    action_thread = threading.Thread(target=process_actions, daemon=True)
    action_thread.start()

    # Start the player connection thread:
          
    print("Starting server...")
    server = GameServer('0.0.0.0', 4000)
    try:
        server.start()
    except KeyboardInterrupt:
        print("\nShutting down server...")
        server.stop()

if __name__ == "__main__":
    main()  
