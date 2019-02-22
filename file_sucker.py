from adb.client import Client as AdbClient
import os

DEFAULT_SERVER_IP = "127.0.0.1"
DEFAULT_SERVER_PORT = 5037

SCOUTING_FOLDER_OUTPUT_PATH = ""  # TODO: Find and fill.
FIND_SCOUTING_FILES_COMMAND = "ls {path}".format(path=SCOUTING_FOLDER_OUTPUT_PATH)

OUTPUT_FOLDER = "Scouting"
FILE_ID = 0
FILE_NAME = "x{id}.txt".format(id=FILE_ID)

REMOVE_FILE_COMMAND = "rm {file_path}"


class FileSucker(object):
    """
    Sucks scouting files from connected phone.
    """
    def __init__(self):
        """
        Sets the adb client, TODO: Check if it opens the adb server automatically or not.
        """
        self.__client = AdbClient(host=DEFAULT_SERVER_IP, port=DEFAULT_SERVER_PORT)

        self.__phone = self.__client.devices()[0]

    def find_all_scouting_files(self):
        """
        Searches for all scouting files in the phone.
        :return: A list of all the found scouting files paths.
        :rtype: list
        """
        paths = [self.__phone.shell(FIND_SCOUTING_FILES_COMMAND)]
        #TODO: this wont work, I do not know how the scouting arranges the files, Needs to be fixed.
        return [SCOUTING_FOLDER_OUTPUT_PATH + path for path in paths]

    def cut_file(self, file_path):
        """
        Gets a file path and cuts it from the phone to the computer.
        :param file_path: The path of the file to cut.
        """
        global FILE_ID
        if not os.path.exists(OUTPUT_FOLDER) and os.path.isdir(OUTPUT_FOLDER):
            os.mkdir(OUTPUT_FOLDER)

        FILE_ID += 1
        self.__phone.pull(file_path, OUTPUT_FOLDER + FILE_NAME)
        self.__phone.shell(REMOVE_FILE_COMMAND.format(file_path=file_path))

    def cut_all_scouting_files_from_phone(self):
        """
        Finds and cuts all the scouting files in the connected phone to the computer.
        """
        scouting_files = self.find_all_scouting_files()
        print "Found {number} scouting files in the device.".format(number=len(scouting_files))

        for index, file_path in enumerate(scouting_files):
            print "Copying {current}/{total}".format(current=(index + 1), total=len(scouting_files))
            self.cut_file(file_path)


def main():
    FileSucker().cut_all_scouting_files_from_phone()


if __name__ == '__main__':
    main()