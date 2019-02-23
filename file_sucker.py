from adb.client import Client as AdbClient
import os
import re
import base64

DEFAULT_SERVER_IP = "127.0.0.1"
DEFAULT_SERVER_PORT = 5037

SCOUTING_FOLDER_OUTPUT_PATH = "/sdcard/documents"
LIST_DOCUMENTS_FOLDER = "ls {path}".format(path=SCOUTING_FOLDER_OUTPUT_PATH)
SCOUTING_FOLDERS_FORMAT = "Robot Scouter export_[0-9]*"
SCOUTING_FILES_FORMAT = ".*.xlsx"  # TODO: need to change according to the name of the real files.
LIST_SCOUTING_FILES = "ls {father_path}/{child_path}"
SCOUTING_FILES_FULL_PATH_FORMAT = "{base_folder}/{export_folder}/{filename}"

OUTPUT_FOLDER = "Scouting"
FILE_ID = 0
FILE_NAME = "x{id}.xlsx"
PULL_BASE64_FORMAT = "cat {file_path} | base64"

REMOVE_FILE_COMMAND = "rm -r {file_path}"


class FilePuller(object):
    """
    Pulls scouting files from connected phone.
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
        output_list = []
        list_documents = self.__phone.shell(LIST_DOCUMENTS_FOLDER)
        scouting_folders = [folder_path.replace(" ", r"\ ") for folder_path in
                            re.findall(SCOUTING_FOLDERS_FORMAT, list_documents)]

        for folder_path in scouting_folders:
            list_scouting_files = self.__phone.shell(LIST_SCOUTING_FILES.format(
                                                        father_path=SCOUTING_FOLDER_OUTPUT_PATH,
                                                        child_path=folder_path))

            scouting_files = [file.replace(" ", r"\ ") for file in re.findall(SCOUTING_FILES_FORMAT, list_scouting_files)]

            for file in scouting_files:
                output_list.append(SCOUTING_FILES_FULL_PATH_FORMAT.format(
                    base_folder=SCOUTING_FOLDER_OUTPUT_PATH,
                    export_folder=folder_path,
                    filename=file
                ))

        return output_list

    def copy_file(self, file_path):
        """
        Gets a file path and copies it from the phone to the computer.
        :param file_path: The path of the file to copy.
        """
        global FILE_ID
        if not os.path.exists(OUTPUT_FOLDER):
            os.mkdir(OUTPUT_FOLDER)

        FILE_ID += 1
        base_64_file = self.__phone.shell(PULL_BASE64_FORMAT.format(file_path=file_path))

        with open(OUTPUT_FOLDER + "/" + FILE_NAME.format(id=FILE_ID), "wb") as output_file:
            output_file.write(base64.b64decode(base_64_file))

    def cut_all_scouting_files_from_phone(self):
        """
        Finds and cuts all the scouting files in the connected phone to the computer.
        """
        scouting_files = self.find_all_scouting_files()
        print "Found {number} scouting files in the device.".format(number=len(scouting_files))

        for index, file_path in enumerate(scouting_files):
            print "Copying {current}/{total}".format(current=(index + 1), total=len(scouting_files))
            self.copy_file(file_path)


def main():
    FilePuller().cut_all_scouting_files_from_phone()


if __name__ == '__main__':
    main()
