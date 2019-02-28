import os

from adb.client import Client as AdbClient
import time
import subprocess

from src.animation.animation import animate_loading, colors
from src.animation.colors import colored
from file_puller import FilePuller


class PurpleScouter(object):
    """
    Handles the main user loop.
    """

    def __init__(self, adb_ip, adb_port, config):
        """
        Starts the connection with the adb server.
        """
        try:
            self.__adb = AdbClient(host=adb_ip, port=adb_port)
            self.__adb.devices()
        except Exception:
            with colored(colors.RED):
                print "adb server isn't running, opening."
                subprocess.Popen([config.get("adb", "adb_location"), "start-server"])

        self.__config = config

    def start(self):
        """
        Starts the infinite loop.
        """
        print "Welcome to:"
        with colored(colors.PURPLE):
            print "Purple Scouter!"
        time.sleep(1)

        while True:
            devices = self.__adb.devices()
            if devices:
                with colored(colors.BLUE):
                    print "\nFound {len} connected devices!".format(len=len(devices))

                for device in devices:
                    FilePuller(device, self.__config).move_all_scouting_files_from_phone()

            animate_loading()
