from copy import deepcopy
from datetime import datetime

import pytest
from freezegun import freeze_time

from history_dict import HistoryDict


def test_get_existing_key():
    test_dict = HistoryDict()
    test_dict["key"] = "value-1"
    test_dict["key"] = "value-2"
    test_dict["key"] = "value-3"

    assert test_dict.get("key") == "value-3"


def test_get_unexisting_key():
    test_dict = HistoryDict()

    with pytest.raises(KeyError):
        test_dict["fake"]

    assert test_dict.get("fake") is None


def test_get_old_existing_key():
    test_dict = HistoryDict()

    with freeze_time(datetime(2021, 1, 1, 10)):
        test_dict["key"] = "old-value"
    with freeze_time(datetime(2021, 1, 1, 12)):
        test_dict["key"] = "new-value"

    assert test_dict.get_old("key", datetime(2021, 1, 1, 10)) == "old-value"
    assert test_dict.get_old("key", datetime(2021, 1, 1, 11)) == "old-value"
    assert test_dict.get_old("key", datetime(2021, 1, 1, 12)) == "new-value"


def test_get_old_unexisting_key():
    test_dict = HistoryDict()

    with freeze_time(datetime(2021, 1, 1, 10)):
        test_dict["key"] = "value"

    assert test_dict.get_old("key", datetime(2021, 1, 1, 8)) is None
    assert test_dict.get_old("unexisting_key", datetime(2021, 9, 13, 9)) is None


def test_change_newest_key():
    test_dict = HistoryDict()
    test_dict["key"] = "value"

    assert test_dict["key"] == "value"
    test_dict["key"] = "value-2"
    assert test_dict.get("key") == "value-2"


def test_pop_existing_key():
    test_dict = HistoryDict()
    test_dict["key1"] = "value-1"
    test_dict["key1"] = "value-2"
    test_dict["key2"] = "value-3"
    test_dict["key3"] = "value-4"

    prev_len = len(test_dict)
    popped_value = test_dict.pop("key3")

    assert type(popped_value) == dict
    assert list(popped_value.values())[0] == "value-4"
    assert len(test_dict) == prev_len - 1


def test_pop_unexisting_key():
    test_dict = HistoryDict()
    test_dict["key"] = "value"

    with pytest.raises(KeyError):
        test_dict.pop("unxesisting_key")


def test_isinstance():
    test_dict = HistoryDict()

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
