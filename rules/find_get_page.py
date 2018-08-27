from __future__ import division, print_function
from autocheck import get_system_info, prerequisite
from pykdump.API import exec_crash_command
from insights.core.plugins import rule, make_pass, make_fail
from . import STANDARD_FAIL, STANDARD_PASS

PASS = "FIND_GET_PAGE_PASS"
FAIL = "FIND_GET_PAGE_FAIL"
CONTENT = {PASS: STANDARD_PASS, FAIL: STANDARD_FAIL}


@prerequisite(get_system_info)
def add_rule(sysinfo):
    if not sysinfo or sysinfo.get("RELEASE", "").startswith("2.6.32-696.20.1.el6"):
        return sysinfo


@rule(add_rule)
def run_rule(sysinfo):
    """ Checking find_get_page() bug in the system """

    result = exec_crash_command("log")
    idx = result.find("find_get_page+0x")
    if idx == -1:
        return make_pass(PASS)

    startidx = max(idx - 380, 0)
    endidx = min(idx + 800, len(result))
    return make_fail(FAIL,
            title="find_get_page() softlockup BZ detected.",
            msg=result[startidx:endidx],
            kcs_title="softlockup in find_get_pages after installing kernel-2.6.32-696.23.1",
            kcs_url="https://access.redhat.com/solutions/3390081",
            resolution="Upgrade kernel to kernel-2.6.32-754.el6 or later version")


if __name__ == '__main__':
    print(run_rule(None))
