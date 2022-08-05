import json
import logging

import pytest

from dict_json import dict_json

# import yaml

delimiter = dict_json.DELIMITER
# delimiter = '\0'
# dict_json.DELIMITER = delimiter


# logging.basicConfig(level=logging.INFO)
logging.basicConfig(level=logging.DEBUG)

"""
Generator for json
Need to generate dict and list test data.
d_def(5)(1:l_def(4)(d_def(2))

l_def(0:3, d
d_def(4)

"""


def d_def(*arg, n=1):
    """Create a test dictionary
    Number of fields in dictionary
    keys are k99, values are random
    :param n: Number of keys in test dict
    :return:
    """
    d_work = {}
    for x in range(n):
        d_work[f"k{x}"] = "x" + ("s" * x) if len(arg) == 0 else arg[x % len(arg)].copy()
    return d_work


def l_def(*arg, n=1):
    """Create test list
    Number of elements in list
    values are random

    :param n: Number of elements in test list
    :return:
    """
    ls: list[...] = [None] * n
    if arg == ():
        for index in range(n):
            ls[index] = "x" + ("s" * index)
    else:
        for index in range(n):
            ls[index] = arg[index % len(arg)].copy()
    return ls


d01 = d_def(n=3)
d02 = d_def(n=3)

l01 = l_def(n=3)
l02 = l_def(n=3)

d01l = d_def(n=3)
d01l["d0"] = l01
d01l["d1"] = l02
d01l["d2"] = d02

d022 = d_def(l01, l01, d01, n=3)

l03: list[...] = l_def(d02, n=2)
l04: list[...] = l_def(l01, n=3)
l05: list[...] = l_def(l04, n=3)

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
j01_ks = ["a", "b:c", "b:d"]

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
j02_ks = ["a", "b:0:c", "b:0:d", "b:1:c", "b:1:d"]

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


@pytest.fixture
def print_keys(request):
    return request.config.getoption("--print")


