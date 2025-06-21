import pytest

def test_arg(response_args):
    result = whatsqap_response.arg(response_args)
    assert attype(result)
