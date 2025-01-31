import socket
import threading
import time
from typing import Optional, Dict, Set
from .parser import Parser
from .io import TelnetIO

class GameServer:
    """Game server that listens for and handles client connections."""
    
    # Telnet protocol commands
    IAC = bytes([255])  # "Interpret As Command"
    WILL = bytes([251])
    WONT = bytes([252])
    DO = bytes([253])
    DONT = bytes([254])
    ECHO = bytes([1])   # Echo option
    SGA = bytes([3])    # Suppress Go Ahead
    
    def __init__(self, host: str = '0.0.0.0', port: int = 4000, timeout: int = 300):
        self.host = host
        self.port = port
        self.timeout = timeout  # connection timeout in seconds
        self.server_socket: Optional[socket.socket] = None
        self.parser = Parser()
        self.running = False
        self.clients: Dict[socket.socket, threading.Thread] = {}
        self.active_players: Set[str] = set()
        self._lock = threading.Lock()
        
    def start(self) -> None:
        """Start the game server."""
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        self.running = True
        
        print(f"Game server listening on {self.host}:{self.port}")
        
        try:
            while self.running:
                try:
                    client_socket, address = self.server_socket.accept()
                    print(f"New connection from {address}")
                    self._handle_client(client_socket)
                except Exception as e:
                    print(f"Error accepting connection: {e}")
        finally:
            self._cleanup()
                
    def stop(self) -> None:
        """Stop the game server and disconnect all clients."""
        self.running = False
        if self.server_socket:
            self.server_socket.close()
        self._cleanup()
            
    def _cleanup(self) -> None:
        """Clean up all client connections."""
        with self._lock:
            for client_socket in list(self.clients.keys()):
                try:
                    client_socket.shutdown(socket.SHUT_RDWR)
                    client_socket.close()
                except:
                    pass
            self.clients.clear()
            self.active_players.clear()
            
    def _handle_client(self, client_socket: socket.socket) -> None:
        """Create new thread for client connection."""
        client_socket.settimeout(self.timeout)
        self._setup_telnet(client_socket)
        
        client_thread = threading.Thread(
            target=self._client_session,
            args=(client_socket,),
            daemon=True
        )
        
        with self._lock:
            self.clients[client_socket] = client_thread
            
        client_thread.start()
        
    def _client_session(self, client_socket: socket.socket) -> None:
        """Handle individual client connection."""
        try:
            io_handler = TelnetIO(self.parser, client_socket)
            io_handler.start_session()  # TelnetIO will handle authentication
        except socket.timeout:
            print("Client connection timed out")
        except Exception as e:
            print(f"Client session error: {e}")
        finally:
            with self._lock:
                self.clients.pop(client_socket, None)
            try:
                client_socket.close()
            except:
                pass
                
    def _setup_telnet(self, client_socket: socket.socket) -> None:
        """Send initial telnet protocol negotiations."""
        try:
            # Tell client we'll echo
            client_socket.send(self.IAC + self.WILL + self.ECHO)
            # Tell client we want it to echo
            client_socket.send(self.IAC + self.DO + self.ECHO)
            print("Sent telnet negotiations")
            # Don't wait for response - some clients don't send one
        except Exception as e:
            print(f"Telnet negotiation error: {e}")

if __name__=="__main__":
    print("This module is not meant to be run directly.")