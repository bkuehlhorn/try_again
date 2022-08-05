# content of conftest.py
import logging

import pytest

import dict_json

logging.basicConfig(level=logging.INFO)


def pytest_addoption(parser):
    parser.addoption("--all", action="store_true", help="run all combinations")
    # parser.addoption("--debug", action="store_true",
    #     help="Logger Trace level")
    parser.addoption("--print", action="store_true", help="print all keys")


def pytest_generate_tests(metafunc):
    if "param1" in metafunc.fixturenames:
        if metafunc.config.getoption("all"):
            end = 5
        else:
            end = 2
        metafunc.parametrize("param1", range(end))

    if "debug" in metafunc.fixturenames:
        if metafunc.config.getoption("debug"):
            logging.basicConfig(level=logging.DEBUG)
        # metafunc.parametrize("debug", metafunc.config.getoption('debug'))

    if "print" in metafunc.fixturenames:
        print = metafunc.config.getoption("print")

        # metafunc.parametrize("print", print)


def pytest_addoption(parser):
    parser.addoption(
        "--cmdopt", action="store", default="type1", help="my option: type1 or type2"
    )
    parser.addoption("--all", action="store", default=False, help="do all types")
    parser.addoption("--print", action="store", default=False, help="print all keys")


@pytest.fixture
def cmdopt(request):
    return request.config.getoption("--cmdopt")


@pytest.fixture(scope="module")
def debug(request):
    dict_json.logging.basicConfig(level=logging.DEBUG) if request.config.getoption(
        "--debug"
    ) else ""
    return request.config.getoption("--debug")


@pytest.fixture(scope="module")
def printKeys(request):
    return request.config.getoption("--print")
