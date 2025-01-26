
from engine import ConsoleIO, Parser
from ini import splash, __author__, __version__


def splash():
    return(splash_art)



if __name__ == "__main__":
    connection = ConsoleIO(Parser())
    connection.print(splash())
    connection.start_session()
