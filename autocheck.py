"""
Written by Daniel Sungju Kwon

This is running extra rules to detect known issues.
"""
from __future__ import print_function

import argparse
import os
import sys

import crashcolor
from insights import datasource, dr
from insights.core.plugins import is_type, rule
from insights.formats.text import HumanReadableFormat
from pykdump.API import exec_crash_command


class prerequisite(dr.ComponentType):
    """
    Custom decorator for some rule dependencies. If a rule requires a
    prerequisite that does not return a value, the rule will be skipped. This
    provides the same semantics as ``add_rule``.
    """
    def invoke(self, broker):
        result = super(prerequisite, self).invoke(broker)
        if not result:
            raise dr.SkipComponent()
        return result


@datasource()
def get_system_info():
    sysinfo = {}
    resultlines = exec_crash_command("sys").splitlines()
    for line in resultlines:
        words = line.split(":")
        sysinfo[words[0].strip()] = words[1].strip()
    return sysinfo


def get_active_rules():
    """
    Run the prerequisites and their dependencies to get the rules that could
    have run. Add to them the rules that have no prerequisites. If a rule has
    no prerequisites, it might always run.
    """
    prereqs = dr.COMPONENTS_BY_TYPE.get(prerequisite)
    rules = [r for r in dr.COMPONENTS_BY_TYPE[rule]
             if not any(is_type(d, prerequisite) for d in dr.get_dependencies(r))]
    graph = {}
    for p in prereqs:
        graph.update(dr.get_dependency_graph(p))

    broker = dr.run(graph)
    for p in list(broker.get_by_type(prerequisite)):
        rules.extend(dr.get_dependents(p))
    return rules


def print_rule(component):
    crashcolor.set_color(crashcolor.BLUE)
    print("[%s]" % dr.get_name(component), end='')
    crashcolor.set_color(crashcolor.RESET)

    doc = (getattr(component, "__doc__", "") or "No description available.")
    print(": %s" % doc)


def print_rules(rules):
    if not rules:
        print("No rules available for this vmcore.")
        return

    width = 75
    dashes = "-" * width
    print(dashes)
    for module in sorted(rules, key=dr.get_name):
        print_rule(module)

    print(dashes)
    print("There are %d rules available for this vmcore." % len(rules))
    print("=" * width)


def run_rules():
    """ Runs all of the loaded rules. """
    broker = dr.Broker()
    with HumanReadableFormat(broker):
        dr.run(broker=broker)


def extend_environment(cmd_path_list):
    """ Helper for adding paths to the python system path. """
    if cmd_path_list:
        sys.path.extend(cmd_path_list.split(':'))


def autocheck():
    p = argparse.ArgumentParser()  # optparse is deprecated in python 2.7.
    p.add_argument("-l", "--list", action="store_true", default=False,
            help="Shows the currently available rules")
    args = p.parse_args()

    extend_environment(os.environ.get("PYKDUMPPATH", ""))
    dr.load_components("rules")

    if args.list:
        rules = get_active_rules()
        print_rules(rules)
    else:
        run_rules()


if __name__ == '__main__':
    autocheck()