class TestGetKeys(object):
    def test_get_keys_d01(self, print_keys, debug):
        d01_ks = ["k0", "k1", "k2"]
        d01_k = dict_json.getKeys(d01)
        print(f"keys: {d01_k}") if print_keys else ""
        assert len(d01_k) == len(d01_ks)
        assert d01_k == d01_ks

    def test_get_keys_d02(self, print_keys, debug):
        d02_ks = [
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
        d02_k = dict_json.getKeys(d022)
        print(f"keys: {d02_k}") if print_keys else ""
        assert len(d02_k) == len(d02_ks)
        assert d02_k == d02_ks

    def test_get_keys_d02_list(self, print_keys, debug):
        d02_ks = [
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
        d02_k = dict_json.getKeys(d022, seralize=False)
        print(f"keys: {d02_k}") if print_keys else ""
        assert len(d02_k) == len(d02_ks)
        assert d02_k == d02_ks

    def test_get_keys_l01(self, print_keys, debug):
        l01_ks = ["0", "1", "2"]
        l01_k = dict_json.getKeys(l01)
        print(f"keys: {l01_ks}") if print_keys else ""
        assert len(l01_k) == len(l01_ks)
        assert l01_k == l01_ks

    def test_get_keys_l04(self, print_keys, debug):
        l04_ks = ["0:0", "0:1", "0:2", "1:0", "1:1", "1:2", "2:0", "2:1", "2:2"]
        l04_k = dict_json.getKeys(l04)
        print(f"keys: {l04_k}") if print_keys else ""
        assert len(l04_k) == len(l04_ks)
        assert l04_k == l04_ks

    def test_get_keys_l05(self, print_keys, debug):
        l05_ks = [
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
        l05_k = dict_json.getKeys(l05)
        print(f"keys: {l05_k}") if print_keys else ""
        assert len(l05_k) == len(l05_ks)
        assert l05_k == l05_ks

    def test_get_keys_j01(self, print_keys, debug):
        j01 = json.loads(j01s)
        j01_k = dict_json.getKeys(j01)
        print(f"keys: {j01_k}") if print_keys else ""
        assert len(j01_k) == len(j01_ks)
        assert j01_k == j01_ks

    def test_get_keys_j02(self, print_keys, debug):
        j02 = json.loads(j02s)
        j02k = dict_json.getKeys(j02)
        print(f"keys: {j02k}") if print_keys else ""
        assert len(j02k) == len(j02_ks)
        assert j02k == j02_ks


class TestSetValue(object):
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
        field_value = dict_json.Get_Value(d01, key)
        assert field_value == d01[key]

    def test_dict_list_exist(self):  # Nested dict, list-str
        key = ["d1", "1"]
        field_value = dict_json.Get_Value(d01l, dict_json.DELIMITER.join(key))
        assert field_value == d01l[key[0]][int(key[1])]

    def test_dict_list_int_exist(self):  # Nested dict, list-int
        key = ["d1", 1]
        field_value = dict_json.Get_Value(d01l, key)
        assert field_value == d01l[key[0]][key[1]]

    def test_dict_list_int_l05_exist(self):  # Nested dict, list-int
        key = ["1", 1, "0"]
        field_value = dict_json.Get_Value(l05, key)
        assert field_value == l05[int(key[0])][int(key[1])][int(key[2])]

    def test__json_dict_list_exist(self):  # Nested json dict, list, dict
        key = ["a"]
        j02 = json.loads(j02s)
        field_value = dict_json.Get_Value(j02, dict_json.DELIMITER.join(key))
        assert field_value == j02[key[0]]

    def test_json_dict_list_exist2(self):  # Nested json dict, list, dict
        key = ["b", "1"]
        j02 = json.loads(j02s)
        field_value = dict_json.Get_Value(j02, dict_json.DELIMITER.join(key))
        assert field_value == j02[key[0]][int(key[1])]

    def test_json_dict_list_missing_list(self):  # Nested json dict, list, dict
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
        # match_value = r"k1n for entry 0:{}".format(key)
        with pytest.raises(KeyError, match=rf"{key} for entry 0:{key}"):  # .format()):
            assert dict_json.Get_Value(d01, key)


class TestAddValue(object):
    """
    Tests for addValue

    Using d02

    """

    def test_d01_key_value_exists(self):
        key = "k1l"
        new_value = "yyy"
        dict_json.setValue(d01, key, new_value)
        field_value = dict_json.Get_Value(d01, key)
        assert field_value == new_value

    def test_d012_key_value_missing(self):
        key = "k1n:a"
        new_value = "yyy"
        dict_json.setValue(d01, key, new_value)
        field_value = dict_json.Get_Value(d01, key)
        assert field_value == new_value

    def test_normal_key_value_missing(self):
        key = "c:cc"
        new_value = "yyy"
        dict_json.setValue(normal_dict, key, new_value)
        assert normal_dict["c"]["cc"] == new_value

    def test_d01_key_value_missing(self):
        key = "k1n"
        new_value = "yyy"
        dict_json.setValue(d01, key, new_value)
        # field_value = dict_json.Get_Value(d01, key)
        assert new_value == d01[key]

    def test_d02_key_value_exists(self):
        key = "d1"
        new_value = "yyy"
        dict_json.setValue(d02, key, new_value)
        assert new_value == d02[key]

    def test_d02_key_value_missing(self):
        key = "d1l"
        new_value = "yyy"
        dict_json.setValue(d02, key, new_value)
        # field_value = dict_json.Get_Value(d02, key)
        assert new_value == d02[key]

    def test_02_index_int_value_missing(self):
        key = ["k1", 1]
        new_value = "yyy"
        dict_json.setValue(d022, key, new_value)
        assert new_value == d022[key[0]][key[1]]

    def test_d02_index_str_value_missing(self):
        # dict_json.DELIMITER = '\0'
        keys = ["k1", "5"]
        key = dict_json.DELIMITER.join(keys)
        new_value = "yyy"
        dict_json.setValue(d022, key, new_value)
        assert new_value == d022[keys[0]][int(keys[1])]

    def test_l05_index_value_exists(self):
        keys = ["1", "1"]
        key = dict_json.DELIMITER.join(keys)
        new_value = "yyy"
        dict_json.setValue(l05, key, new_value)
        assert new_value == l05[int(keys[0])][int(keys[1])]

    def test_l05_index_value_missing(self):
        keys = ["1", "3"]
        key = dict_json.DELIMITER.join(keys)
        new_value = "yyy"
        dict_json.setValue(l05, key, new_value)
        assert new_value == l05[int(keys[0])][int(keys[1])]

    def test_l05_change_node(self):
        keys = ["b"]
        key = dict_json.DELIMITER.join(keys)
        new_value = "yyy"
        j02 = json.loads(j02s)
        dict_json.setValue(j02, key, new_value)
        assert new_value == j02[keys[0]]

    def test_l05_change_node_with_node(self):
        keys = ["b"]
        key = dict_json.DELIMITER.join(keys)
        new_value = {"zz": "yyy"}
        j02 = json.loads(j02s)
        dict_json.setValue(j02, key, new_value)
        assert new_value == j02[keys[0]]
