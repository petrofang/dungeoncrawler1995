from engine import ConsoleIO, Parser
import ini

connection = ConsoleIO(Parser())
connection.print(ini.splash_art)
connection.start_session()
