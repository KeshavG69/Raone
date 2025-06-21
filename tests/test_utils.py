# example tests for utils.py
import pytest

def test_time_formats():
    result = utils.format_time(11, 30)
    assert result == "11:30"