import json

import pytest

from dict_json import dict_json

# import yaml

delimiter = dict_json.DELIMITER
# delimiter = '\0'
# dict_json.DELIMITER = delimiter

# from .conftest import logging
import logging

# logging.basicConfig(level=logging.INFO)
logging.basicConfig(level=logging.DEBUG)
from dict_json import dict_json

"""
Generator for json
Need to generate dict and list test data.
d(5)(1:l(4)(d(2))

l(0:3, d
d(4)

"""


def d(*arg, n=1):
    """Create a test dictionary
    Number of fields in dictionary
    keys are k99, values are random
    :param n: Number of keys in test dict
    :return:
    """
    d = {}
    for x in range(n):
        d[f"k{x}"] = "x" + ("s" * x) if len(arg) == 0 else arg[x % len(arg)].copy()
    return d


def l(*arg, n=1):
    """Create test list
    Number of elements in list
    values are random

    :param n: Number of elements in test list
    :return:
    """
    if arg == ():
        element = lambda x: "x" + ("s" * x)
    else:
        element = lambda x: arg[x % len(arg)].copy()
    ls = [None] * n
    for index in range(n):
        ls[index] = element(index)
    return ls


d01 = d(n=3)
d02 = d(n=3)

l01 = l(n=3)
l02 = l(n=3)

d01l = d(n=3)
d01l["d0"] = l01
d01l["d1"] = l02
d01l["d2"] = d02

d022 = d(l01, l01, d01, n=3)

l03 = l(d02, n=2)
l04 = l(l01, n=3)
l05 = l(l04, n=3)


j01s = """
{
"a": 1,
"b":
    {
        "c": 3,
        "d": 4
    }
}
"""
j01Ks = ["a", "b:c", "b:d"]

y01s = """
a: 1
b:
    c: 3
    d: 4
"""

j02s = """
{
"a": 1,
"b":
    [
        {
            "c": 3,
            "d": 4
        },
        {
            "c": 5,
            "d": 6
        }
    ]
}
"""
j02Ks = ["a", "b:0:c", "b:0:d", "b:1:c", "b:1:d"]

normal_dict = {
    "a": "0",
    "b": {
        "a": "1.0",
        "b": "1.1",
    },
    "c": {
        "a": "2.0",
        "b": {
            "a": "2.1.0",
            "b": "2.1.1",
        },
    },
}
#
# @pytest.fixture
# def printKeys(request):
#     return request.config.getoption("--print")


