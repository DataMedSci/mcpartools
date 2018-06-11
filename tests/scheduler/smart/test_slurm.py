from unittest import TestCase
from mcpartools.scheduler.smart.slurm import cluster_status_from_raw_stdout


class TestClusterInfo(TestCase):
    raw_stdout = """HOSTNAMES PARTITION NODES CPU_LOAD CPUS(A/I/O/T) STATE
p0615 plgrid* 1 3.92 16/8/0/24 mixed
p0620 plgrid* 1 0.41 0/24/0/24 idle
p0627 plgrid* 1 4.00 16/8/0/24 mixed"""

    def test_cluster_status_from_raw_stdout(self):
        cluster_status = cluster_status_from_raw_stdout(self.raw_stdout)
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
