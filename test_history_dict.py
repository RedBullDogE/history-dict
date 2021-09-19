from copy import deepcopy
from datetime import datetime

import pytest

from history_dict import HistoryDict

test_dict = HistoryDict()
test_data = {
    "key": {datetime(2021, 9, 13, 12): "value-2", datetime(2021, 9, 13, 10): "value-1"},
    "another_key": {datetime(2021, 9, 13, 10): "value"},
    "key_to_delete": {datetime(2021, 1, 1, 0): "value"},
}
test_dict.load_test_data(test_data)


def test_get_existing_key():
    assert test_dict.get("key") == "value-1"


def test_get_unexisting_key():
    with pytest.raises(KeyError):
        test_dict["fake"]

    assert test_dict.get("fake") is None


def test_get_old_existing_key():
    assert test_dict.get_old("key", datetime(2021, 9, 13, 12)) == "value-2"


def test_get_old_unexisting_key():
    assert test_dict.get_old("unexisting_key", datetime(2021, 9, 13, 9)) is None
    assert test_dict.get_old("key", datetime(9999, 9, 9, 9)) is None


def test_change_newest_key():
    assert test_dict["another_key"] == "value"
    test_dict["another_key"] = "value-2"
    assert test_dict.get("another_key") == "value-2"


def test_pop_existing_key():
    prev_len = len(test_dict)
    assert test_dict.pop("key_to_delete") == {datetime(2021, 1, 1, 0): "value"}
    assert len(test_dict) == prev_len - 1


def test_pop_unexisting_key():
    with pytest.raises(KeyError):
        test_dict.pop("unxesisting_key")


def test_pop_old_unexisting_key():
    with pytest.raises(KeyError):
        test_dict.pop_old("unxesisting_key", datetime(2021, 1, 1, 1))

    with pytest.raises(KeyError):
        test_dict.pop_old("key", datetime(9999, 9, 9, 9))


def test_isinstance():
    assert isinstance(test_dict, dict) == True


def test_copying():
    original_dict = HistoryDict()
    original_dict["key"] = "value"

    deep_copy = deepcopy(original_dict)
    shallow_copy = original_dict

    deep_copy["key"] = "good-copy"
    shallow_copy["key"] = "bad-copy"

    
    assert deep_copy["key"] is not original_dict["key"]
    assert shallow_copy["key"] is original_dict["key"]