class TestGetKeys(object):
    def test_get_keys_d01(self, printKeys, debug):
        d01Ks = ["k0", "k1", "k2"]
        d01K = dict_json.getKeys(d01)
        print(f"keys: {d01K}") if printKeys else ""
        assert len(d01K) == len(d01Ks)
        assert d01K == d01Ks

    def test_get_keys_d02(self, printKeys, debug):
        d02Ks = [
            "k0:0",
            "k0:1",
            "k0:2",
            "k1:0",
            "k1:1",
            "k1:2",
            "k2:k0",
            "k2:k1",
            "k2:k2",
        ]
        d02K = dict_json.getKeys(d022)
        print(f"keys: {d02K}") if printKeys else ""
        assert len(d02K) == len(d02Ks)
        assert d02K == d02Ks

    def test_get_keys_d02List(self, printKeys, debug):
        d02Ks = [
            ["k0", "0"],
            ["k0", "1"],
            ["k0", "2"],
            ["k1", "0"],
            ["k1", "1"],
            ["k1", "2"],
            ["k2", "k0"],
            ["k2", "k1"],
            ["k2", "k2"],
        ]
        d02K = dict_json.getKeys(d022, seralize=False)
        print(f"keys: {d02K}") if printKeys else ""
        assert len(d02K) == len(d02Ks)
        assert d02K == d02Ks

    def test_get_keys_l01(self, printKeys, debug):
        l01Ks = ["0", "1", "2"]
        l01K = dict_json.getKeys(l01)
        print(f"keys: {l01K}") if printKeys else ""
        assert len(l01K) == len(l01Ks)
        assert l01K == l01Ks

    def test_get_keys_l04(self, printKeys, debug):
        l04Ks = ["0:0", "0:1", "0:2", "1:0", "1:1", "1:2", "2:0", "2:1", "2:2"]
        l04K = dict_json.getKeys(l04)
        print(f"keys: {l04K}") if printKeys else ""
        assert len(l04K) == len(l04Ks)
        assert l04K == l04Ks

    def test_get_keys_l05(self, printKeys, debug):
        l05Ks = [
            "0:0:0",
            "0:0:1",
            "0:0:2",
            "0:1:0",
            "0:1:1",
            "0:1:2",
            "0:2:0",
            "0:2:1",
            "0:2:2",
            "1:0:0",
            "1:0:1",
            "1:0:2",
            "1:1:0",
            "1:1:1",
            "1:1:2",
            "1:2:0",
            "1:2:1",
            "1:2:2",
            "2:0:0",
            "2:0:1",
            "2:0:2",
            "2:1:0",
            "2:1:1",
            "2:1:2",
            "2:2:0",
            "2:2:1",
            "2:2:2",
        ]
        l05K = dict_json.getKeys(l05)
        print(f"keys: {l05K}") if printKeys else ""
        assert len(l05K) == len(l05Ks)
        assert l05K == l05Ks

    def testGetKeysj01(self, printKeys, debug):
        j01 = json.loads(j01s)
        j01K = dict_json.getKeys(j01)
        print(f"keys: {j01K}") if printKeys else ""
        assert len(j01K) == len(j01Ks)
        assert j01K == j01Ks

    def testGetKeysj02(self, printKeys, debug):
        j02 = json.loads(j02s)
        j02K = dict_json.getKeys(j02)
        print(f"keys: {j02K}") if printKeys else ""
        assert len(j02K) == len(j02Ks)
        assert j02K == j02Ks


class TestGetValue(object):
    """
    Tests for get_value

    Simple dict
    Simple list
    Nested dict, dict
    Nested dict, list, dict
    Nested list, dict
    Nested list, list, dict

    Simple dict - missing key
    Simple list - missing index
    Nested dict, dict - missing second key
    Nested dict, list, dict - missing second index
    Nested list, dict - missing second key
    Nested list, list, dict - missing third key

    """

    def test_dict_simple_exist(self):  # Simple dict
        key = f"k1"
        fieldValue = dict_json.Get_Value(d01, key)
        assert fieldValue == d01[key]

    def test_dict_list_exist(self):  # Nested dict, list-str
        key = ["d1", "1"]
        fieldValue = dict_json.Get_Value(d01l, dict_json.DELIMITER.join(key))
        assert fieldValue == d01l[key[0]][int(key[1])]

    def test_dict_list_int_exist(self):  # Nested dict, list-int
        key = ["d1", 1]
        fieldValue = dict_json.Get_Value(d01l, key)
        assert fieldValue == d01l[key[0]][key[1]]

    def test_dict_list_int_l05_exist(self):  # Nested dict, list-int
        key = ["1", 1, "0"]
        fieldValue = dict_json.Get_Value(l05, key)
        assert fieldValue == l05[int(key[0])][int(key[1])][int(key[2])]

    def test__json_dict_list_exist(self):  # Nested json dict, list, dict
        key = ["a"]
        j02 = json.loads(j02s)
        fieldValue = dict_json.Get_Value(j02, dict_json.DELIMITER.join(key))
        assert fieldValue == j02[key[0]]

    def test_json_dict_list_exist2(self):  # Nested json dict, list, dict
        key = ["b", "1"]
        j02 = json.loads(j02s)
        fieldValue = dict_json.Get_Value(j02, dict_json.DELIMITER.join(key))
        assert fieldValue == j02[key[0]][int(key[1])]

    def test_json_dict_list_missingList(self):  # Nested json dict, list, dict
        key = ["a", "1"]
        j02 = json.loads(j02s)
        with pytest.raises(TypeError):
            assert dict_json.Get_Value(j02, dict_json.DELIMITER.join(key))

    def test_json_dict_list_missing2(self):  # Nested json dict, list, dict
        key = ["b", "3"]
        j02 = json.loads(j02s)
        with pytest.raises(
            IndexError, match=rf"list index out of range for entry 1:{key[1]}"
        ):
            assert dict_json.Get_Value(j02, dict_json.DELIMITER.join(key))

    def test_dict_missing(self):  # Simple dict - missing key
        key = f"k1n"
        match_value = r"k1n for entry 0:{}".format(key)
        with pytest.raises(KeyError, match=rf"{key} for entry 0:{key}"):  # .format()):
            assert dict_json.Get_Value(d01, key)


