import time
import os
import pytest

@pytest.fixture(scope='function', autouse=True)
def handler():
    pass


def test_one():
    print("process id running in pytest: ", os.getpid())
    while True:
        time.sleep(1)
    assert 1 == 1