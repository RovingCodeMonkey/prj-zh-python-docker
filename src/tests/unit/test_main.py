from app import main


def test_generic_exception_handler():
    assert main.generic_exception_handler("hello", "world").status_code == 500
