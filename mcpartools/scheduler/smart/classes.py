class NodeInfo:
    def __init__(self, line):
        parameters = line.split(" ")
        self.node_id = parameters[0]
        self.partition = parameters[1]
        self.load = parameters[3]
        self.cpu_info = CpuInfo(parameters[4])
        self.state = parameters[5]

    def is_idle(self):
        return self.state == "idle"

    def is_mixed(self):
        return self.state == "mixed"


class CpuInfo:
    def __init__(self, data):
        parameters = data.split("/")
        self.available = parameters[0]
        self.idle = parameters[1]
        self.other = parameters[2]
        self.total = parameters[3]


class ClusterInfo:
    def __init__(self, nodes_info):
        """

        :type nodes_info: list of NodeInfo
        """
        self.nodes_info = nodes_info

    def get_idle_nodes(self):
        return [node.node_id for node in self.nodes_info if node.is_idle()]

    def get_mixed_nodes(self):
        return [node.node_id for node in self.nodes_info if node.is_mixed()]

    def zipWith(self, clusterInfo):
        return ClusterInfo(self.nodes_info.extend(clusterInfo.nodes_info))


