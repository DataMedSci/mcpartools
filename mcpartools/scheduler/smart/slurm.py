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
        for node in nodes_sorted:
            count = int(round(node.cpu_idle * ratio))
            from itertools import repeat
            node_ids.extend(repeat(node.node_id, times=count))

        return node_ids[:jobs_no]

    def __sort(self, nodes):
        from operator import attrgetter
        return sorted(nodes, key=attrgetter('state', 'load', 'cpu_idle'))


def cluster_status_from_raw_stdout(std_out):
    splitted_output = std_out.split("\n")[1:]
    nodes = [NodeInfo(line) for line in splitted_output if line is not ""]
    cluster_info = ClusterState(nodes)
    return cluster_info


def get_cluster_state_from_os():
    # command = "sinfo --states='idle,mixed' --partition=plgrid --format='%n %P %O %T %C'"
    # output = check_output(split(command), shell=True, stderr=STDOUT)
    cluster_info = cluster_status_from_raw_stdout(sample_output)
    return cluster_info


sample_output = """HOSTNAMES PARTITION CPU_LOAD STATE CPUS(A/I/O/T)
p0579 plgrid* 17.27 mixed 20/4/0/24
p0581 plgrid* 4.33 mixed 12/12/0/24
p0583 plgrid* 4.18 mixed 13/11/0/24
p0589 plgrid* 7.17 mixed 12/12/0/24
p0590 plgrid* 9.66 mixed 12/12/0/24
p0593 plgrid* 19.17 mixed 20/4/0/24
p0595 plgrid* 3.09 mixed 11/13/0/24
p0596 plgrid* 2.27 mixed 12/12/0/24
p0599 plgrid* 1.34 mixed 12/12/0/24
p0600 plgrid* 2.18 mixed 12/12/0/24
p0601 plgrid* 4.26 mixed 12/12/0/24
p0602 plgrid* 3.28 mixed 12/12/0/24
p0604 plgrid* 3.23 mixed 12/12/0/24
p0607 plgrid* 1.47 mixed 16/8/0/24
p0613 plgrid* 6.47 mixed 12/12/0/24
p0616 plgrid* 15.13 mixed 19/5/0/24
p0617 plgrid* 5.35 mixed 12/12/0/24
p0618 plgrid* 3.27 mixed 12/12/0/24
p0619 plgrid* 5.35 mixed 12/12/0/24
p0620 plgrid* 17.09 mixed 20/4/0/24
p0624 plgrid* 3.35 mixed 12/12/0/24
p0626 plgrid* 16.24 mixed 20/4/0/24
p0628 plgrid* 16.01 mixed 20/4/0/24
p0630 plgrid* 6.19 mixed 12/12/0/24
p0632 plgrid* 2.25 mixed 12/12/0/24
p0636 plgrid* 17.15 mixed 19/5/0/24
p0637 plgrid* 9.29 mixed 12/12/0/24
p0638 plgrid* 3.33 mixed 12/12/0/24
p0640 plgrid* 4.29 mixed 12/12/0/24
p0646 plgrid* 2.15 mixed 12/12/0/24
p0647 plgrid* 2.14 mixed 12/12/0/24
p0660 plgrid* 7.10 mixed 20/4/0/24
p0668 plgrid* 20.24 mixed 20/4/0/24
p0672 plgrid* 3.16 mixed 12/12/0/24
p0673 plgrid* 15.36 mixed 22/2/0/24
p0674 plgrid* 2.33 mixed 12/12/0/24
p0677 plgrid* 3.39 mixed 12/12/0/24
p0678 plgrid* 19.07 mixed 20/4/0/24
p0680 plgrid* 6.25 mixed 12/12/0/24
p0685 plgrid* 5.98 mixed 6/18/0/24
p0690 plgrid* 6.49 mixed 12/12/0/24
p0694 plgrid* 2.63 mixed 12/12/0/24
p0695 plgrid* 3.27 mixed 12/12/0/24
p0699 plgrid* 1.09 mixed 12/12/0/24
p0701 plgrid* 2.27 mixed 12/12/0/24
p0704 plgrid* 4.29 mixed 12/12/0/24
p0707 plgrid* 3.29 mixed 12/12/0/24
p0710 plgrid* 4.94 mixed 12/12/0/24
p0713 plgrid* 1.10 mixed 12/12/0/24
p0714 plgrid* 1.10 mixed 12/12/0/24
p0719 plgrid* 3.25 mixed 12/12/0/24
p0721 plgrid* 3.26 mixed 12/12/0/24
p0722 plgrid* 3.22 mixed 12/12/0/24
p0725 plgrid* 2.13 mixed 12/12/0/24
p0731 plgrid* 5.38 mixed 19/5/0/24
p0737 plgrid* 2.16 mixed 12/12/0/24
p0738 plgrid* 14.01 mixed 15/9/0/24
p0746 plgrid* 17.10 mixed 17/7/0/24
p0748 plgrid* 4.33 mixed 12/12/0/24
p0750 plgrid* 7.55 mixed 12/12/0/24
p0751 plgrid* 3.30 mixed 12/12/0/24
p0757 plgrid* 6.53 mixed 12/12/0/24
p0759 plgrid* 7.51 mixed 12/12/0/24
p0762 plgrid* 4.20 mixed 12/12/0/24
p0765 plgrid* 6.32 mixed 12/12/0/24
p0766 plgrid* 17.05 mixed 20/4/0/24
p0768 plgrid* 2.18 mixed 12/12/0/24
p0772 plgrid* 18.10 mixed 20/4/0/24
p0774 plgrid* 13.44 mixed 14/10/0/24
p0776 plgrid* 6.14 mixed 12/12/0/24
p0778 plgrid* 0.78 mixed 12/12/0/24
p0784 plgrid* 7.01 mixed 12/12/0/24
p0785 plgrid* 4.77 mixed 12/12/0/24
p0787 plgrid* 1.04 mixed 12/12/0/24
p0791 plgrid* 4.38 mixed 12/12/0/24
p0792 plgrid* 16.18 mixed 18/6/0/24
p0795 plgrid* 2.66 mixed 12/12/0/24
p0800 plgrid* 3.39 mixed 12/12/0/24
p0802 plgrid* 1.24 mixed 12/12/0/24
p0804 plgrid* 4.65 mixed 12/12/0/24
p0805 plgrid* 2.19 mixed 12/12/0/24
p0806 plgrid* 1.04 mixed 12/12/0/24
p0807 plgrid* 3.17 mixed 12/12/0/24
p0808 plgrid* 5.28 mixed 13/11/0/24
p0809 plgrid* 3.63 mixed 12/12/0/24
p0810 plgrid* 4.30 mixed 12/12/0/24
p0812 plgrid* 2.15 mixed 12/12/0/24
p0817 plgrid* 18.29 mixed 20/4/0/24
p0820 plgrid* 3.01 mixed 12/12/0/24
p0822 plgrid* 17.24 mixed 20/4/0/24
p0824 plgrid* 4.28 mixed 12/12/0/24
p0825 plgrid* 0.01 mixed 12/12/0/24
p0827 plgrid* 18.15 mixed 20/4/0/24
p0829 plgrid* 0.74 mixed 12/12/0/24
p0830 plgrid* 2.23 mixed 12/12/0/24
p0831 plgrid* 0.01 mixed 12/12/0/24
p0834 plgrid* 9.31 mixed 12/12/0/24
p0835 plgrid* 9.61 mixed 10/14/0/24
p0836 plgrid* 6.35 mixed 12/12/0/24
p0837 plgrid* 7.12 mixed 12/12/0/24
p0840 plgrid* 3.17 mixed 12/12/0/24
p0842 plgrid* 1.06 mixed 12/12/0/24
p0843 plgrid* 3.21 mixed 12/12/0/24
p0845 plgrid* 8.43 mixed 10/14/0/24
p0846 plgrid* 2.20 mixed 12/12/0/24
p0849 plgrid* 5.42 mixed 12/12/0/24
p0854 plgrid* 5.13 mixed 14/10/0/24
p0857 plgrid* 8.01 mixed 16/8/0/24
p0858 plgrid* 11.22 mixed 16/8/0/24
p0859 plgrid* 3.30 mixed 12/12/0/24
p0863 plgrid* 5.09 mixed 14/10/0/24
p0867 plgrid* 19.15 mixed 20/4/0/24
p0868 plgrid* 3.26 mixed 12/12/0/24
p0871 plgrid* 0.02 mixed 12/12/0/24
p0875 plgrid* 4.35 mixed 12/12/0/24
p0878 plgrid* 18.00 mixed 20/4/0/24
p0879 plgrid* 1.13 mixed 12/12/0/24
p0880 plgrid* 2.12 mixed 12/12/0/24
p0881 plgrid* 1.12 mixed 12/12/0/24
p0882 plgrid* 4.20 mixed 12/12/0/24
p0883 plgrid* 19.26 mixed 22/2/0/24
p0884 plgrid* 7.79 mixed 12/12/0/24
p0889 plgrid* 6.06 mixed 12/12/0/24
p0890 plgrid* 3.99 mixed 12/12/0/24
p0908 plgrid* 3.33 mixed 12/12/0/24
p0911 plgrid* 0.13 mixed 12/12/0/24
p0913 plgrid* 3.26 mixed 12/12/0/24
p0914 plgrid* 3.16 mixed 12/12/0/24
p0916 plgrid* 11.27 mixed 16/8/0/24
p0918 plgrid* 4.24 mixed 12/12/0/24
p0925 plgrid* 6.49 mixed 12/12/0/24
p0931 plgrid* 1.08 mixed 12/12/0/24
p0936 plgrid* 2.13 mixed 12/12/0/24
p0937 plgrid* 1.25 mixed 12/12/0/24
p0938 plgrid* 8.50 mixed 12/12/0/24
p0939 plgrid* 4.32 mixed 12/12/0/24
p0942 plgrid* 20.35 mixed 20/4/0/24
p0945 plgrid* 9.10 mixed 12/12/0/24
p0947 plgrid* 0.23 mixed 12/12/0/24
p0953 plgrid* 1.04 mixed 9/15/0/24
p0956 plgrid* 5.52 mixed 12/12/0/24
p0961 plgrid* 0.24 mixed 12/12/0/24
p0965 plgrid* 3.32 mixed 12/12/0/24
p0970 plgrid* 0.01 mixed 10/14/0/24
p0972 plgrid* 10.42 mixed 12/12/0/24
p0974 plgrid* 17.03 mixed 20/4/0/24
p0978 plgrid* 16.01 mixed 20/4/0/24
p0979 plgrid* 0.29 mixed 12/12/0/24
p0980 plgrid* 18.01 mixed 21/3/0/24
p0981 plgrid* 16.01 mixed 16/8/0/24
p0994 plgrid* 6.36 mixed 12/12/0/24
p0997 plgrid* 4.73 mixed 12/12/0/24
p1004 plgrid* 5.25 mixed 12/12/0/24
p1005 plgrid* 7.10 mixed 14/10/0/24
p1007 plgrid* 2.23 mixed 12/12/0/24
p1008 plgrid* 3.18 mixed 12/12/0/24
p1010 plgrid* 1.07 mixed 12/12/0/24
p1011 plgrid* 4.62 mixed 12/12/0/24
p1013 plgrid* 16.12 mixed 19/5/0/24
p1015 plgrid* 9.47 mixed 12/12/0/24
p1016 plgrid* 3.48 mixed 12/12/0/24
p1018 plgrid* 0.01 mixed 12/12/0/24
p1021 plgrid* 3.18 mixed 12/12/0/24
p1022 plgrid* 3.15 mixed 12/12/0/24
p1030 plgrid* 12.09 mixed 14/10/0/24
p1035 plgrid* 1.08 mixed 12/12/0/24
p1036 plgrid* 3.72 mixed 12/12/0/24
p1039 plgrid* 11.99 mixed 14/10/0/24
p1041 plgrid* 11.99 mixed 14/10/0/24
p1042 plgrid* 2.14 mixed 12/12/0/24
p1043 plgrid* 0.01 mixed 12/12/0/24
p1048 plgrid* 3.24 mixed 12/12/0/24
p1049 plgrid* 2.16 mixed 12/12/0/24
p1050 plgrid* 0.01 mixed 11/13/0/24
p1051 plgrid* 11.11 mixed 17/7/0/24
p1052 plgrid* 2.78 mixed 12/12/0/24
p1053 plgrid* 2.97 mixed 12/12/0/24
p1056 plgrid* 4.53 mixed 12/12/0/24
p1057 plgrid* 4.01 mixed 14/10/0/24
p1058 plgrid* 6.45 mixed 12/12/0/24
p1059 plgrid* 2.36 mixed 12/12/0/24
p1060 plgrid* 8.03 mixed 16/8/0/24
p1061 plgrid* 18.01 mixed 21/3/0/24
p1062 plgrid* 0.58 mixed 12/12/0/24
p1063 plgrid* 4.24 mixed 12/12/0/24
p1065 plgrid* 5.27 mixed 12/12/0/24
p1073 plgrid* 1.07 mixed 12/12/0/24
p1077 plgrid* 5.45 mixed 12/12/0/24
p1080 plgrid* 3.23 mixed 12/12/0/24
p1082 plgrid* 8.00 mixed 12/12/0/24
p1083 plgrid* 3.46 mixed 12/12/0/24
p1088 plgrid* 6.67 mixed 12/12/0/24
p1094 plgrid* 3.19 mixed 12/12/0/24
p1098 plgrid* 3.22 mixed 5/19/0/24
p1102 plgrid* 2.11 mixed 12/12/0/24
p1103 plgrid* 4.05 mixed 12/12/0/24
p1105 plgrid* 1.01 mixed 12/12/0/24
p1106 plgrid* 6.17 mixed 14/10/0/24
p1107 plgrid* 3.68 mixed 12/12/0/24
p1108 plgrid* 4.91 mixed 12/12/0/24
p1110 plgrid* 22.04 mixed 22/2/0/24
p1113 plgrid* 2.13 mixed 12/12/0/24
p1114 plgrid* 1.24 mixed 12/12/0/24
p1118 plgrid* 3.26 mixed 12/12/0/24
p1119 plgrid* 0.05 mixed 12/12/0/24
p1122 plgrid* 7.55 mixed 14/10/0/24
p1124 plgrid* 1.29 mixed 12/12/0/24
p1126 plgrid* 1.09 mixed 12/12/0/24
p1129 plgrid* 5.62 mixed 12/12/0/24
p1131 plgrid* 1.13 mixed 12/12/0/24
p1132 plgrid* 7.25 mixed 12/12/0/24
p1134 plgrid* 2.18 mixed 12/12/0/24
p1137 plgrid* 5.71 mixed 6/18/0/24
p1146 plgrid* 6.58 mixed 12/12/0/24
p1150 plgrid* 22.01 mixed 23/1/0/24
p1153 plgrid* 3.48 mixed 12/12/0/24
p1154 plgrid* 34.66 mixed 16/8/0/24
p1156 plgrid* 3.71 mixed 12/12/0/24
p1157 plgrid* 5.58 mixed 12/12/0/24
p1160 plgrid* 3.07 mixed 13/11/0/24
p1161 plgrid* 4.36 mixed 12/12/0/24
p1163 plgrid* 0.01 mixed 12/12/0/24
p1164 plgrid* 30.81 mixed 13/11/0/24
p1168 plgrid* 30.71 mixed 13/11/0/24
p1169 plgrid* 5.43 mixed 12/12/0/24
p1170 plgrid* 28.33 mixed 13/11/0/24
p1176 plgrid* 41.44 mixed 21/3/0/24
p1179 plgrid* 42.12 mixed 21/3/0/24
p1181 plgrid* 31.46 mixed 13/11/0/24
p1183 plgrid* 28.19 mixed 13/11/0/24
p1184 plgrid* 5.32 mixed 12/12/0/24
p1188 plgrid* 34.42 mixed 17/7/0/24
p1196 plgrid* 0.02 mixed 12/12/0/24
p1197 plgrid* 43.16 mixed 21/3/0/24
p1200 plgrid* 42.11 mixed 21/3/0/24
p1201 plgrid* 3.25 mixed 12/12/0/24
p1204 plgrid* 17.64 mixed 20/4/0/24
p1205 plgrid* 6.89 mixed 12/12/0/24
p1206 plgrid* 16.13 mixed 20/4/0/24
p1208 plgrid* 1.22 mixed 12/12/0/24
p1209 plgrid* 30.60 mixed 13/11/0/24
p1214 plgrid* 0.01 mixed 12/12/0/24
p1219 plgrid* 2.11 mixed 12/12/0/24
p1221 plgrid* 3.24 mixed 12/12/0/24
p1224 plgrid* 12.06 mixed 14/10/0/24
p1231 plgrid* 5.01 mixed 12/12/0/24
p1233 plgrid* 2.19 mixed 12/12/0/24
p1237 plgrid* 3.27 mixed 12/12/0/24
p1241 plgrid* 2.38 mixed 12/12/0/24
p1243 plgrid* 29.37 mixed 13/11/0/24
p1250 plgrid* 28.97 mixed 5/19/0/24
p1252 plgrid* 2.18 mixed 12/12/0/24
p1253 plgrid* 3.63 mixed 12/12/0/24
p1255 plgrid* 29.08 mixed 5/19/0/24
p1257 plgrid* 20.93 mixed 22/2/0/24
p1258 plgrid* 27.19 mixed 11/13/0/24
p1261 plgrid* 1.42 mixed 12/12/0/24
p1263 plgrid* 9.97 mixed 11/13/0/24
p1264 plgrid* 29.33 mixed 13/11/0/24
p1265 plgrid* 4.56 mixed 12/12/0/24
p1275 plgrid* 28.42 mixed 13/11/0/24
p1280 plgrid* 0.01 mixed 12/12/0/24
p1284 plgrid* 35.38 mixed 16/8/0/24
p1286 plgrid* 1.03 mixed 12/12/0/24
p1289 plgrid* 34.22 mixed 13/11/0/24
p1292 plgrid* 14.12 mixed 19/5/0/24
p1300 plgrid* 31.46 mixed 13/11/0/24
p1304 plgrid* 7.28 mixed 12/12/0/24
p1305 plgrid* 4.44 mixed 12/12/0/24
p1308 plgrid* 21.37 mixed 22/2/0/24
p1309 plgrid* 0.05 mixed 11/13/0/24
p1311 plgrid* 26.22 mixed 12/12/0/24
p1315 plgrid* 9.23 mixed 12/12/0/24
p1323 plgrid* 9.82 mixed 12/12/0/24
p1326 plgrid* 4.47 mixed 12/12/0/24
p1331 plgrid* 1.09 mixed 12/12/0/24
p1332 plgrid* 4.42 mixed 12/12/0/24
p1335 plgrid* 0.03 mixed 12/12/0/24
p1338 plgrid* 1.19 mixed 12/12/0/24
p1339 plgrid* 1.04 mixed 12/12/0/24
p1340 plgrid* 0.01 mixed 12/12/0/24
p1342 plgrid* 30.69 mixed 13/11/0/24
p1345 plgrid* 30.11 mixed 13/11/0/24
p1347 plgrid* 0.01 mixed 12/12/0/24
p1349 plgrid* 27.03 mixed 13/11/0/24
p1350 plgrid* 1.12 mixed 12/12/0/24
p1356 plgrid* 5.12 mixed 12/12/0/24
p1362 plgrid* 39.17 mixed 19/5/0/24
p1365 plgrid* 3.38 mixed 12/12/0/24
p1370 plgrid* 3.44 mixed 12/12/0/24
p1371 plgrid* 1.14 mixed 12/12/0/24
p1377 plgrid* 0.01 mixed 12/12/0/24
p1378 plgrid* 1.09 mixed 12/12/0/24
p1381 plgrid* 29.07 mixed 13/11/0/24
p1388 plgrid* 0.01 mixed 12/12/0/24
p1390 plgrid* 0.01 mixed 12/12/0/24
p1391 plgrid* 31.07 mixed 13/11/0/24
p1393 plgrid* 11.22 mixed 12/12/0/24
p1394 plgrid* 42.08 mixed 21/3/0/24
p1395 plgrid* 4.32 mixed 12/12/0/24
p1396 plgrid* 1.08 mixed 12/12/0/24
p1400 plgrid* 41.41 mixed 21/3/0/24
p1401 plgrid* 5.53 mixed 12/12/0/24
p1402 plgrid* 0.01 mixed 12/12/0/24
p1403 plgrid* 1.60 mixed 12/12/0/24
p1404 plgrid* 4.66 mixed 12/12/0/24
p1414 plgrid* 28.24 mixed 13/11/0/24
p1421 plgrid* 0.01 mixed 12/12/0/24
p1422 plgrid* 31.42 mixed 14/10/0/24
p1428 plgrid* 3.17 mixed 12/12/0/24
p1433 plgrid* 5.22 mixed 12/12/0/24
p1435 plgrid* 3.34 mixed 12/12/0/24
p1439 plgrid* 26.08 mixed 11/13/0/24
p1447 plgrid* 0.01 mixed 12/12/0/24
p1450 plgrid* 1.05 mixed 12/12/0/24
p1455 plgrid* 31.61 mixed 14/10/0/24
p1456 plgrid* 1.11 mixed 12/12/0/24
p1461 plgrid* 43.07 mixed 22/2/0/24
p1462 plgrid* 3.32 mixed 12/12/0/24
p1469 plgrid* 2.19 mixed 12/12/0/24
p1470 plgrid* 4.62 mixed 12/12/0/24
p1471 plgrid* 41.19 mixed 21/3/0/24
p1475 plgrid* 31.34 mixed 13/11/0/24
p1476 plgrid* 7.55 mixed 12/12/0/24
p1479 plgrid* 5.43 mixed 12/12/0/24
p1480 plgrid* 29.33 mixed 13/11/0/24
p1481 plgrid* 2.46 mixed 12/12/0/24
p1484 plgrid* 27.32 mixed 11/13/0/24
p1488 plgrid* 5.42 mixed 12/12/0/24
p1501 plgrid* 27.16 mixed 13/11/0/24
p1503 plgrid* 5.14 mixed 12/12/0/24
p1507 plgrid* 1.12 mixed 12/12/0/24
p1509 plgrid* 3.77 mixed 12/12/0/24
p1513 plgrid* 3.29 mixed 12/12/0/24
p1514 plgrid* 1.95 mixed 12/12/0/24
p1515 plgrid* 1.16 mixed 12/12/0/24
p1516 plgrid* 0.01 mixed 12/12/0/24
p1518 plgrid* 0.06 mixed 12/12/0/24
p1519 plgrid* 2.16 mixed 12/12/0/24
p1521 plgrid* 30.28 mixed 13/11/0/24
p1522 plgrid* 1.09 mixed 12/12/0/24
p1523 plgrid* 1.08 mixed 12/12/0/24
p1524 plgrid* 25.01 mixed 13/11/0/24
p1526 plgrid* 27.20 mixed 13/11/0/24
p1529 plgrid* 29.32 mixed 13/11/0/24
p1536 plgrid* 2.21 mixed 12/12/0/24
p1538 plgrid* 12.01 mixed 14/10/0/24
p1539 plgrid* 13.06 mixed 14/10/0/24
p1544 plgrid* 2.21 mixed 12/12/0/24
p1549 plgrid* 3.36 mixed 12/12/0/24
p1551 plgrid* 4.48 mixed 12/12/0/24
p1552 plgrid* 3.25 mixed 12/12/0/24
p1556 plgrid* 8.35 mixed 12/12/0/24
p1557 plgrid* 1.05 mixed 12/12/0/24
p1560 plgrid* 4.80 mixed 12/12/0/24
p1562 plgrid* 2.16 mixed 12/12/0/24
p1567 plgrid* 2.16 mixed 12/12/0/24
p1576 plgrid* 30.21 mixed 14/10/0/24
p1578 plgrid* 3.27 mixed 12/12/0/24
p1583 plgrid* 6.01 mixed 14/10/0/24
p1586 plgrid* 30.04 mixed 13/11/0/24
p1590 plgrid* 28.39 mixed 13/11/0/24
p1592 plgrid* 5.17 mixed 12/12/0/24
p1593 plgrid* 29.27 mixed 13/11/0/24
p1603 plgrid* 15.21 mixed 18/6/0/24
p1604 plgrid* 0.01 mixed 12/12/0/24
p1606 plgrid* 12.04 mixed 14/10/0/24
p1613 plgrid* 2.08 mixed 12/12/0/24
p1615 plgrid* 3.30 mixed 12/12/0/24
p1617 plgrid* 3.12 mixed 12/12/0/24
p1620 plgrid* 3.31 mixed 12/12/0/24
p1621 plgrid* 17.12 mixed 20/4/0/24
p1623 plgrid* 18.20 mixed 20/4/0/24
p1624 plgrid* 41.17 mixed 21/3/0/24
p1627 plgrid* 40.98 mixed 21/3/0/24
p1628 plgrid* 4.09 mixed 12/12/0/24
p1633 plgrid* 44.31 mixed 21/3/0/24
p1634 plgrid* 41.06 mixed 21/3/0/24
p1635 plgrid* 7.22 mixed 12/12/0/24
p1636 plgrid* 42.08 mixed 21/3/0/24
p1637 plgrid* 41.01 mixed 21/3/0/24
p1638 plgrid* 7.66 mixed 12/12/0/24
p1644 plgrid* 27.33 mixed 13/11/0/24
p1645 plgrid* 1.06 mixed 12/12/0/24
p1647 plgrid* 24.98 mixed 13/11/0/24
p1650 plgrid* 2.50 mixed 12/12/0/24
p1656 plgrid* 27.16 mixed 13/11/0/24
p1672 plgrid* 27.19 mixed 13/11/0/24
p1691 plgrid* 13.97 mixed 16/8/0/24
p1699 plgrid* 5.35 mixed 12/12/0/24
p1700 plgrid* 0.01 mixed 12/12/0/24
p1707 plgrid* 0.01 mixed 12/12/0/24
p1709 plgrid* 1.11 mixed 12/12/0/24
p1710 plgrid* 1.98 mixed 12/12/0/24
p1714 plgrid* 25.01 mixed 13/11/0/24
p1716 plgrid* 27.15 mixed 13/11/0/24
p1726 plgrid* 30.26 mixed 13/11/0/24
p1748 plgrid* 18.24 mixed 20/4/0/24
p1754 plgrid* 3.39 mixed 12/12/0/24
p1759 plgrid* 6.54 mixed 12/12/0/24
p1760 plgrid* 4.32 mixed 12/12/0/24
p1761 plgrid* 0.94 mixed 12/12/0/24
p1762 plgrid* 17.00 mixed 20/4/0/24
p1763 plgrid* 2.19 mixed 12/12/0/24
p1766 plgrid* 16.06 mixed 20/4/0/24
p1769 plgrid* 17.11 mixed 20/4/0/24
p1771 plgrid* 5.34 mixed 12/12/0/24
p1776 plgrid* 3.33 mixed 12/12/0/24
p1777 plgrid* 2.23 mixed 12/12/0/24
p1779 plgrid* 0.01 mixed 12/12/0/24
p1780 plgrid* 3.24 mixed 12/12/0/24
p1781 plgrid* 16.43 mixed 20/4/0/24
p1801 plgrid* 3.45 mixed 12/12/0/24
p1802 plgrid* 5.69 mixed 12/12/0/24
p1803 plgrid* 5.01 mixed 12/12/0/24
p1810 plgrid* 3.72 mixed 12/12/0/24
p1814 plgrid* 1.52 mixed 12/12/0/24
p1818 plgrid* 3.39 mixed 12/12/0/24
p1822 plgrid* 2.21 mixed 12/12/0/24
p1826 plgrid* 5.47 mixed 12/12/0/24
p1833 plgrid* 1.09 mixed 12/12/0/24
p1847 plgrid* 0.01 mixed 12/12/0/24
p1850 plgrid* 0.45 mixed 12/12/0/24
p1903 plgrid* 3.32 mixed 12/12/0/24
p1906 plgrid* 2.33 mixed 12/12/0/24
p1907 plgrid* 0.01 mixed 12/12/0/24
p1910 plgrid* 6.85 mixed 12/12/0/24
p1913 plgrid* 6.41 mixed 12/12/0/24
p1914 plgrid* 3.93 mixed 12/12/0/24
p1916 plgrid* 8.03 mixed 12/12/0/24
p1917 plgrid* 4.39 mixed 12/12/0/24
p1919 plgrid* 4.71 mixed 12/12/0/24
p1920 plgrid* 1.12 mixed 12/12/0/24
p1921 plgrid* 7.10 mixed 13/11/0/24
p1922 plgrid* 4.50 mixed 12/12/0/24
p1923 plgrid* 5.84 mixed 12/12/0/24
p1924 plgrid* 6.79 mixed 12/12/0/24
p1925 plgrid* 4.31 mixed 12/12/0/24
p1928 plgrid* 18.18 mixed 20/4/0/24
p1929 plgrid* 18.20 mixed 20/4/0/24
p1931 plgrid* 19.39 mixed 20/4/0/24
p1932 plgrid* 18.13 mixed 20/4/0/24
p1933 plgrid* 16.01 mixed 20/4/0/24
p1934 plgrid* 16.01 mixed 20/4/0/24
p1935 plgrid* 16.01 mixed 20/4/0/24
p1936 plgrid* 17.06 mixed 20/4/0/24
p1937 plgrid* 6.54 mixed 12/12/0/24
p1938 plgrid* 16.01 mixed 20/4/0/24
p1939 plgrid* 17.03 mixed 20/4/0/24
p1940 plgrid* 18.13 mixed 20/4/0/24
p1941 plgrid* 7.94 mixed 12/12/0/24
p1942 plgrid* 0.18 mixed 12/12/0/24
p1943 plgrid* 17.06 mixed 20/4/0/24
p1944 plgrid* 7.57 mixed 12/12/0/24
p1959 plgrid* 1.05 mixed 11/13/0/24
p1963 plgrid* 3.26 mixed 12/12/0/24
p1964 plgrid* 2.18 mixed 12/12/0/24
p1967 plgrid* 5.43 mixed 12/12/0/24
p1968 plgrid* 2.26 mixed 12/12/0/24
p1970 plgrid* 1.94 mixed 12/12/0/24
p1971 plgrid* 13.11 mixed 14/10/0/24
p1972 plgrid* 14.15 mixed 14/10/0/24
p1973 plgrid* 1.07 mixed 12/12/0/24
p1975 plgrid* 2.12 mixed 12/12/0/24
p1981 plgrid* 5.46 mixed 12/12/0/24
p1982 plgrid* 4.22 mixed 12/12/0/24
p1983 plgrid* 3.06 mixed 12/12/0/24
p1984 plgrid* 5.91 mixed 12/12/0/24
p1985 plgrid* 5.75 mixed 12/12/0/24
p1987 plgrid* 3.27 mixed 12/12/0/24
p1988 plgrid* 3.63 mixed 12/12/0/24
p1989 plgrid* 5.32 mixed 12/12/0/24
p1991 plgrid* 2.11 mixed 12/12/0/24
p1993 plgrid* 12.16 mixed 17/7/0/24
p1997 plgrid* 5.31 mixed 12/12/0/24
p2038 plgrid* 20.01 mixed 22/2/0/24
p2047 plgrid* 0.01 mixed 7/17/0/24
p2055 plgrid* 1.17 mixed 12/12/0/24
p2063 plgrid* 3.27 mixed 12/12/0/24
p2071 plgrid* 0.62 mixed 12/12/0/24
p2072 plgrid* 3.19 mixed 12/12/0/24
p2077 plgrid* 2.18 mixed 12/12/0/24
p2081 plgrid* 5.28 mixed 12/12/0/24
p2082 plgrid* 2.45 mixed 12/12/0/24
p2084 plgrid* 2.39 mixed 12/12/0/24
p2087 plgrid* 2.10 mixed 12/12/0/24
p2092 plgrid* 4.01 mixed 5/19/0/24
p2100 plgrid* 12.14 mixed 17/7/0/24
p2106 plgrid* 3.29 mixed 12/12/0/24
p2111 plgrid* 29.85 mixed 15/9/0/24
p2122 plgrid* 9.08 mixed 13/11/0/24
p2126 plgrid* 0.01 mixed 12/12/0/24
p2130 plgrid* 16.57 mixed 20/4/0/24
p2131 plgrid* 4.10 mixed 8/16/0/24
p2135 plgrid* 6.12 mixed 12/12/0/24
p2136 plgrid* 4.32 mixed 12/12/0/24
p2141 plgrid* 3.94 mixed 12/12/0/24
p2187 plgrid* 7.27 mixed 14/10/0/24
p2188 plgrid* 13.34 mixed 17/7/0/24
p2190 plgrid* 12.01 mixed 14/10/0/24
p2194 plgrid* 6.49 mixed 12/12/0/24
p2195 plgrid* 1.10 mixed 12/12/0/24
p2196 plgrid* 5.41 mixed 12/12/0/24
p2198 plgrid* 9.02 mixed 16/8/0/24
p2199 plgrid* 10.21 mixed 16/8/0/24
p2204 plgrid* 3.22 mixed 12/12/0/24
p2206 plgrid* 2.17 mixed 12/12/0/24
p2207 plgrid* 3.19 mixed 12/12/0/24
p2211 plgrid* 1.10 mixed 12/12/0/24
p2214 plgrid* 1.11 mixed 12/12/0/24
p2216 plgrid* 3.28 mixed 12/12/0/24
p2218 plgrid* 17.05 mixed 20/4/0/24
p2219 plgrid* 17.06 mixed 20/4/0/24
p2220 plgrid* 17.03 mixed 20/4/0/24
p2221 plgrid* 17.11 mixed 20/4/0/24
p2222 plgrid* 18.38 mixed 20/4/0/24
p2223 plgrid* 17.09 mixed 20/4/0/24
p2224 plgrid* 19.30 mixed 20/4/0/24
p2225 plgrid* 16.65 mixed 20/4/0/24
p2226 plgrid* 17.10 mixed 20/4/0/24
p2227 plgrid* 2.99 mixed 13/11/0/24
p2228 plgrid* 18.44 mixed 20/4/0/24
p2230 plgrid* 16.01 mixed 20/4/0/24
p2232 plgrid* 16.01 mixed 20/4/0/24
p2238 plgrid* 17.73 mixed 19/5/0/24
p2251 plgrid* 4.07 mixed 12/12/0/24
p2252 plgrid* 5.66 mixed 12/12/0/24
p2255 plgrid* 6.41 mixed 12/12/0/24
p2257 plgrid* 1.03 mixed 3/21/0/24
p2261 plgrid* 5.02 mixed 12/12/0/24
p2266 plgrid* 22.02 mixed 22/2/0/24
p2268 plgrid* 13.03 mixed 18/6/0/24
p2269 plgrid* 3.19 mixed 12/12/0/24
p2270 plgrid* 7.37 mixed 12/12/0/24
p2274 plgrid* 6.71 mixed 13/11/0/24
p2275 plgrid* 5.26 mixed 13/11/0/24
p2276 plgrid* 2.24 mixed 12/12/0/24
p2278 plgrid* 5.71 mixed 12/12/0/24
p2279 plgrid* 5.79 mixed 12/12/0/24
p2280 plgrid* 2.78 mixed 13/11/0/24
p2282 plgrid* 7.04 mixed 15/9/0/24
p0603 plgrid* 4.41 idle 0/24/0/24
p1254 plgrid* 0.01 idle 0/24/0/24
p1267 plgrid* 0.01 idle 0/24/0/24
p1268 plgrid* 0.01 idle 0/24/0/24
p1298 plgrid* 0.01 idle 0/24/0/24
p1313 plgrid* 0.01 idle 0/24/0/24
p1317 plgrid* 0.01 idle 0/24/0/24
p1320 plgrid* 0.01 idle 0/24/0/24
p1372 plgrid* 0.26 idle 0/24/0/24
p1411 plgrid* 0.01 idle 0/24/0/24
p1412 plgrid* 0.01 idle 0/24/0/24
p1416 plgrid* 0.01 idle 0/24/0/24
p1493 plgrid* 0.19 idle 0/24/0/24
p1537 plgrid* 0.01 idle 0/24/0/24
p1728 plgrid* 0.01 idle 0/24/0/24
"""
