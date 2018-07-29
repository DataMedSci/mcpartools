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

    def get_nodes_for_scheduling(self, jobs_no, utilisation, ratio):
        if jobs_no > self.max_capacity():
            raise AssertionError("Jobs count exceeds maximum cluster capacity.")
        nodes_sorted = self.__sort(self.nodes_info)

        '''
        Iteratively increase cluster nodes utilisation based on given params.
        If, for the given initial utilisation, it is impossible to contain all required jobs,
        multiply utilisation by given ratio.
        In other words, utilisation 0.5 means that at minimum half of the available cores on single node
        will be used (if necessary). Ratio 1.08 means that if initial utilisation is not enough, in the next iteration
        algorithm will try to use utilisation of 0.5*1.08 = 0.54 (8% bigger).
        '''
        util = utilisation
        while int(self.max_capacity() * util) < jobs_no:
            util = util * ratio

        if util > 1:
            util = 1

        node_ids = []
        from itertools import repeat
        for node in nodes_sorted:
            count = int(round(node.cpu_idle * util))
            node_ids.extend(repeat(node.node_id, times=count))

        return node_ids[:jobs_no]

    def __sort(self, nodes):
        from operator import attrgetter
        return sorted(nodes, key=attrgetter('state', 'load', 'cpu_idle'))


def cluster_status_from_raw_stdout(std_out):
    import sys
    if sys.version_info[0] < 3:
        output = std_out.decode("UTF-8")
    else:
        output = std_out
    splitted_output = output.split("\n")[1:]
    nodes = []
    for line in splitted_output:
        try:
            nodeinfo = NodeInfo(line)
            nodes.append(nodeinfo)
        except Exception:
            logger.info("Unable to parse line, skipping: " + line)
    cluster_info = ClusterState(nodes)
    return cluster_info


def get_cluster_state_from_os(partition):
    from subprocess import check_output, STDOUT
    from shlex import split
    command = "sinfo --states='idle,mixed' --partition={partition} --format='%n %P %O %T %C'" \
        .format(partition=partition)
    output = check_output(split(command), shell=False, stderr=STDOUT)
    cluster_info = cluster_status_from_raw_stdout(output)
    return cluster_info
