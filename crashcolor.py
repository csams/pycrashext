"""
 Written by Daniel Sungju Kwon
"""
from __future__ import division, print_function
from pykdump.API import exec_crash_command
import sys

BLACK = 1
RED = 2
GREEN = 3
YELLOW = 4
BLUE = 5
MAGENTA = 6
CYAN = 7
DARKGRAY = 8
LIGHTRED = 9
LIGHTGREEN = 10
LIGHTYELLOW = 11
LIGHTBLUE = 12
LIGHTMAGENTA = 13
LIGHTCYAN = 14
LIGHTGRAY = 15
WHITE = 16
RESET = 17

MAX_COLOR = WHITE

BOLD = 0x00100
BLINK = 0x00200
UNDERLINE = 0x00400
INVERT = 0x00800

MIN_MODE = BOLD
MAX_MODE = INVERT

COLOR_MASK = 0x00ff
MODE_MASK = 0xff00


color_list = {
    BLACK: "\\033[30m",
    RED: "\\033[31m",
    GREEN: "\\033[32m",
    YELLOW: "\\033[33m",
    BLUE: "\\033[34m",
    MAGENTA: "\\033[35m",
    CYAN: "\\033[36m",
    LIGHTGRAY: "\\033[37m",
    DARKGRAY: "\\033[38m",
    LIGHTRED: "\\033[91m",
    LIGHTGREEN: "\\033[92m",
    LIGHTYELLOW: "\\033[93m",
    LIGHTBLUE: "\\033[94m",
    LIGHTMAGENTA: "\\033[95m",
    LIGHTCYAN: "\\033[96m",
    WHITE: "\\033[97m",
    RESET: "\\033[0m",
    BOLD: "\\033[1m",
    BLINK: "\\033[5m",
    UNDERLINE: "\\033[4m",
    INVERT: "\\033[7m",
}


def set_color(color_mix):
    if not sys.stdout.isatty():
        return

    color = color_mix & COLOR_MASK
    mode = color_mix & MODE_MASK

    color_ansi_code = ""
    # Set text color
    if color in color_list:
        color_ansi_code = color_list[color]

    # Set text mode
    for cur_mode in range(MIN_MODE, MAX_MODE, MIN_MODE):
        cur_color = mode & cur_mode
        if cur_color in color_list:
            color_ansi_code = color_ansi_code + color_list[cur_color]

    if len(color_ansi_code) > 0:
        result_str = exec_crash_command("gdb echo " + color_ansi_code)
        print (result_str, end='')