class TestAddValue(object):
    """
    Tests for addValue

    Using d02

    """

    def test_d01_key_value_exists(self):
        key = "k1l"
        newValue = "yyy"
        dict_json.setValue(d01, key, newValue)
        fieldValue = dict_json.Get_Value(d01, key)
        assert fieldValue == newValue

    def test_d012_key_value_missing(self):
        key = "k1n:a"
        newValue = "yyy"
        dict_json.setValue(d01, key, newValue)
        fieldValue = dict_json.Get_Value(d01, key)
        assert fieldValue == newValue

    def test_normal_key_value_missing(self):
        key = "c:cc"
        newValue = "yyy"
        dict_json.setValue(normal_dict, key, newValue)
        assert normal_dict["c"]["cc"] == newValue

    def test_normal_key_value_missing(self):
        key = "c:cc"
        newValue = "yyy"
        dict_json.setValue(normal_dict, key, newValue)
        assert normal_dict["c"]["cc"] == newValue

    def test_d01_key_value_missing(self):
        key = "k1n"
        newValue = "yyy"
        dict_json.setValue(d01, key, newValue)
        fieldValue = dict_json.Get_Value(d01, key)
        assert newValue == d01[key]

    def test_d02_key_value_exists(self):
        key = "d1"
        newValue = "yyy"
        dict_json.setValue(d02, key, newValue)
        assert newValue == d02[key]

    def test_d02_key_value_missing(self):
        key = "d1l"
        newValue = "yyy"
        dict_json.setValue(d02, key, newValue)
        fieldValue = dict_json.Get_Value(d02, key)
        assert newValue == d02[key]

    def test_02_index_int_value_missing(self):
        key = ["k1", 1]
        newValue = "yyy"
        dict_json.setValue(d022, key, newValue)
        assert newValue == d022[key[0]][key[1]]

    def test_d02_index_str_value_missing(self):
        # dict_json.DELIMITER = '\0'
        keys = ["k1", "5"]
        key = dict_json.DELIMITER.join(keys)
        newValue = "yyy"
        dict_json.setValue(d022, key, newValue)
        assert newValue == d022[keys[0]][int(keys[1])]

    def test_l05_index_value_exists(self):
        keys = ["1", "1"]
        key = dict_json.DELIMITER.join(keys)
        newValue = "yyy"
        dict_json.setValue(l05, key, newValue)
        assert newValue == l05[int(keys[0])][int(keys[1])]

    def test_l05_index_value_missing(self):
        keys = ["1", "3"]
        key = dict_json.DELIMITER.join(keys)
        newValue = "yyy"
        dict_json.setValue(l05, key, newValue)
        assert newValue == l05[int(keys[0])][int(keys[1])]

    def test_l05_change_node(self):
        keys = ["b"]
        key = dict_json.DELIMITER.join(keys)
        newValue = "yyy"
        j02 = json.loads(j02s)
        dict_json.setValue(j02, key, newValue)
        assert newValue == j02[keys[0]]

    def test_l05_change_node_with_node(self):
        keys = ["b"]
        key = dict_json.DELIMITER.join(keys)
        newValue = {"zz": "yyy"}
        j02 = json.loads(j02s)
        dict_json.setValue(j02, key, newValue)
        assert newValue == j02[keys[0]]
