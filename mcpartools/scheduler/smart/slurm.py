import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class NodeInfo:
    def __init__(self, line):
        logger.debug(line)
        parameters = line.split(" ")
        logger.debug(parameters)
        self.node_id = parameters[0]
        self.partition = parameters[1]
        self.load = parameters[2]
        self.state = parameters[3]

        cpu = parameters[4].split('/')
        self.cpu_available = int(cpu[0])
        self.cpu_idle = int(cpu[1])
        self.cpu_other = int(cpu[2])
        self.cpu_total = int(cpu[3])

    def is_idle(self):
        return self.state == "idle"

    def is_mixed(self):
        return self.state == "mixed"


class ClusterState:
    efficiency_ratio = 0.5
    step = 1.08

    def __init__(self, nodes_info):
        """
        :type nodes_info: list of NodeInfo
        """
        self.nodes_info = nodes_info

    def get_idle_nodes(self):
        return [node for node in self.nodes_info if node.is_idle()]

    def get_mixed_nodes(self):
        return [node for node in self.nodes_info if node.is_mixed()]

    def max_capacity(self):
        capacities = [node.cpu_idle for node in self.nodes_info]
        from functools import reduce
        return reduce((lambda x, y: x + y), capacities)

    def get_nodes_for_scheduling(self, jobs_no):
        if jobs_no > self.max_capacity():
            raise AssertionError("Jobs count exceeds maximum cluster capacity.")
        nodes_sorted = self.__sort(self.nodes_info)

        ratio = self.efficiency_ratio
        while int(self.max_capacity() * ratio) < jobs_no:
            ratio = ratio * self.step

        if ratio > 1:
            ratio = 1

        node_ids = []
        from itertools import repeat
        for node in nodes_sorted:
            count = int(round(node.cpu_idle * ratio))
            node_ids.extend(repeat(node.node_id, times=count))

        return node_ids[:jobs_no]

    def __sort(self, nodes):
        from operator import attrgetter
        return sorted(nodes, key=attrgetter('state', 'load', 'cpu_idle'))


def cluster_status_from_raw_stdout(std_out):
    splitted_output = std_out.split("\n")[1:]
    nodes = []
    for line in splitted_output:
        try:
            nodeinfo = NodeInfo(line)
            nodes.append(nodeinfo)
        except Exception:
            logger.info("Unable to parse line, skipping: " + line)
    cluster_info = ClusterState(nodes)
    return cluster_info


def get_cluster_state_from_os():
    from subprocess import check_output, STDOUT
    from shlex import split
    command = "sinfo --states='idle,mixed' --partition=plgrid --format='%n %P %O %T %C'"
    output = check_output(split(command), shell=False, stderr=STDOUT)
    cluster_info = cluster_status_from_raw_stdout(output)
    return cluster_info
