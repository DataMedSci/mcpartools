from itertools import repeat
from unittest import TestCase

from mcpartools.scheduler.smart.slurm import cluster_status_from_raw_stdout


class TestClusterInfo(TestCase):
    raw_stdout = """HOSTNAMES PARTITION NODES CPU_LOAD STATE CPUS(A/I/O/T)
p0615 plgrid* 3.92 mixed 16/8/0/24
p0620 plgrid* 0.41 idle 0/24/0/24
p0627 plgrid* 4.00 mixed 16/8/0/24"""
    invalid_raw_stdout = """HOSTNAMES PARTITION NODES CPU_LOAD STATE CPUS(A/I/O/T)
p0615 plgrid* 3.92 mixed [16/8/0/24
p0615 plgrid* 3.92 mixed 16/8/0/24
p0620 plgrid* 0.41 idle 0/24/0/24
p0627 plgrid* 4.00 mixed 16/8/0/24

"""

    def test_cluster_status_from_raw_stdout(self):
        cluster_status = cluster_status_from_raw_stdout(self.raw_stdout)
        self.assertEquals(len(cluster_status.nodes_info), 3)

    def test_should_skip_invalid_line_while_building_cluster_status_from_raw_stdout(self):
        cluster_status = cluster_status_from_raw_stdout(self.invalid_raw_stdout)
        self.assertEquals(len(cluster_status.nodes_info), 3)

    def test_get_idle_nodes(self):
        cluster_status = cluster_status_from_raw_stdout(self.raw_stdout)
        idle = cluster_status.get_idle_nodes()
        self.assertEquals(len(idle), 1)

        idle_ids = [node.node_id for node in idle]
        self.assertEquals(idle_ids, ["p0620"])

    def test_get_mixed_nodes(self):
        cluster_status = cluster_status_from_raw_stdout(self.raw_stdout)
        idle = cluster_status.get_mixed_nodes()
        self.assertEquals(len(idle), 2)

        idle_ids = [node.node_id for node in idle]
        self.assertEquals(idle_ids, ["p0615", "p0627"])

    def test_get_nodes_for_scheduling_1(self):
        cluster_status = cluster_status_from_raw_stdout(self.raw_stdout)
        nodes = cluster_status.get_nodes_for_scheduling(5)
        self.assertEquals(nodes, ['p0620', 'p0620', 'p0620', 'p0620', 'p0620'])

    def test_get_nodes_for_scheduling_2(self):
        cluster_status = cluster_status_from_raw_stdout(self.raw_stdout)
        nodes = cluster_status.get_nodes_for_scheduling(20)
        expected = []
        expected.extend(repeat('p0620', 12))
        expected.extend(repeat('p0615', 4))
        expected.extend(repeat('p0627', 4))
        self.assertEquals(nodes, expected)

    def test_get_nodes_for_scheduling_3(self):
        cluster_status = cluster_status_from_raw_stdout(self.raw_stdout)
        nodes = cluster_status.get_nodes_for_scheduling(30)
        expected = []
        expected.extend(repeat('p0620', 19))
        expected.extend(repeat('p0615', 6))
        expected.extend(repeat('p0627', 5))
        self.assertEquals(nodes, expected)

    def test_get_nodes_for_scheduling_4(self):
        cluster_status = cluster_status_from_raw_stdout(self.raw_stdout)
        nodes = cluster_status.get_nodes_for_scheduling(31)
        expected = []
        expected.extend(repeat('p0620', 19))
        expected.extend(repeat('p0615', 6))
        expected.extend(repeat('p0627', 6))
        self.assertEquals(nodes, expected)

    def test_get_nodes_for_scheduling_5(self):
        cluster_status = cluster_status_from_raw_stdout(self.raw_stdout)
        nodes = cluster_status.get_nodes_for_scheduling(39)
        expected = []
        expected.extend(repeat('p0620', 24))
        expected.extend(repeat('p0615', 8))
        expected.extend(repeat('p0627', 7))
        self.assertEquals(nodes, expected)

    def test_get_nodes_for_scheduling_6(self):
        cluster_status = cluster_status_from_raw_stdout(self.raw_stdout)
        nodes = cluster_status.get_nodes_for_scheduling(40)
        expected = []
        expected.extend(repeat('p0620', 24))
        expected.extend(repeat('p0615', 8))
        expected.extend(repeat('p0627', 8))
        self.assertEquals(nodes, expected)
