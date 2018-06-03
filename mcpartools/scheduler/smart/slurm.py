#! /bin/python
from classes import *
from shlex import split
from subprocess import STDOUT
from subprocess import check_output


def gather_cluster_state():
    command = "sinfo --states='idle,mixed' --partition=plgrid --format='%n %P %O %C %T'"
    output = check_output(split(command), shell=True, stderr=STDOUT)
    splitted_output = output.split("\n")[1:]
    nodes = [NodeInfo(line) for line in splitted_output]
    cluster_info = ClusterInfo(nodes)
    print ClusterInfo
    return cluster_info
