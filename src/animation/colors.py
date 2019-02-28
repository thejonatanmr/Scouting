from contextlib import contextmanager
import sys

BROWN = "\33[0;33m"
GRAY = "\33[0;37m"
DARK_GRAY = "\33[1;30m"
LIGHT_BLUE = " \33[0;34m"
LIGHT_GREEN = "\33[0;32m"
LIGHT_CYAN = "\33[0;36m"
LIGHT_RED = "\33[0;31m"
LIGHT_PURPLE = "\33[0;35m"
YELLOW = "\33[1;33m"
PURPLE = "\33[1;35m"
RED = "\033[1;31m"
BLUE = "\033[1;34m"
CYAN = "\033[1;36m"
GREEN = "\033[0;32m"

all_colors = [BROWN, GRAY, DARK_GRAY, LIGHT_BLUE, LIGHT_GREEN, LIGHT_CYAN, LIGHT_RED, LIGHT_PURPLE, YELLOW, PURPLE, RED,
              BLUE, CYAN, GREEN]

RESET = "\033[0;0m"
BOLD = "\033[;1m"
REVERSE = "\033[;7m"


@contextmanager
def colored(color):
    sys.stdout.write(color)
    yield
    sys.stdout.write(RESET)
