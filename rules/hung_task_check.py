from __future__ import division, print_function

import math
import operator

from autocheck import prerequisite
from insights.core.plugins import datasource, rule, make_pass, make_fail
from pykdump.API import exec_crash_command, readSymbol
from . import STANDARD_FAIL, STANDARD_PASS

PASS = "FIND_GET_PAGE_PASS"
FAIL = "FIND_GET_PAGE_FAIL"
CONTENT = {PASS: STANDARD_PASS, FAIL: STANDARD_FAIL}


@datasource()
def ps_m():
    return exec_crash_command("ps -m")


@prerequisite(ps_m)
def find_uninterruptible_tasks(ps_list_str):
    ps_list = ps_list_str.splitlines()
    un_list = []
    for pid in ps_list:
        words = pid.split()
        if len(words) > 3 and words[2] == "[UN]":
            un_list.append(pid)
    return sorted(un_list, key=operator.itemgetter(1), reverse=True)


@prerequisite(find_uninterruptible_tasks)
def check_system_hang(task_list):
    if not task_list:
        return False

    task = task_list[len(task_list) - 1]
    words = task.split()
    days = words[0][1:]
    time_str = words[1][:-1]
    words = time_str.split(':')
    time = int(days) * 24 * 60 * 60 + int(words[0]) * 60 * 60 + \
            int(words[1]) * 60 + math.ceil(float(words[2]))

    return time >= readSymbol("sysctl_hung_task_timeout_secs")


@rule(find_uninterruptible_tasks, check_system_hang)
def run_rule(result, system_hung):
    """ Checking hung tasks """
    min_idx = max(len(result) - 5, 0)
    return make_fail(FAIL,
            title="Hung tasks detected",
            msg="%s UN tasks\n" % (len(result)) +
                "%s" % ("...\n" if min_idx > 0 else "") +
                "\n".join(result[min_idx:]),
            kcs_title="System becomes unresponsive with message \"INFO: task <process>:<pid> blocked for more than 120 seconds\".",
            kcs_url="https://access.redhat.com/solutions/31453",
            resolution="Please check long blocked tasks.\n" +
                "\tCurrent hung_task_timeout_secs is %d seconds" %
                (readSymbol("sysctl_hung_task_timeout_secs")))


if __name__ == '__main__':
    import pprint
    pp = pprint.PrettyPrinter(indent=0, width=180)
    pp.pprint(run_rule(None))
