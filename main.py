from src.purple_scouter import PurpleScouter
import ConfigParser

CONFIG_PATH = "scouter.conf"


def main():
    """
    Starts the program.
    """
    config = ConfigParser.ConfigParser()
    config.read(CONFIG_PATH)
    PurpleScouter(adb_ip=config.get("adb", "adb_server_ip"),
                  adb_port=int(config.get("adb", "adb_server_port")),
                  config=config).start()

if __name__ == '__main__':
    main()