import pytest
from datetime import datetime

from history_dict import HistoryDict

test = HistoryDict()
test_data = {
    "key": {
        "newest": (datetime(2021, 9, 13, 10), "value-1"),
        datetime(2021, 9, 13, 12): "value-2",
    },
    "another_key": {"newest": (datetime(2021, 9, 13, 10), "value-xxx")},
}
test.load_test_data(test_data)


def test_get_existing_key():
    assert test.get("key") == "value-1"


def test_get_old_existing_key():
    assert test.get_old("key", datetime(2021, 9, 13, 12)) == "value-2"


def test_get_old_unexisting_key():
    assert test.get_old("key", datetime(2021, 9, 13, 9)) is None


def test_change_newest_key():
    assert test["another_key"] == "value-xxx"
    test["another_key"] = "value-xxx-2"
    assert test.get("another_key") == "value-xxx-2"


def test_get_unexisting_key():
    with pytest.raises(KeyError):
        test["fake"]
    assert test.get("fake") is None
