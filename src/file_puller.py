import ConfigParser
import os
import re
import base64
import sys
import time

from src.animation import colors

SCOUTING_FOLDER_OUTPUT_PATH = "/sdcard/documents"
LIST_DOCUMENTS_FOLDER = "ls {path}".format(path=SCOUTING_FOLDER_OUTPUT_PATH)
LIST_SCOUTING_FILES = "ls {father_path}/{child_path}"
SCOUTING_FILES_FULL_PATH_FORMAT = "{base_folder}/{export_folder}/{filename}"

OUTPUT_FOLDER = "./Scouting"
FILE_ID = 0

PULL_BASE64_FORMAT = "cat {file_path} | base64"

REMOVE_FILE_COMMAND = "rm -r {base_folder}/{folder}"

NUMBER_ANIMATION = r"{curr}\{total}"
ANIMATION_ITERATION = 0.2


class FilePuller(object):
    """
    Pulls scouting files from connected phone.
    """
    __config = None  # type: ConfigParser

    def __init__(self, device, config):
        """
        Saves the connected device.
        """
        self.__phone = device
        self.__config = config

    def find_all_scouting_files(self):
        """
        Searches for all scouting files in the phone.
        :return: A list of all the found scouting files paths.
        :rtype: list
        """
        output_list = []
        list_documents = self.__phone.shell(LIST_DOCUMENTS_FOLDER)
        scouting_folders = [folder_path.replace(" ", r"\ ") for folder_path in
                            re.findall(self.__config.get("file_puller", "scouting_folder_regex"), list_documents)]

        for folder_path in scouting_folders:
            list_scouting_files = self.__phone.shell(LIST_SCOUTING_FILES.format(
                father_path=SCOUTING_FOLDER_OUTPUT_PATH,
                child_path=folder_path))

            scouting_files = [file.replace(" ", r"\ ") for file in
                              re.findall(self.__config.get("file_puller", "scouting_files_regex"), list_scouting_files)]

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

        with open(OUTPUT_FOLDER + "/" + self.__config.get("file_puller", "output_file_format").format(id=FILE_ID),
                  "wb") as output_file:
            output_file.write(base64.b64decode(base_64_file))

    def delete_all_scouting_folders(self):
        """
        Deletes all scouting folders.
        """
        list_documents = self.__phone.shell(LIST_DOCUMENTS_FOLDER)
        scouting_folders = [folder_path.replace(" ", r"\ ") for folder_path in
                            re.findall(self.__config.get("file_puller", "scouting_folder_regex"), list_documents)]

        for index, folder in enumerate(scouting_folders):
            time.sleep(ANIMATION_ITERATION)
            sys.stdout.write("\rDeleting " + NUMBER_ANIMATION.format(curr=(index + 1), total=len(scouting_folders)))
            sys.stdout.flush()
            self.__phone.shell(REMOVE_FILE_COMMAND.format(base_folder=SCOUTING_FOLDER_OUTPUT_PATH, folder=folder))

    def move_all_scouting_files_from_phone(self):
        """
        Finds and cuts all the scouting files in the connected phone to the computer.
        """
        scouting_files = self.find_all_scouting_files()
        with colors.colored(colors.GREEN if len(scouting_files) > 0 else colors.YELLOW):
            print "Found {number} scouting files in the device.".format(number=len(scouting_files))

        for index, file_path in enumerate(scouting_files):
            time.sleep(ANIMATION_ITERATION)
            sys.stdout.write("\rCopying " + NUMBER_ANIMATION.format(curr=(index + 1), total=len(scouting_files)))
            sys.stdout.flush()
            self.copy_file(file_path)
            print""

        self.delete_all_scouting_folders()
        print ""
