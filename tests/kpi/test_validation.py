import os


def test_log_exists():
    assert os.path.exists("output/ratio_edge_cases.log")