from helper.util import get_driver, sleep
import pytest

driver = None
config = None


@pytest.fixture(scope='session')
def sess_scope():
    driver, config = get_driver()
    pass


# 定义全局方法
def setup_module():
    # driver, config = get_driver()
    pass


def teardown_module(metadata):
    # driver.close()

    pass
