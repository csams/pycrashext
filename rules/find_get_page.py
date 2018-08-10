"""
 Written by Daniel Sungju Kwon
"""

from __future__ import print_function
from __future__ import division

from pykdump.API import *

from LinuxDump import Tasks

import sys
import ntpath
import operator

import crashcolor

def add_rule(sysinfo):
    if sysinfo is None or "RELEASE" not in sysinfo:
        return True

    if sysinfo["RELEASE"].startswith("2.6.32-696.20.1.el6"):
        return True

    return False

def run_rule(sysinfo):
    result = exec_crash_command("log")
    idx = result.find("find_get_page+0x")
    if idx == -1:
        return True

    print("=" * 75)
    crashcolor.set_color(crashcolor.LIGHTRED)
    print("!!! Known BUG on this system detected by %s !!!" % ntpath.basename(__file__))
    crashcolor.set_color(crashcolor.RESET)
    print("-" * 75)
    startidx = max(idx - 380, 0)
    endidx = min(idx + 800, len(result))
    print(result[startidx:endidx])
    print("-" * 75)
    print("KCS:")
    print("     softlockup in find_get_pages after installing kernel-2.6.32-696.23.1")
    crashcolor.set_color(crashcolor.BLUE)
    print("     https://access.redhat.com/solutions/3390081")
    crashcolor.set_color(crashcolor.RESET)
    print("Resolution:")
    crashcolor.set_color(crashcolor.RED)
    print("     Upgrade kernel to kernel-2.6.32-754.el6 or later version")
    crashcolor.set_color(crashcolor.RESET)
    print("-" * 75)

def find_get_page():
    run_rule(None)

if ( __name__ == '__main__'):
    find_get_page(None)
