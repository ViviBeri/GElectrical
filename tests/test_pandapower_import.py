import unittest

from gelectrical.model.pandapower_import import summarize_network


class SummarizeNetworkTests(unittest.TestCase):
    def test_summarizes_populated_tables_and_ignores_empty_tables(self):
        network = {
            "bus": [1, 2, 3],
            "line": [1],
            "trafo": [],
            "load": [1, 2],
            "ext_grid": [1],
        }

        self.assertEqual(
            summarize_network(network),
            "Buses: 3\nLines: 1\nLoads: 2\nExternal grids: 1",
        )

    def test_handles_missing_tables(self):
        self.assertEqual(
            summarize_network({}),
            "The imported network contains no recognized elements.",
        )


if __name__ == "__main__":
    unittest.main()
