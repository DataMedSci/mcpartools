from shlex import split
from subprocess import check_output, STDOUT


class NodeInfo:
    def __init__(self, line):
        parameters = line.split(" ")
        self.node_id = parameters[0]
        self.partition = parameters[1]
        self.load = parameters[3]
        self.cpu_info = CpuInfo(parameters[4])
        self.state = parameters[5]

        print(self)

    def is_idle(self):
        return self.state == "idle"

    def is_mixed(self):
        return self.state == "mixed"


class CpuInfo:
    def __init__(self, data):
        cpu = data.split("/")
        self.available = int(cpu[0])
        self.idle = int(cpu[1])
        self.other = int(cpu[2])
        self.total = int(cpu[3])


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
        return [node.cpu_info.idle for node in self.nodes_info]

    def get_nodes_for_scheduling(self, jobs_no):
        pass


def cluster_status_from_raw_stdout(std_out):
    splitted_output = std_out.split("\n")[1:]
    nodes = [NodeInfo(line) for line in splitted_output]
    cluster_info = ClusterState(nodes)
    return cluster_info


def get_cluster_state_from_os():
    command = "sinfo --states='idle,mixed' --partition=plgrid --format='%n %P %O %C %T'"
    output = check_output(split(command), shell=True, stderr=STDOUT)
    cluster_info = cluster_status_from_raw_stdout(output)
    return cluster_info
