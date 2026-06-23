from src.etl.normaliser import *

def test_ticker():
    assert normalize_ticker(" tcs ") == "TCS"

def test_year():
    assert normalize_year(2024.0) == 2024
